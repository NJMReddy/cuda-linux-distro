# Track C technical report

## Problem and requirements

Build a small, reproducible x86_64 Linux compute appliance around NVIDIA CUDA while separating implementation from measured operation. Track C is appropriate for controlled GPU numerical computation and eventual inference, not an assertion that every GPU or inference framework is supported.

Engineering targets (not measurements): x86_64 CPU with PCIe, a driver-supported NVIDIA GPU (Turing T4 or Ampere is a sensible validation target), 4 GiB system RAM for the QEMU baseline, at least 8 GiB storage for the generated image and working state; plan 16 GiB RAM and 50 GiB free Linux build storage. Exact NVIDIA GPU PCI IDs must be checked against the pinned driver. No sensors are required for vector addition. Measure GPU power with nvidia-smi on hardware; no power budget has been established. Target boot-to-login under 15 s, low idle RAM, and at least 40% reduction of a **stated comparable image metric**. These thresholds remain unverified. Vector addition measures memory throughput, not inference latency or matrix FLOPS.

Stock Ubuntu 22.04 is the comparison baseline because it is general purpose and offers a broad package environment. The appliance can explicitly select services and deploy immutable files; whether that saves 40% with cuDNN/cuBLAS included must be measured. Stock Ubuntu remains useful for the build host and supported CUDA development environment. No performance disadvantage is assumed without measurements.

## Build system choice

| Aspect | Buildroot | Yocto/OpenEmbedded |
|---|---|---|
| Model | Whole-system cross-build with Kconfig and package recipes | Layer/recipe based custom distribution tooling |
| Project fit | Existing BR2_EXTERNAL tree is small and reviewable | Better suited to more extensive product/BSP layering |
| Updates | Rebuild image; no assumption of apt package management | Can support package feeds and richer distribution policy |
| Tradeoff here | Preserve existing scripts and fixed image workflow | Migration would add scope and require new validation |

Keep Buildroot for this academic appliance. Neither choice guarantees smaller images or reproducible bytes on its own. See [references](references.md).

## Architecture and kernel

The [architecture diagram](architecture.md) shows UEFI → GRUB → custom Linux → OpenRC → writable-path service → synchronous GPU test. x86_64 discovers devices with ACPI/PCI; no device tree is required and no placeholder DTB is supplied.

Buildroot 2024.02 is pinned to a SHA-256 checked upstream archive, Linux to 6.6.18, and GCC to the supported 12.x selection (12.3.0 in this release). The old GCC 14/binutils 2.43 requests were unavailable in the chosen release. Existing kernel input is retained with boot-critical GPT/virtio/ext4/serial parents and module autoload corrected. It remains an input configuration, **not a newly generated or built final .config**. It still contains broader hardware support than a single known board needs. Resolve it through Linux olddefconfig, retain the generated final .config, then prune only against the actual hardware inventory. Kernel size, module count and boot deltas are unmeasured.

Historical build.log ends in host objtool errors for libelf.h/gelf.h. `BR2_LINUX_KERNEL_NEEDS_HOST_LIBELF=y` makes Buildroot build host elfutils before Linux. The build wrapper additionally compiles/links libelf and OpenSSL probes, reports missing utilities, preserves pipeline failures, and refuses to reuse unidentified source trees. Host dependency checks are prerequisites, not a replacement for rebuilding the kernel.

## NVIDIA, CUDA and cuDNN

The original empty external.mk never included custom recipes. Including them unchanged would collide with Buildroot's built-in NVIDIA 390.x package. The custom driver is therefore `cuda-nvidia-driver` / `BR2_PACKAGE_CUDA_NVIDIA_DRIVER`. Kernel-module infrastructure adds Linux ordering and module installation; headless userspace includes libcuda, NVML, PTX JIT components, nvidia-smi and nvidia-modprobe. The startup service loads nvidia/uvm and creates nodes through nvidia-modprobe. It does not bypass failures or enforce unsigned-module blocking.

NVIDIA's independent component versions are used: CUDA cudart 12.4.127, cuDNN archive 9.2.1.18, cuBLAS 12.4.5.8 and NVRTC 12.4.127. Official manifest hashes are pinned. Library copies preserve all vendor SONAME symlinks and fail when required files are missing. cuBLAS/NVRTC are included for cuDNN runtime dependencies. Actual ELF dependency closure, module vermagic/version consistency, hardware compatibility and cuDNN inference still need validation on the built target. Custom Buildroot/glibc is not represented as an NVIDIA-certified OS.

**Runtime versus toolkit:** nvcc and a complete CUDA SDK are not on the target. Runtime headers are staged for dependent builds. The vector-add application uses Python stdlib ctypes to call the native CUDA Driver API and JIT an embedded PTX kernel, requiring no PyTorch, NumPy or nvcc. It allocates GPU memory, copies inputs, runs warmups, times repeated GPU launches using CUDA events, copies results back and verifies every element. JSON and console output identify device, driver API version, timing scope and effective memory GB/s. Exit 77 means unavailable hardware/driver, 1 means failure and 0 means checked computation. CUDA event time excludes allocation, JIT and host copies; it is not end-to-end application latency. The previous PyTorch GEMM/ResNet code remains historical reference only.

