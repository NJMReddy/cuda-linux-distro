#!/usr/bin/env python3
"""Reject silently dropped/changed requested Buildroot symbols."""
import pathlib, sys
root=pathlib.Path(__file__).resolve().parents[1]
def load(p):
    return dict(line.split('=',1) for line in pathlib.Path(p).read_text().splitlines() if line.startswith('BR2_') and '=' in line)
want=load(root/'buildroot/configs/cuda_distro_defconfig'); got=load(sys.argv[1]); errors=[]
for key,value in want.items():
    if value=='n':
        if got.get(key)=='y': errors.append(key+' unexpectedly enabled')
    elif got.get(key)!=value:
        errors.append(f'{key}: requested {value}, resolved {got.get(key,"unset")}')
for error in errors: print('FAIL',error)
sys.exit(bool(errors))
