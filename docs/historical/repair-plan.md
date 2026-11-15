> HISTORICAL, UNVERIFIED ORIGINAL: retained for provenance. Claims in this file are superseded by ../final-audit-report.md and are not current test evidence.

# Repair Plan — Track C Custom CUDA Linux Distribution

This document details all defects, inconsistencies, syntax errors, and missing prerequisites identified across the repository during Phase 0 discovery, alongside their exact technical corrections.

---

## 1. Buildroot External Tree & Package Recipes (Phase 1)

### Defect 1.1: Invalid `mainmenu` Directive in `buildroot/Config.in`
- **Location:** `buildroot/Config.in:1`
- **Issue:** An external tree's `Config.in` is included within the top-level Buildroot Kconfig menu. Specifying `mainmenu "Custom CUDA Linux Distribution"` is illegal or ignored by Buildroot because Buildroot defines its own `mainmenu "Buildroot $BR2_VERSION Configuration"`.
- **Correction:** Remove `mainmenu` from `buildroot/Config.in`, keeping only the menu and package sources.

### Defect 1.2: Duplicate `NVIDIA_DRIVER_EXTRACT_CMDS` in `nvidia-driver.mk`
- **Location:** `buildroot/package/nvidia-driver/nvidia-driver.mk:15-22`
- **Issue:** `NVIDIA_DRIVER_EXTRACT_CMDS` is assigned twice in succession (first with `=` line 15, then with `define ... endef` line 18).
- **Correction:** Remove the first assignment and keep the clean `define NVIDIA_DRIVER_EXTRACT_CMDS` block using `$(SHELL) $(DL_DIR)/$(NVIDIA_DRIVER_SOURCE) --extract-only --target $(@D)/nvidia-extracted`.

### Defect 1.3: Architecture Variable Inconsistency in `nvidia-driver.mk`
- **Location:** `buildroot/package/nvidia-driver/nvidia-driver.mk:33`
- **Issue:** Kernel module compilation uses `ARCH=$(KERNEL_ARCH)`, whereas standard Buildroot variable for kernel architecture is `ARCH=$(KERNEL_ARCH)` or `ARCH=x86_64` (and `KERNEL_ARCH` is not always exported unless using kernel-module infrastructure).
- **Correction:** Set `ARCH=x86_64` explicitly and point `SYSSRC="$(LINUX_DIR)"` with `IGNORE_PREEMPT_RT_PRESENCE=1` to guarantee smooth out-of-tree NVIDIA compilation.

### Defect 1.4: Missing Directory Creation in `cuda-runtime.mk` and `cudnn-runtime.mk`
- **Location:** `buildroot/package/cuda-runtime/cuda-runtime.mk:72`, `buildroot/package/cudnn-runtime/cudnn-runtime.mk:93`
- **Issue:** Scripts write directly to `$(TARGET_DIR)/etc/ld.so.conf.d/*.conf` without first running `$(INSTALL) -d $(TARGET_DIR)/etc/ld.so.conf.d`. If that directory does not exist, build fails.
- **Correction:** Add `$(INSTALL) -d $(TARGET_DIR)/etc/ld.so.conf.d` before redirecting configuration files.

### Defect 1.5: Missing `BR2_TARGET_ROOTFS_TAR` in `cuda_distro_defconfig`
- **Location:** `buildroot/configs/cuda_distro_defconfig`
- **Issue:** `scripts/package-rootfs-docker.sh` explicitly expects `output/images/rootfs.tar`, but `cuda_distro_defconfig` only had `BR2_TARGET_ROOTFS_EXT2=y`.
- **Correction:** Add `BR2_TARGET_ROOTFS_TAR=y` and `BR2_TARGET_ROOTFS_TAR_ZSTD=y` to `cuda_distro_defconfig`.

---

## 2. Kernel Configuration (Phase 2)

### Defect 2.1: Conflicting Open-Source Nouveau Driver
- **Location:** `kernel/linux.config:445`
- **Issue:** `CONFIG_DRM_NOUVEAU=m` is enabled. Nouveau directly conflicts with the out-of-tree proprietary `nvidia.ko` module by claiming PCI IDs during boot.
- **Correction:** Disable Nouveau (`CONFIG_DRM_NOUVEAU=n`, `# CONFIG_DRM_NOUVEAU is not set`) to avoid module binding races on GPU hardware.

