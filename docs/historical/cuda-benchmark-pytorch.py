#!/usr/bin/env python3
"""
CUDA Benchmark Suite
Part of the Custom Linux Distribution for CUDA/GPU Compute (Track C).
Executes GPU validation, matrix multiplication (GEMM) benchmark,
and deep learning inference latency evaluation.

Designed to operate seamlessly on physical NVIDIA hardware,
cloud instances (Google Colab / AWS), or CPU-only QEMU emulation.
"""

import argparse
import json
import os
import sys
import time

def get_gpu_info():
    info = {
        "device_available": False,
        "device_name": "None",
        "cuda_version": "N/A",
        "device_count": 0,
        "memory_total_mb": 0.0,
        "execution_mode": "CPU_FALLBACK"
    }
    # Try PyTorch detection
    try:
        import torch
        if torch.cuda.is_available():
            info["device_available"] = True
            info["device_count"] = torch.cuda.device_count()
            info["device_name"] = torch.cuda.get_device_name(0)
            info["cuda_version"] = torch.version.cuda
            props = torch.cuda.get_device_properties(0)
            info["memory_total_mb"] = round(props.total_memory / (1024 * 1024), 2)
            info["compute_capability"] = f"{props.major}.{props.minor}"
            info["execution_mode"] = "CUDA_GPU"
            return info
        else:
            info["execution_mode"] = "CPU_PYTORCH_AVAILABLE"
    except ImportError:
        pass

    # Fallback to nvidia-smi if torch is not yet installed or running as standalone binary
    try:
        import subprocess
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader,nounits"],
            stderr=subprocess.DEVNULL,
            universal_newlines=True
        ).strip().split(",")
        if len(out) >= 2:
            info["device_available"] = True
            info["device_name"] = out[0].strip()
            info["memory_total_mb"] = float(out[1].strip())
            info["driver_version"] = out[2].strip() if len(out) > 2 else "Unknown"
            info["execution_mode"] = "NVIDIA_SMI_ONLY"
    except Exception:
        pass

    return info

def run_gemm_benchmark(matrix_size=4096, iterations=50, allow_cpu_fallback=False):
    """Measures single-precision GEMM throughput (TFLOPS)."""
    results = {
        "matrix_size": f"{matrix_size}x{matrix_size}",
        "iterations": iterations,
        "avg_latency_ms": 0.0,
        "tflops": 0.0,
        "status": "FAILED"
    }
    try:
        import torch
        if not torch.cuda.is_available():
            if not allow_cpu_fallback:
                results["status"] = "SKIPPED_NO_GPU"
                results["reason"] = "No CUDA GPU detected; QEMU CPU emulation mode"
                return results
            device = torch.device("cpu")
            matrix_size = min(matrix_size, 1024)
            iterations = 5
        else:
            device = torch.device("cuda:0")

        a = torch.randn(matrix_size, matrix_size, device=device, dtype=torch.float32)
        b = torch.randn(matrix_size, matrix_size, device=device, dtype=torch.float32)

        # Warm-up iterations
        for _ in range(5):
            c = torch.matmul(a, b)
        if device.type == "cuda":
            torch.cuda.synchronize()

        # Timed loop
        latencies = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            c = torch.matmul(a, b)
            if device.type == "cuda":
                torch.cuda.synchronize()
            t1 = time.perf_counter()
            latencies.append((t1 - t0) * 1000.0)

        avg_lat = sum(latencies) / len(latencies)
        # FLOPs for NxN GEMM = 2 * N^3
        total_flops = 2.0 * (matrix_size ** 3)
        tflops = (total_flops / (avg_lat / 1000.0)) / 1e12

        results["avg_latency_ms"] = round(avg_lat, 2)
        results["min_latency_ms"] = round(min(latencies), 2)
        results["max_latency_ms"] = round(max(latencies), 2)
        results["tflops"] = round(tflops, 3)
        results["status"] = "SUCCESS"
    except ImportError as e:
        results["status"] = "SKIPPED_NO_GPU"
        results["reason"] = f"PyTorch/CUDA runtime not installed in host environment ({e})"
    except Exception as e:
        results["error"] = str(e)
    return results

