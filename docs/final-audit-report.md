# Final engineering audit — 2026-11-15

**Submission readiness: NOT READY.** This is a repaired source deliverable with honest validation boundaries, not a successfully rebuilt GPU Linux release. Critical build, image boot and hardware demonstrations remain blocked by the available environment. The full on-target CUDA development toolkit is not complete; manual OCI GPU device configuration is implemented but unverified.

## Scope and preservation

The supplied ZIP was copied into this workspace and repaired in place there; the OneDrive original is unchanged. No usable Git history was supplied. Existing buildroot external-tree layout, script entry points, original logs, useful kernel/input configurations and historical benchmark/documents are preserved. The custom NVIDIA package was necessarily renamed to avoid Buildroot's built-in package namespace. Original documents are archived under historical/ with explicit provenance warnings. No registry push, remote Git publication, destructive host operation or NVIDIA binary redistribution occurred.

## Defects and root causes repaired

1. **NVIDIA modules missing:** empty external.mk omitted all external package makefiles; including them exposed a collision with Buildroot's existing nvidia-driver. Add include rules, rename the custom package and use kernel-module infrastructure so Linux ordering/build/install are connected.
2. **gelf.h/libelf.h compilation failure:** historical objtool build lacked host ELF headers/libraries. Select Buildroot host elfutils via the Linux dependency option and add explicit compile/link host probes; do not disable objtool protections to hide the error.
3. **Unsupported toolchain requests:** GCC 14/binutils 2.43 did not belong to the pinned 2024.02 release. Resolve supported selections, pin Linux 6.6.18, and reject silently dropped requests with check-config.py.
4. **Invalid proprietary runtime URLs:** toolkit release version is not necessarily component archive version. Use NVIDIA's manifests for cudart 12.4.127, cuDNN archive 9.2.1.18, cuBLAS and NVRTC with official SHA-256 hashes. Preserve actual SONAME links and require files instead of silently skipping them. NVIDIA NVVM has its own 4.0.0 filename; derive driver library SONAME links from ELF metadata rather than assuming every library ends in the driver version or .so.1.
5. **Nonbootable-image false success:** previous loop-device fallback wrote only rootfs and left ESP empty; host grub commands could also be missing without failure. Replace this path with unprivileged genimage and required Buildroot-generated EFI/kernel/rootfs artifacts, fixed GPT PARTUUID and structure validation.
6. **QEMU launch/measurement defects:** wrong Windows image path, success on absent image, BIOS launch of EFI-only image, accelerator logs corrupting a captured value, duplicate serial endpoints and welcome-banner timing. Use explicit UEFI, one serial backend, real login detection, monotonic timing and critical-error scanning. Missing image/firmware fails nonzero.
7. **Overlay failure and writable root:** fstab mounted rw, tried /dev/root fsck, used systemd-only ordering and created upper/work dirs too late. Declare ro/noauto/pass=0, create upper/work after /run, mount native OpenRC overlays on /var and /usr/local before consumers, and expose actual mount tests.
8. **Benchmark dependency and false success:** target did not install PyTorch; CPU/fallback/probe results could be confused with computation. Replace target application with stdlib ctypes calls into native CUDA Driver API and embedded PTX, exact numerical verification and GPU event timing; preserve original PyTorch code as historical reference. Missing GPU is BLOCKED, never PASS; real application errors stay nonzero and synchronous service logs expose them.
9. **Security configuration not applied:** lock root, allow only explicitly provisioned console hash, omit SSH, apply sysctls from the startup dependency and test runtime controls. Do not claim uninstalled AppArmor draft enforcement or disable modules before NVIDIA loads.
10. **Container category error:** importing rootfs into host Docker does not install a guest runtime. Select runc and cgroups, add a real CPU OCI execution helper, keep host import separate and remove automatic pushes. A separate --gpu mode configures explicit NVIDIA device nodes and cgroup allowances for a trusted benchmark container; actual execution remains blocked.
11. **Unsupported evidence:** remove fabricated completion scores, contradictory image/boot/GPU results, hardcoded guide paths and claimed licensing percentages. Preserve originals, supply accurate current docs and a measured-input-only comparison tool.

## Actual verification

The executed command transcript with exit codes is `../verification/commands.json` and associated numbered `.log` files. Static structured output is `../verification/static-results.json`; Kconfig resolution is a Python evaluation of the pinned upstream sources, **not native Buildroot make or compilation**. Upstream release hashes and cudart archive contents were inspected. Seven failure-path regression tests were executed. Shell tree-sitter parsing and PowerShell parser checks are distinct from executing Linux shell scripts. The release gate intentionally exits nonzero while essential evidence is absent.

Environment: Windows / PowerShell / Python 3.14. WSL listing returns E_ACCESSDENIED. Git Bash fails MSYS object creation with access denied; the WindowsApps Bash alias is unusable by the verifier. A native Linux toolchain/build and QEMU binary/image are unavailable. No workaround claims a successful build. Historical serial logs show login alongside fsck/overlay/NVIDIA failures; they are not corrected runtime evidence.

## Requirement gate

