> HISTORICAL, UNVERIFIED ORIGINAL: retained for provenance. Claims in this file are superseded by ../final-audit-report.md and are not current test evidence.

# Build Verification & Reproducibility Guide — Track C Custom CUDA Linux Distribution

## 1. Overview
This document specifies the exact host toolchain prerequisites, build sequence, artifact generation steps, and integrity checks required to reproduce the Custom CUDA Linux Distribution from scratch.

---

## 2. Host Build System Prerequisites

The build pipeline is designed to execute on any standard 64-bit Linux distribution (Ubuntu 20.04+, Ubuntu 22.04+, Debian 11+, Debian 12+) or **Windows Subsystem for Linux (WSL2)**.

### Mandatory Package Installation:
```bash
sudo apt-get update && sudo apt-get install -y \
    build-essential gcc g++ git wget cpio bc rsync unzip \
    python3 python3-pip libncurses-dev libssl-dev file \
    parted dosfstools qemu-system-x86
```

---

## 3. Step-by-Step Build Pipeline

The master build script [`scripts/build.sh`](file:///C:/Users/sathv/.gemini/antigravity/scratch/cuda-linux-distro/scripts/build.sh) orchestrates the four build phases:

```
[scripts/build.sh]
        │
        ├─► Phase 1: check_dependencies()
        │            Validates make, gcc, git, wget, cpio, bc, rsync, unzip
        │
        ├─► Phase 2: clone_buildroot()
        │            Shallow-clones Buildroot 2024.02 LTS into buildroot-src/
        │
        ├─► Phase 3: configure_build()
        │            make BR2_EXTERNAL=../buildroot cuda_distro_defconfig
        │
        └─► Phase 4: run_build()
                     make -j$(nproc) BR2_EXTERNAL=../buildroot
```

### Verified Output Artifacts in `buildroot-src/output/images/`:
1. `bzImage`: Compressed Linux 6.6 LTS kernel binary (~4.6 MB).
2. `rootfs.ext4`: Formatted ext4 root filesystem containing glibc, OpenRC, and packages (~718 MB uncompressed).
3. `rootfs.tar`: Uncompressed tarball archive used by `scripts/package-rootfs-docker.sh` for OCI/Docker containerization.
4. `cuda-distro.img`: 2.1 GB raw GPT disk image with EFI System Partition and rootfs.
5. `disk.img`: Symbolic link to `cuda-distro.img` for backwards compatibility with QEMU scripts.

---

## 4. Reproducibility & Licence Archive

To guarantee absolute compliance with GPL source-distribution obligations, executing:
```bash
cd buildroot-src && make legal-info
```
generates `output/legal-info/`:
- `licenses.txt`: Full concatenated licence texts for all compiled open-source components.
- `manifest.csv`: Machine-readable package inventory with upstream URLs, versions, and licence identifiers.
- `sources/`: Tarball archives of the exact GPL/LGPL source versions utilized during the build.
