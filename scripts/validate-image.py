#!/usr/bin/env python3
"""Validate primary/backup GPT CRCs, ESP EFI executable and rootfs ext magic.
This does not establish boot success. Read-only; handles sparse raw files.
"""
import pathlib, struct, sys, uuid, zlib
def validate(path):
    size=path.stat().st_size
    with path.open('rb') as f:
        def read(off,n):
            f.seek(off); b=f.read(n)
            if len(b)!=n: raise ValueError('truncated image')
            return b
        if read(510,2)!=b'\x55\xaa': raise ValueError('missing protective MBR signature')
        def header(lba):
            h=bytearray(read(lba*512,512)); assert h[:8]==b'EFI PART','GPT signature'
            n=struct.unpack_from('<I',h,12)[0]; expected=struct.unpack_from('<I',h,16)[0]
            assert 92<=n<=512,'GPT header size'; struct.pack_into('<I',h,16,0)
            assert zlib.crc32(h[:n])==expected,'GPT header CRC'
            current,backup,first,last=struct.unpack_from('<QQQQ',h,24)
            assert current==lba and first<=last<size//512,'GPT bounds'
            entry_lba,count,stride,crc=struct.unpack_from('<QIII',h,72)
            assert 0<count<=4096 and 128<=stride<=4096,'entry dimensions'
            entries=read(entry_lba*512,count*stride)
            assert zlib.crc32(entries)==crc,'GPT entry CRC'
            return backup, entries, stride
        backup,entries,stride=header(1); back,be,bs=header(backup)
        assert back==1 and be==entries and bs==stride,'backup GPT mismatch'
        partitions=[]
        for i in range(0,len(entries),stride):
            e=entries[i:i+stride]
            if e[:16]==bytes(16): continue
            start,end=struct.unpack_from('<QQ',e,32)
            assert 34<=start<=end<backup,'partition bounds'
            partitions.append((start,end,e[:16]))
        assert len(partitions)==2,'expected ESP and root'
        esp,root=partitions
        assert esp[1]<root[0],'overlapping partitions'
        assert esp[2]==uuid.UUID('c12a7328-f81f-11d2-ba4b-00a0c93ec93b').bytes_le,'ESP type'
        # Check FAT boot signature and executable presence in bounded ESP bytes.
        fat=read(esp[0]*512,(esp[1]-esp[0]+1)*512)
        assert fat[510:512]==b'\x55\xaa','ESP boot signature'
        assert b'BOOTX64 EFI' in fat.upper(),'EFI fallback filename absent'
        assert b'PE\x00\x00' in fat,'PE EFI executable absent'
        assert read(root[0]*512+1024+56,2)==b'\x53\xef','ext root filesystem magic'
    return {'logical_bytes':size,'partitions':len(partitions)}
if __name__=='__main__':
    try: print('PASS image structure',validate(pathlib.Path(sys.argv[1])))
    except (AssertionError,ValueError,OSError,IndexError) as e:
        print('FAIL image structure:',e,file=sys.stderr); sys.exit(1)
