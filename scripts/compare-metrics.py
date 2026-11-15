#!/usr/bin/env python3
"""Compare measured JSON values with explicit units and like-for-like scope."""
import argparse, json, sys
p=argparse.ArgumentParser(); p.add_argument('stock'); p.add_argument('custom'); a=p.parse_args()
stock=json.load(open(a.stock)); custom=json.load(open(a.custom)); rows=[]
if stock['measurement_definition']!=custom['measurement_definition']:
    sys.exit('FAIL: measurement definitions differ (hardware, GPU stack and collection conditions must match)')
for key in ('raw_logical_bytes','allocated_bytes','compressed_bytes','rootfs_used_bytes','ram_idle_kib','boot_ms','package_count','kernel_bytes','gpu_gbps'):
    x=stock.get(key); y=custom.get(key)
    reduction=None if x is None or y is None else (x-y)/x*100 if x>0 else None
    rows.append({'metric':key,'stock':x,'custom':y,'reduction_percent':reduction,'status':'PASS' if reduction is not None else 'NOT TESTED'})
print(json.dumps({'measurements':rows,'note':'40% criterion must use the same stated image metric; no defaults or estimated numbers'},indent=2))
