# Evidence-based requirement gate

No marks or predicted score are assigned. PASS applies only to the tested scope in its row. Implementation presence does not establish enforcement.

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

Submission readiness: **NOT READY**. Full system and hardware verification, GPU container verification/full toolkit requirements, measurements and student video remain outstanding.