Under GPU-less QEMU startup writes a BLOCKED result and permits the OS to boot. This is not successful CUDA execution. A detected NVIDIA device followed by a module/driver/application error fails visibly. The full toolkit requirement is not complete; the deployment-only decision must be accepted by the instructor or a supported development toolkit integration must be added and verified.

## Filesystems and security

Root boots ro and fstab declares ro,noauto with fsck pass 0, avoiding the historical /dev/root fsck error and OpenRC rw remount. A native OpenRC `cuda-writable` service needs localmount, creates tmpfs-backed upper/work directories at runtime, and mounts overlays on /var and /usr/local before consumers. /tmp and /run are tmpfs, /etc remains immutable, and resolver writes use /run/resolv.conf. Volatile logs and overlay changes do not survive reboot; copy logs out before shutdown. No persistent writable partition is implemented. Mount errors propagate.

Hardening implementation: secured root account (locked by default, optional private console hash), no SSH server, read-only root with selected writable paths, sysctl ASLR/kernel pointer/dmesg restrictions, and kernel stack/KASLR options. `verify-runtime` checks actual mounts, writes to /var, account state and live sysctls. These controls require runtime evidence before being marked enforced. The benchmark currently runs as root because module/device setup is privileged; least-privilege application separation remains future work. AppArmor profile is retained as an **uninstalled, unverified draft**, not counted as enforced hardening. No `modules_disabled=1` setting blocks NVIDIA initialization.

## Containers

runc is selected as a small OCI runtime and relevant namespace/cgroup/seccomp/overlay kernel inputs are present. `container-smoke` creates a bundle and attempts a real CPU container with read-only userspace binds, uid/gid 65534, no capabilities and no new privileges. Capture its real output before claiming container support. Docker rootfs import is a separate optional host packaging operation, with no automatic registry push. `container-smoke --gpu` configures explicit NVIDIA character-device nodes and cgroup device access with the target userspace libraries mounted read-only, then runs the same numerical benchmark inside runc. This manual OCI path is for trusted workloads, uses container uid 0 with no capabilities, disables JIT disk caching, and still requires real hardware verification. It is not NVIDIA Container Toolkit, and runc supplies no image registry or Docker daemon. Actual CPU and GPU container execution remain BLOCKED.

## Image, build and verification

genimage uses Buildroot host tools to build GPT with a 64 MiB ESP and the actual rootfs image length. It consumes the Buildroot-built EFI binary, copies board grub.cfg, and requires kernel/rootfs/EFI artifacts; no loop mounts or blank-ESP success fallback remain. Root partition has a fixed PARTUUID so kernel root discovery works without initramfs label resolution. A Python validator checks GPT primary/backup CRCs, bounds, EFI fallback file/PE signatures and ext magic; these are structure checks, not proof that firmware executes it.

Follow README for build prerequisites. Default QEMU requires non-Secure-Boot OVMF; direct kernel boot is explicitly separate. The smoke runner waits for the actual `cuda-distro login:` prompt, saves serial output and rejects critical boot errors. Login alone leaves runtime controls unverified. Run verify-runtime after authenticated console login. No new build or QEMU result exists in this Windows environment: WSL reports E_ACCESSDENIED, Git Bash fails creating its MSYS shared object, and QEMU is unavailable. See verification logs for actual executed checks and [final audit](final-audit-report.md).

## Evaluation and reproducibility limits

No accepted stock/custom numerical measurements are available. Earlier 3,200/1,450 MB disk claims conflict with the old 2 GiB root plus 64 MiB ESP configuration (approximately 2,116 MiB raw including overhead), and other reports claimed 412 MB compressed and different boot/GPU figures without matching raw evidence. Those claims are withdrawn, not adjusted into substitute measurements. New root capacity is deliberately 4 GiB to allow GPU dependencies; logical allocation is not used filesystem space. The 40% criterion has NOT TESTED status.

[Measurement protocol](measurement-protocol.md) distinguishes raw logical, allocated, compressed and used rootfs bytes. Reduction = (stock − custom) / stock × 100 using the same metric and matched hardware/stack. No estimates are inserted by compare-distros.sh. If the target is missed, inspect Buildroot size reports and remove only demonstrated unnecessary packages; retaining required GPU libraries takes precedence over a favorable percentage.

Pins/checksums and explicit dependencies improve source reproducibility. A clean full rebuild, toolchain output comparison and bit-for-bit reproducibility have not been demonstrated. Build host packages are not container-pinned. Old upstream versions are preserved for project compatibility; no claim of production security maintenance is made.

## Licensing, team and demonstration

See [license inventory](licenses.md). No NVIDIA binary, license secret or bootable image is redistributed here; review each agreement and collect `make legal-info` before sharing binaries. Actual license inventory requires a completed build. Original ZIP has no usable Git history; the repaired snapshot must be committed/pushed to the team's authorized repository. No remote publishing was performed.

Proposed responsibilities (not fabricated contributions): Shashank — build/kernel and resolved configs; Sathvik — image/QEMU/filesystem evidence; Jagan — NVIDIA/CUDA/cuDNN tests and metrics; Pardhu — security/container checks, report and presentation. Team members must confirm actual contributions. [Demo](demo.md) assigns executable steps. Video remains for students to create; none was produced.
