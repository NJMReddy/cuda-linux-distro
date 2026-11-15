#!/usr/bin/env python3
"""Failure-path regression tests; no synthetic GPU successes or build artifacts."""
import importlib.machinery
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(name,path):
    loader=importlib.machinery.SourceFileLoader(name,str(path))
    spec=importlib.util.spec_from_loader(name,loader)
    module=importlib.util.module_from_spec(spec); loader.exec_module(module)
    return module
bench=load('benchmark',ROOT/'buildroot/board/cuda-distro/rootfs-overlay/usr/local/bin/cuda-benchmark')
image=load('image_validator',ROOT/'scripts/validate-image.py')

class Regressions(unittest.TestCase):
    def test_missing_driver_returns_77_and_records_blocked(self):
        with tempfile.TemporaryDirectory() as t, mock.patch.object(bench.C,'CDLL',side_effect=OSError('driver unavailable')):
            dest=pathlib.Path(t)/'result.json'
            self.assertEqual(bench.main(['--output-json',str(dest)]),77)
            result=json.loads(dest.read_text())
            self.assertEqual(result['status'],'BLOCKED')
            self.assertFalse(result['gpu_computation_performed'])
    def test_driver_runtime_error_is_failure(self):
        with mock.patch.object(bench,'run',side_effect=RuntimeError('cuLaunchKernel failed')):
            self.assertEqual(bench.main([]),1)
    def test_invalid_dimensions_rejected(self):
        with self.assertRaises(SystemExit) as ex:
            bench.main(['--size','0'])
        self.assertEqual(ex.exception.code,2)
    def test_empty_disk_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t)/'empty.img'; p.write_bytes(b'')
            with self.assertRaises(ValueError): image.validate(p)
    def test_blank_disk_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t)/'blank.img'; p.write_bytes(bytes(4096))
            with self.assertRaises(ValueError): image.validate(p)
    def test_unlike_comparison_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            a=pathlib.Path(t)/'a.json'; b=pathlib.Path(t)/'b.json'
            a.write_text(json.dumps({'measurement_definition':'disk'})); b.write_text(json.dumps({'measurement_definition':'container'}))
            result=subprocess.run([sys.executable,str(ROOT/'scripts/compare-metrics.py'),str(a),str(b)],capture_output=True)
            self.assertNotEqual(result.returncode,0)
    def test_unmeasured_values_stay_unmeasured(self):
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t)/'input.json'; p.write_text(json.dumps({'measurement_definition':'same setup'}))
            result=subprocess.run([sys.executable,str(ROOT/'scripts/compare-metrics.py'),str(p),str(p)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0)
            self.assertTrue(all(r['status']=='NOT TESTED' and r['reduction_percent'] is None for r in json.loads(result.stdout)['measurements']))

if __name__=='__main__': unittest.main()