### Defect 2.2: Missing AppArmor Kernel Subsystem
- **Location:** `kernel/linux.config:563-578`
- **Issue:** Security scripts install AppArmor profiles, but `CONFIG_SECURITY_APPARMOR` and `CONFIG_DEFAULT_SECURITY_APPARMOR` were not configured in `kernel/linux.config`.
- **Correction:** Add `CONFIG_SECURITY_APPARMOR=y`, `CONFIG_SECURITY_APPARMOR_HASH=y`, `CONFIG_SECURITY_APPARMOR_HASH_DEFAULT=y`, and update LSM ordering `CONFIG_LSM="lockdown,yama,loadpin,safesetid,integrity,apparmor,bpf"`.

---

## 3. Disk Image, QEMU & Scripts Consistency (Phase 3)

### Defect 3.1: Disk Image Filename Inconsistency
- **Location:** `buildroot/board/cuda-distro/post-image.sh:18` vs `scripts/run-qemu.sh:10` & `scripts/measure-boot-time.sh:10`
- **Issue:** `post-image.sh` created `cuda-distro.img`, while `run-qemu.sh` and `measure-boot-time.sh` looked for `disk.img`.
- **Correction:** Standardize on `cuda-distro.img` across all scripts, and create a symlink `disk.img -> cuda-distro.img` in `post-image.sh` for universal backwards compatibility.

### Defect 3.2: GRUB Root Device Assumption
- **Location:** `buildroot/board/cuda-distro/post-image.sh:87`
- **Issue:** `grub.cfg` hardcoded `root=/dev/sda2`, which fails when QEMU attaches the drive as virtio-blk (`/dev/vda2`).
- **Correction:** Use filesystem label `root=LABEL=cuda-rootfs` and support both `/dev/vda2` and `/dev/sda2` fallbacks.

### Defect 3.3: Boot Timer Timeout Masking
- **Location:** `scripts/measure-boot-time.sh:93-97`
- **Issue:** When the boot timed out without reaching login prompt, the script reported `login_ms = 120000 ms` as a valid measurement.
- **Correction:** If the prompt is not found, output an explicit error message, record the failure, and exit with status code 1.

---

## 4. Benchmark Scripts, Paths & Security Profiles (Phases 4 & 5)

### Defect 4.1: Benchmark Path Mismatch
- **Location:** Binary located at `/usr/local/bin/cuda-benchmark`, but AppArmor profile specified `/usr/bin/cuda-benchmark`, and OpenRC script used `/usr/local/bin/cuda-benchmark`.
- **Correction:** Maintain the primary binary at `/usr/local/bin/cuda-benchmark`, install a symbolic link `/usr/bin/cuda-benchmark -> /usr/local/bin/cuda-benchmark` in `post-build.sh`, and update the AppArmor profile to cover both paths.

### Defect 4.2: AppArmor Profile Write Restriction for JSON Results
- **Location:** `security/apparmor-cuda-benchmark:89`
- **Issue:** Profile only allowed writing to `/var/log/cuda-benchmark.log`, while `S99cuda-benchmark` and `cuda-benchmark` write JSON reports to `/var/log/cuda-benchmark/results.json`.
- **Correction:** Add `/var/log/cuda-benchmark/` and `/var/log/cuda-benchmark/** rw,` to `security/apparmor-cuda-benchmark`.

### Defect 4.3: Python Benchmark GPU Absence Handling
- **Location:** `buildroot/board/cuda-distro/rootfs-overlay/usr/local/bin/cuda-benchmark`
- **Issue:** When run in QEMU (no NVIDIA GPU), benchmark printed an error but returned exit code 0 or failed unhandled if parameters were missing.
- **Correction:** Return clean structured JSON with status `"SKIPPED_NO_GPU"` when running on CPU-only/QEMU systems, allowing tests to distinguish intentional skips from genuine script crashes.

---

## 5. Verification Framework (Phase 7)
- **Addition:** Create `scripts/verify-project.sh` to run automated syntax, configuration, path, and security checks across the repository.
