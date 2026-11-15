# License inventory and redistribution review

This is an inventory of intended components, not legal advice or proof of compliance. `make legal-info` has not completed here. Review its generated license files, source archives and manifest for the actual image before distribution. Buildroot legal-info may identify incomplete information; preserve and resolve its warnings.

| Component | License family / purpose |
|---|---|
| Buildroot | GPL-2.0-or-later build system; check pinned source COPYING |
| Linux | GPL-2.0 kernel; preserve corresponding-source obligations |
| BusyBox | GPL-2.0 userland; preserve corresponding-source obligations |
| glibc | LGPL family; review exact generated inventory |
| OpenRC | BSD-2-Clause init |
| Python/libffi | Python/PSF and libffi license; native API bridge |
| runc | Apache-2.0 OCI runtime and transitive dependencies |
| NVIDIA 550.127.05 | Proprietary driver agreement; kernel/userspace GPU support |
| CUDA cudart, cuBLAS, NVRTC | NVIDIA CUDA agreement; deployable components subject to exact redistribution terms |
| cuDNN 9.2.1.18 | NVIDIA cuDNN agreement; neural-network runtime |

Official sources: [CUDA agreement](https://docs.nvidia.com/cuda/eula/index.html), [cuDNN agreement](https://docs.nvidia.com/deeplearning/cudnn/sla/index.html), [driver download](https://download.nvidia.com/XFree86/Linux-x86_64/550.127.05/). Check the LICENSE shipped with each pinned artifact. The project makes no blanket claim that all components are freely redistributable or all require written permission.

After reviewing terms, a builder may explicitly set ACCEPT_NVIDIA_LICENSES=1. That flag is not a legal license grant. Packages use REDISTRIBUTE=NO to prevent a misleading unrestricted-source redistribution assumption. The wrapper downloads from official HTTPS sources and verifies pinned archive hashes. It does not automate account consent or bypass gated downloads; if terms or access change, stop and obtain the artifact legitimately. No proprietary binaries are included in this repaired source deliverable.