| Requirement | Implementation | Test evidence | Status |
|---|---|---|---|
| Hardware, latency, power and footprint requirements | Targets and collection protocol in report | Source review; values clearly labeled targets | PASS |
| Justification versus stock Ubuntu | Explicit appliance/service-selection rationale | report.md reviewed; no assumed performance delta | PASS |
| Compare at least two build systems | Buildroot versus Yocto table and references | Documentation review | PASS |
| Custom kernel with necessary drivers | Existing config repaired, Linux pinned, host ELF dependency fixed | Kconfig input/source checks only; kernel compilation unavailable | BLOCKED |
| NVIDIA driver integration | Distinct recipe, kernel-module infrastructure, headless libs, runtime validator | Official metadata checked; module build/load unavailable | BLOCKED |
| CUDA runtime and cuDNN | Correct archive versions/hashes plus cuBLAS/NVRTC | cudart archive hash/content checked; target installation unavailable | BLOCKED |
| Full CUDA toolkit | Deployment runtime deliberately omits nvcc/full SDK | Not implemented as an on-target toolkit | NOT TESTED |
| Container runtime | runc selection, unified cgroups, real CPU smoke helper | Configuration resolves; actual OCI execution unavailable | BLOCKED |
| NVIDIA GPU container injection | Explicit devices/cgroup rules in container-smoke --gpu; no toolkit claim | No container GPU execution evidence | BLOCKED |
| Minimal justified userland | Removed undeclared framework/development/debug requests | Selection review; installed manifest unavailable | BLOCKED |
| Automatic application startup | Registered synchronous native OpenRC service | Shell parsed; real service execution unavailable | BLOCKED |
| Read-only root and writable overlay | Ordered runtime overlays and immutable etc/root | Syntax/order review; mount enforcement unavailable | BLOCKED |
| Three applied hardening controls | Secured account, no sshd, ro root, sysctls, kernel options | Implementation/source checks only; verify-runtime not executed on target | BLOCKED |
| Reproducible build scripts | Pinned source/versions/hashes, host probes, nonzero failures | Python Kconfig and source checks; clean repeated build unavailable | BLOCKED |
| Bootable image on QEMU/hardware | Rootless GPT/ESP assembly and EFI QEMU launcher | Negative image tests pass; no rebuilt image/boot | BLOCKED |
| End-to-end CUDA application | Driver API PTX vector addition and exact correctness | Missing-driver path returns 77; no GPU execution | BLOCKED |
| Stock/custom measurements | Strict matched-input comparator and collection protocol | Mismatched/missing data regression tests pass; no real datasets | NOT TESTED |
| At least 40% reduction or measured shortfall | Same-metric formula; old numbers withdrawn | No accepted stock/custom image measurements | NOT TESTED |
| Kernel final config/package/license manifest | Input config and generation commands provided | Actual generated final outputs await successful build | BLOCKED |
| Git repository | Local repository initialized, no commits or remote publication | git init and git status exit 0; original ZIP had no history | PASS |
| Final report/demo/team responsibilities | Updated report, four-member procedure, proposed roles | Documentation review, no fake contribution/video claims | PASS |
| Student video presentation | Students to produce separately | Not produced, as requested | NOT TESTED |

## Remaining work in priority order

1. Transfer the repaired source to a Linux filesystem under a working unprivileged Linux account. Install prerequisites, review vendor licenses, run clean build, fix any real compile/install failure, save final kernel configuration and legal-info. Non-cudart proprietary archive/license-file contents have not been locally extracted; resolve legal-info warnings and confirm exact files/ELF dependencies after acquisition.
2. Validate actual image structure and boot via firmware QEMU. Provision a private console password hash for authenticated inspection; locked-root default intentionally provides no interactive account. Run verify-runtime and rc-status, fix any ordering/service/permission issue, preserve serial evidence and volatile logs.
3. Boot actual supported NVIDIA hardware, run verify-gpu-stack, verify module vermagic/dependencies/userspace versions and numerical GPU results. Independently execute a cuDNN workload; vector-add does not prove cuDNN inference. Complete full toolkit integration if required by the instructor.
4. Run actual OCI CPU test, then run and validate `container-smoke --gpu` with its explicit NVIDIA device/library configuration. The manual OCI device path must pass numerical GPU verification before claiming GPU container support; no NVIDIA Container Toolkit integration is claimed.
5. Collect comparable Ubuntu 22.04 and custom image, RAM, kernel, package, power, latency and GPU measurements. Evaluate 40% using one explicit image metric; explain any measured shortfall without deleting required CUDA features.
6. Repeat clean builds under a fixed host environment, review generated manifests/licenses, confirm member contributions, commit/push to the team's authorized Git repository and create the student video.

## Deliverables and changed files

See [changes.md](changes.md) for every added/modified/removed file and purpose, generated against the original ZIP. Historical originals remain available. The deliverable contains source, corrected reports, test commands/logs and build/demo instructions; no fake images, fake CUDA outputs or fake video are included. No device tree is supplied for this x86_64 ACPI/PCI target.

## Executed check summary

Static checks: 63 PASS, 3 BLOCKED, 7 NOT TESTED, 0 FAIL. Seven failure-path unit tests passed. These counts do not count a blocked system build as a successful build.

| Executed check | Exit code | Interpretation |
|---|---|---|
| kconfig-python-resolution | 0 | PASS |
| requested-config-retained | 0 | PASS |
| static-regression | 0 | PASS |
| failure-path-tests | 0 | PASS |
| benchmark-no-driver | 77 | BLOCKED |
| release-gate-incomplete | 1 | PASS: correctly rejected incomplete release |
| wsl-environment | 4294967295 | BLOCKED |
| linux-build-host-check | 3221225794 | BLOCKED |
| qemu-windows-missing-image | 1 | PASS: correctly rejected absent image |
| corrected-word-guide | 0 | PASS |