def run_inference_benchmark(batch_size=16, iterations=50, allow_cpu_fallback=False):
    """Measures ResNet-50 inference latency and throughput (FPS)."""
    results = {
        "model": "ResNet-50",
        "batch_size": batch_size,
        "iterations": iterations,
        "avg_latency_ms": 0.0,
        "throughput_fps": 0.0,
        "status": "FAILED"
    }
    try:
        import torch
        import torchvision.models as models
        if not torch.cuda.is_available():
            if not allow_cpu_fallback:
                results["status"] = "SKIPPED_NO_GPU"
                results["reason"] = "No CUDA GPU detected; QEMU CPU emulation mode"
                return results
            device = torch.device("cpu")
            batch_size = 1
            iterations = 3
            model = models.resnet50(weights=None).to(device).eval()
            dummy_input = torch.randn(batch_size, 3, 224, 224, device=device)
        else:
            device = torch.device("cuda:0")
            model = models.resnet50(weights=None).to(device).half().eval()
            dummy_input = torch.randn(batch_size, 3, 224, 224, device=device, dtype=torch.float16)

        # Warm-up iterations
        with torch.no_grad():
            for _ in range(5):
                _ = model(dummy_input)
            if device.type == "cuda":
                torch.cuda.synchronize()

        # Benchmark loop
        latencies = []
        with torch.no_grad():
            for _ in range(iterations):
                t0 = time.perf_counter()
                _ = model(dummy_input)
                if device.type == "cuda":
                    torch.cuda.synchronize()
                t1 = time.perf_counter()
                latencies.append((t1 - t0) * 1000.0)

        avg_lat = sum(latencies) / len(latencies)
        fps = (batch_size * 1000.0) / avg_lat

        results["avg_latency_ms"] = round(avg_lat, 2)
        results["latency_per_sample_ms"] = round(avg_lat / batch_size, 3)
        results["throughput_fps"] = round(fps, 1)
        results["status"] = "SUCCESS"
    except ImportError as e:
        results["status"] = "SKIPPED_NO_GPU"
        results["reason"] = f"PyTorch/CUDA runtime not installed in host environment ({e})"
    except Exception as e:
        results["error"] = str(e)
    return results

def main():
    parser = argparse.ArgumentParser(description="Custom Linux Distro CUDA Benchmark Suite")
    parser.add_argument("--all", action="store_true", help="Run full benchmark suite")
    parser.add_argument("--gemm", action="store_true", help="Run GEMM (matrix multiplication) benchmark")
    parser.add_argument("--inference", action="store_true", help="Run ResNet-50 inference benchmark")
    parser.add_argument("--output-json", type=str, default="/var/log/cuda-benchmark/results.json",
                        help="Path to save output JSON report")
    parser.add_argument("--matrix-size", type=int, default=4096, help="Matrix dimension for GEMM")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size for inference")
    parser.add_argument("--allow-cpu-fallback", action="store_true",
                        help="Allow CPU execution fallback when no GPU is present")
    args = parser.parse_args()

    if not (args.all or args.gemm or args.inference):
        args.all = True

    print("=" * 60)
    print("  Custom CUDA Linux Distribution — System Benchmark")
    print("=" * 60)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    report = {
        "timestamp": timestamp,
        "system_info": get_gpu_info(),
        "benchmarks": {}
    }

    print(f"Timestamp:       {timestamp}")
    print(f"Execution Mode:  {report['system_info']['execution_mode']}")
    print(f"GPU Detected:    {report['system_info']['device_name']}")
    print(f"CUDA Version:    {report['system_info'].get('cuda_version', 'N/A')}")
    print(f"Total VRAM:      {report['system_info']['memory_total_mb']} MB")
    print("-" * 60)

    exit_code = 0

    if args.all or args.gemm:
        print(f"Running GEMM Benchmark (Size: {args.matrix_size}x{args.matrix_size})...")
        gemm_res = run_gemm_benchmark(
            matrix_size=args.matrix_size,
            allow_cpu_fallback=args.allow_cpu_fallback
        )
        report["benchmarks"]["gemm"] = gemm_res
        if gemm_res["status"] == "SUCCESS":
            print(f"  -> Latency:    {gemm_res['avg_latency_ms']} ms")
            print(f"  -> Throughput: {gemm_res['tflops']} TFLOPS")
        elif gemm_res["status"] == "SKIPPED_NO_GPU":
            print(f"  -> Status:     SKIPPED (No NVIDIA GPU hardware detected in this environment)")
        else:
            print(f"  -> Status:     FAILED ({gemm_res.get('error', 'unknown error')})")
            exit_code = 1

    if args.all or args.inference:
        print(f"\nRunning Inference Benchmark (ResNet-50, Batch: {args.batch_size})...")
        inf_res = run_inference_benchmark(
            batch_size=args.batch_size,
            allow_cpu_fallback=args.allow_cpu_fallback
        )
        report["benchmarks"]["inference"] = inf_res
        if inf_res["status"] == "SUCCESS":
            print(f"  -> Latency:    {inf_res['avg_latency_ms']} ms ({inf_res['latency_per_sample_ms']} ms/sample)")
            print(f"  -> Throughput: {inf_res['throughput_fps']} FPS")
        elif inf_res["status"] == "SKIPPED_NO_GPU":
            print(f"  -> Status:     SKIPPED (No NVIDIA GPU hardware detected in this environment)")
        else:
            print(f"  -> Status:     FAILED ({inf_res.get('error', 'unknown error')})")
            exit_code = 1

    print("=" * 60)

    # Ensure output directory exists and save results
    out_dir = os.path.dirname(args.output_json)
    if out_dir:
        try:
            os.makedirs(out_dir, exist_ok=True)
            with open(args.output_json, "w") as f:
                json.dump(report, f, indent=2)
            print(f"Benchmark results successfully written to: {args.output_json}")
        except Exception as e:
            print(f"Warning: Could not write JSON output to {args.output_json}: {e}")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
