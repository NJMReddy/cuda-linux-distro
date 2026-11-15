# Primary references used for repairs

- [Buildroot manual](https://buildroot.org/downloads/manual/manual.html): BR2_EXTERNAL, package/kernel-module infrastructure, legal-info, reproducibility limits.
- [Pinned Buildroot 2024.02 sources](https://buildroot.org/downloads/buildroot-2024.02.tar.xz): actual Config.in, Linux host elfutils dependency, OpenRC skeleton and package recipes were inspected.
- [Yocto introduction](https://docs.yoctoproject.org/overview-manual/yp-intro.html): layer-based custom Linux tooling.
- [CUDA 12.4.1 manifest](https://developer.download.nvidia.com/compute/cuda/redist/redistrib_12.4.1.json): exact independent component archive versions and SHA-256 values.
- [cuDNN 9.2.1 manifest](https://developer.download.nvidia.com/compute/cudnn/redist/redistrib_9.2.1.json): archive 9.2.1.18 and CUDA 12 variant hash.
- [Driver 550.127.05 checksum](https://download.nvidia.com/XFree86/Linux-x86_64/550.127.05/NVIDIA-Linux-x86_64-550.127.05.run.sha256sum).
- [CUDA release notes](https://docs.nvidia.com/cuda/archive/12.4.1/cuda-toolkit-release-notes/index.html): components and driver requirements.
- [cuDNN support matrix](https://docs.nvidia.com/deeplearning/cudnn/backend/v9.2.1/reference/support-matrix.html): CUDA 12.4 supported; Linux driver floor listed as 525.60.13. This does not certify a custom Buildroot OS or prove correct execution.
- [OpenRC root service](https://github.com/OpenRC/openrc/blob/0.52.1/init.d/root.in): ro fstab behavior; inspected to fix remount ordering.

- [NVIDIA 550 installed components](https://download.nvidia.com/XFree86/Linux-x86_64/550.127.05/README/installedcomponents.html): NVVM uses an independent 4.0.0 filename; other headless driver libraries were checked against this list.
