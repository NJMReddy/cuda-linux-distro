#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
host="$root/buildroot-src/output/host"
compiler="$host/bin/x86_64-buildroot-linux-gnu-g++"
sysroot=$("$compiler" -print-sysroot)
nvcc --version | grep -F 'release 12.4,'
nvcc -ccbin "$compiler" -std=c++14 -arch=compute_75 -code=compute_75 --cudart=none +    -I"$sysroot/usr/include" "$root/examples/compute.cu" -L"$sysroot/usr/lib" +    -lcudart -lcudnn -o "$root/buildroot/board/cuda-distro/rootfs-overlay/usr/local/bin/compiled-cuda-demo"
