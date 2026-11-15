#!/usr/bin/env python3
"""Static and optional artifact checks. Never equate static checks to readiness."""
import argparse
import ast
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
rows=[]
def record(name,status,detail=''):
    rows.append(dict(check=name,status=status,detail=detail))
    print(f'{status}: {name} {detail}')
def check(name,condition,detail=''):
    record(name,'PASS' if condition else 'FAIL',detail)
def read(p): return (ROOT/p).read_text(encoding='utf-8')

def static():
    external=read('buildroot/external.mk')
    check('external make recipes included','include $(sort $(wildcard' in external)
    cfg=read('buildroot/configs/cuda_distro_defconfig')
    requested=dict(re.findall(r'^(BR2_\w+)=(.*)$',cfg,re.M))
    check('distinct NVIDIA package selected',requested.get('BR2_PACKAGE_CUDA_NVIDIA_DRIVER')=='y' and 'BR2_PACKAGE_NVIDIA_DRIVER=y' not in cfg)
    for key,value in {'BR2_LINUX_KERNEL_NEEDS_HOST_LIBELF':'y','BR2_TARGET_GENERIC_ROOT_PASSWD':'"*"','BR2_TARGET_GENERIC_REMOUNT_ROOTFS_RW':'n','BR2_PACKAGE_RUNC':'y','BR2_LINUX_KERNEL_CUSTOM_VERSION_VALUE':'"6.6.18"'}.items():
        check(key,requested.get(key)==value)
    symbols=[]
    for pkg in sorted((ROOT/'buildroot/package').iterdir()):
        text=(pkg/(pkg.name+'.mk')).read_text()
        prefix=pkg.name.upper().replace('-','_')
        symbols += re.findall(r'^config (\w+)',(pkg/'Config.in').read_text(),re.M)
        check(pkg.name+' hash exists',bool(re.search(r'^sha256  [0-9a-f]{64}  \S+', (pkg/(pkg.name+'.hash')).read_text(),re.M)))
        check(pkg.name+' recipe uses correct namespace',f'{prefix}_VERSION =' in text and '$(eval $(generic-package))' in text)
        check(pkg.name+' installs without suppressed errors','|| true' not in text)
    check('package Kconfig names unique',len(symbols)==len(set(symbols)))
    kernel=read('kernel/linux.config')
    for flag in ['CONFIG_MODULES=y','CONFIG_EFI_PARTITION=y','CONFIG_EXT4_FS=y','CONFIG_VIRTIO_BLK=y','CONFIG_SERIAL_8250_CONSOLE=y','CONFIG_OVERLAY_FS=y','CONFIG_CGROUPS=y','CONFIG_NAMESPACES=y','CONFIG_SECCOMP_FILTER=y','CONFIG_RANDOMIZE_BASE=y']:
        check(flag,flag in kernel.splitlines())
    check('module autoload not disabled','CONFIG_STATIC_USERMODEHELPER=y' not in kernel)
    check('nouveau disabled',not re.search(r'^CONFIG_DRM_NOUVEAU=[ym]',kernel,re.M))
    post=read('buildroot/board/cuda-distro/post-build.sh')
    check('read-only root has noauto/pass=0','/dev/root / ext4 ro,noauto,noatime 0 0' in post)
    check('no systemd overlay ordering','x-systemd' not in post)
    svc=read('buildroot/board/cuda-distro/rootfs-overlay/etc/init.d/cuda-writable')
    check('overlay service orders after localmount','need localmount' in svc and svc.index('mkdir -p')<svc.index('mount -t overlay'))
    bench=ROOT/'buildroot/board/cuda-distro/rootfs-overlay/usr/local/bin/cuda-benchmark'
    ast.parse(bench.read_text()); check('benchmark no undeclared framework','import torch' not in bench.read_text())
    for file in list((ROOT/'scripts').glob('*.py'))+[bench]:
        ast.parse(file.read_text()); record('Python syntax '+str(file.relative_to(ROOT)),'PASS')
    nb=json.loads(read('colab/cuda_benchmark.ipynb'))
    check('notebook document structure',nb.get('nbformat')==4 and isinstance(nb.get('cells'),list))
    overlay_bin=list((ROOT/'buildroot/board/cuda-distro/rootfs-overlay/usr/local/bin').iterdir())
    for file in overlay_bin:
        if file.is_file() and file.read_bytes().startswith(b'#!/usr/bin/env python3'):
            ast.parse(file.read_text()); record('Python overlay syntax '+file.name,'PASS')
    shell_files=list((ROOT/'scripts').glob('*.sh'))+list((ROOT/'buildroot/board/cuda-distro').glob('*.sh'))+[ROOT/'security/hardening.sh']+list((ROOT/'buildroot/board/cuda-distro/rootfs-overlay/etc/init.d').iterdir())+[f for f in overlay_bin if f.is_file() and f.read_bytes().startswith(b'#!/bin/sh')]
    bash=shutil.which('bash')
    usable=False
    if bash:
        try:
            probe=subprocess.run([bash,'-c','exit 0'],capture_output=True)
            usable=probe.returncode==0
        except OSError:
            usable=False
    if usable:
        for file in shell_files:
            p=subprocess.run([bash,'-n',str(file)],capture_output=True,text=True)
            check('shell syntax '+str(file.relative_to(ROOT)),p.returncode==0,p.stderr.strip())
    else:
        record('bash -n shell syntax','BLOCKED','No usable Bash runtime')
        # Optional native Windows parser; the Linux Bash checks remain required.
        try:
            import tree_sitter, tree_sitter_bash
            parser=tree_sitter.Parser(tree_sitter.Language(tree_sitter_bash.language()))
            for file in shell_files:
                check('tree-sitter shell parse '+str(file.relative_to(ROOT)),not parser.parse(file.read_bytes()).root_node.has_error)
        except ImportError:
            record('alternate shell parser','NOT TESTED','Optional tree-sitter-bash unavailable')
    check('report has no invented score','98 / 100' not in read('docs/rubric-compliance.md'))

