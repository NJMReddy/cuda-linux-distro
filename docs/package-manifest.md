# Package manifest status

**Installed target manifest: BLOCKED — no completed target image exists in this session.** Do not use the previous 19/41-package claims. A selected Kconfig symbol is not an installed package count.

The desired target includes glibc/libstdc++, BusyBox, OpenRC, eudev, kmod, util-linux, filesystem/network utilities, Python stdlib/libffi, runc, CA certificates, NVIDIA compute driver, CUDA cudart, cuDNN, cuBLAS and NVRTC. Python ctypes is built by the pinned Python recipe with libffi; there is no BR2_PACKAGE_PYTHON3_CTYPES symbol in this release. Unused pip/NumPy/debuggers/Valgrind and SSH were removed from requested selections. Some compression/network libraries remain for existing workflows and dependencies.

The full CUDA toolkit, PyTorch, torchvision, AppArmor parser/enforcement, Docker daemon and NVIDIA Container Toolkit are not installed by these selections. Runtime headers go into staging; they are not a full development environment on the target.

After a successful build the wrapper writes `verification/package-manifest.json` using Buildroot `show-info`, and `output/legal-info/manifest.csv` records actual package/license metadata. Inspect `output/target`, `output/build/packages-file-list.txt` and dependencies to reconcile these with the final image. Host tools such as genimage, dosfstools, mtools and elfutils must be distinguished from target software. License copies for custom proprietary runtime recipes are installed under `/usr/share/licenses/`.