def artifacts(target,images):
    if target:
        target=pathlib.Path(target)
        for pattern in ['lib/modules/*/extra/nvidia.ko*','lib/modules/*/extra/nvidia-uvm.ko*','lib/modules/*/modules.dep','usr/lib/libcuda.so.1','usr/lib/libnvidia-ml.so.1','usr/lib/libcudart.so.12','usr/lib/libcudnn.so.9','usr/lib/libcublas.so.12','usr/lib/libnvrtc.so.12','usr/bin/nvidia-smi','usr/bin/runc','usr/bin/python3']:
            matches=list(target.glob(pattern))
            check('target '+pattern,any(p.is_file() and p.stat().st_size>0 for p in matches))
        for dep in target.glob('lib/modules/*/modules.dep'):
            check('NVIDIA module dependency metadata',all(name in dep.read_text() for name in ['nvidia.ko','nvidia-uvm.ko']))
        for filename in ['libcuda.so.550.127.05','libnvidia-ml.so.550.127.05','libnvidia-ptxjitcompiler.so.550.127.05','libnvidia-nvvm.so.4.0.0']:
            check('pinned driver library '+filename,(target/'usr/lib'/filename).is_file())
        readelf=shutil.which('readelf')
        if readelf:
            libraries={p.resolve() for pattern in ['libcuda.so*','libnvidia*.so*','libcud*.so*','libcublas*.so*','libnvrtc*.so*'] for p in (target/'usr/lib').glob(pattern) if p.is_file()}
            for lib in sorted(libraries):
                proc=subprocess.run([readelf,'-d',str(lib)],capture_output=True,text=True)
                needed=re.findall(r'\(NEEDED\).*\[(.*?)\]',proc.stdout)
                missing=[name for name in needed if not any((target/directory/name).is_file() for directory in ['usr/lib','lib','lib64','usr/lib64'])]
                check('ELF dependencies '+lib.name,proc.returncode==0 and not missing,', '.join(missing))
        else: record('ELF dependency closure','BLOCKED','readelf unavailable')
        shadow=(target/'etc/shadow')
        check('target root secured',shadow.is_file() and bool(re.search(r'^root:(!|\$6\$)[^:]*:',shadow.read_text())))
    else: record('target installation','BLOCKED','No built target supplied')
    if images:
        images=pathlib.Path(images)
        for f in ['bzImage','rootfs.ext4','efi-part/EFI/BOOT/bootx64.efi']:
            check('boot artifact '+f,(images/f).is_file() and (images/f).stat().st_size>0)
        p=subprocess.run([sys.executable,str(ROOT/'scripts/validate-image.py'),str(images/'cuda-distro.img')])
        check('GPT/ESP/rootfs image validation',p.returncode==0)
    else: record('image structure','BLOCKED','No built image supplied')
    for name in ['QEMU complete runtime','real NVIDIA driver load','CUDA numerical GPU execution','cuDNN execution','OCI container execution','stock comparison','reproducibility rebuild']:
        record(name,'NOT TESTED','Requires independently captured runtime/build evidence')

def main():
    p=argparse.ArgumentParser(); p.add_argument('--target'); p.add_argument('--images'); p.add_argument('--json'); p.add_argument('--release',action='store_true'); args=p.parse_args()
    try: static(); artifacts(args.target,args.images)
    except Exception as e: record('verification exception','FAIL',str(e))
    if args.json:
        pathlib.Path(args.json).parent.mkdir(parents=True,exist_ok=True)
        pathlib.Path(args.json).write_text(json.dumps(rows,indent=2)+'\n')
    failures=any(r['status']=='FAIL' for r in rows)
    incomplete=any(r['status'] in ['BLOCKED','NOT TESTED'] for r in rows)
    print('Submission readiness: NOT READY' if failures or incomplete else 'Submission readiness: requires final human evidence review')
    return int(failures or (args.release and incomplete))

if __name__=='__main__': sys.exit(main())
