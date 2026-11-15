# Files changed against the supplied ZIP

The original ZIP is unchanged. Removed NVIDIA recipe paths are renamed/replaced under cuda-nvidia-driver; useful originals remain in docs/historical. Generated Python bytecode/cache is excluded from the deliverable. No source history was present in the ZIP.

| File | Change | Purpose |
|---|---|---|
| `.gitattributes` | ADDED | Ignore build/cache/secret artifacts and establish text line endings. |
| `.gitignore` | ADDED | Ignore build/cache/secret artifacts and establish text line endings. |
| `HOW_TO_VERIFY_AND_TEST_GUIDE.docx` | MODIFIED | Correct current instructions, evidence status or portable Word-guide generation. |
| `README.md` | MODIFIED | Correct current instructions, evidence status or portable Word-guide generation. |
| `build_guide.py` | MODIFIED | Correct current instructions, evidence status or portable Word-guide generation. |
| `buildroot/Config.in` | MODIFIED | Register distinct NVIDIA and runtime dependency packages. |
| `buildroot/board/cuda-distro/genimage.cfg` | ADDED | Apply root/security settings and create required GPT/EFI image without privileged mounts. |
| `buildroot/board/cuda-distro/grub.cfg` | ADDED | Apply root/security settings and create required GPT/EFI image without privileged mounts. |
| `buildroot/board/cuda-distro/post-build.sh` | MODIFIED | Apply root/security settings and create required GPT/EFI image without privileged mounts. |
| `buildroot/board/cuda-distro/post-image.sh` | MODIFIED | Apply root/security settings and create required GPT/EFI image without privileged mounts. |
| `buildroot/board/cuda-distro/rootfs-overlay/etc/init.d/S99cuda-benchmark` | MODIFIED | Genuine CUDA computation or ordered startup/runtime/OCI checks. |
| `buildroot/board/cuda-distro/rootfs-overlay/etc/init.d/cuda-writable` | ADDED | Genuine CUDA computation or ordered startup/runtime/OCI checks. |
| `buildroot/board/cuda-distro/rootfs-overlay/usr/local/bin/container-smoke` | ADDED | Genuine CUDA computation or ordered startup/runtime/OCI checks. |
| `buildroot/board/cuda-distro/rootfs-overlay/usr/local/bin/cuda-benchmark` | MODIFIED | Genuine CUDA computation or ordered startup/runtime/OCI checks. |
| `buildroot/board/cuda-distro/rootfs-overlay/usr/local/bin/verify-gpu-stack` | ADDED | Genuine CUDA computation or ordered startup/runtime/OCI checks. |
| `buildroot/board/cuda-distro/rootfs-overlay/usr/local/bin/verify-runtime` | ADDED | Genuine CUDA computation or ordered startup/runtime/OCI checks. |
| `buildroot/configs/cuda_distro_defconfig` | MODIFIED | Resolve supported pins/packages; ELF host dependency, secured account and image tools. |
| `buildroot/external.mk` | MODIFIED | Actually include external package recipes. |
| `buildroot/package/cublas-runtime/Config.in` | ADDED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/cublas-runtime/cublas-runtime.hash` | ADDED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/cublas-runtime/cublas-runtime.mk` | ADDED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/cuda-nvidia-driver/Config.in` | ADDED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/cuda-nvidia-driver/cuda-nvidia-driver.hash` | ADDED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/cuda-nvidia-driver/cuda-nvidia-driver.mk` | ADDED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/cuda-runtime/Config.in` | MODIFIED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/cuda-runtime/cuda-runtime.hash` | ADDED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/cuda-runtime/cuda-runtime.mk` | MODIFIED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/cudnn-runtime/Config.in` | MODIFIED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/cudnn-runtime/cudnn-runtime.hash` | ADDED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/cudnn-runtime/cudnn-runtime.mk` | MODIFIED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/nvidia-driver/Config.in` | REMOVED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/nvidia-driver/nvidia-driver.mk` | REMOVED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/nvrtc-runtime/Config.in` | ADDED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/nvrtc-runtime/nvrtc-runtime.hash` | ADDED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `buildroot/package/nvrtc-runtime/nvrtc-runtime.mk` | ADDED | Correct package namespace, upstream archives, dependencies, installs, SONAMEs or checksums. |
| `colab/cuda_benchmark.ipynb` | MODIFIED | Limit host-only GPU demo scope and remove prefilled output claims. |
| `docs/architecture.md` | MODIFIED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/build-verification.md` | MODIFIED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/cuda-benchmark-verification.md` | MODIFIED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/demo.md` | ADDED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/feature-regression-checklist.md` | MODIFIED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/final-audit-report.md` | MODIFIED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/historical/HOW_TO_VERIFY_AND_TEST_GUIDE.docx` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/README.md` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/architecture.md` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/build-verification.md` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/build_guide.py` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/cuda-benchmark-pytorch.py` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/cuda-benchmark-verification.md` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/cuda_benchmark.ipynb` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/feature-regression-checklist.md` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/final-audit-report.md` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/generate_guide_docx.py` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/kernel-size-report.md` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/package-manifest.md` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/qemu-boot-verification.md` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/repair-plan.md` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/report.md` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/historical/rubric-compliance.md` | ADDED | Preserve original drafts, code and evidence; label superseded claims. |
| `docs/licenses.md` | ADDED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/measurement-protocol.md` | ADDED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/package-manifest.md` | MODIFIED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/qemu-boot-verification.md` | MODIFIED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/references.md` | ADDED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/repair-plan.md` | MODIFIED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/report.md` | MODIFIED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `docs/rubric-compliance.md` | MODIFIED | Correct claims, document implementation, gaps, reproduction or evaluation. |
| `kernel/kernel-size-report.md` | MODIFIED | Correct boot/module/security input options and withdraw unsupported kernel measurements. |
| `kernel/linux.config` | MODIFIED | Correct boot/module/security input options and withdraw unsupported kernel measurements. |
| `scripts/build.sh` | MODIFIED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `scripts/check-config.py` | ADDED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `scripts/compare-distros.sh` | MODIFIED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `scripts/compare-metrics.py` | ADDED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `scripts/measure-boot-time.sh` | MODIFIED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `scripts/package-rootfs-docker.sh` | MODIFIED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `scripts/qemu-smoke.py` | ADDED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `scripts/run-qemu.ps1` | MODIFIED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `scripts/run-qemu.sh` | MODIFIED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `scripts/test-regressions.py` | ADDED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `scripts/validate-image.py` | ADDED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `scripts/verify-project.py` | ADDED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `scripts/verify-project.sh` | MODIFIED | Fail accurately, validate configuration/artifacts or test real versus unavailable behavior. |
| `security/apparmor-cuda-benchmark` | MODIFIED | Use runtime validation and stop claiming an uninstalled profile is enforced. |
| `security/hardening.sh` | MODIFIED | Use runtime validation and stop claiming an uninstalled profile is enforced. |
| `verification/01-kconfig-python-resolution.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/02-requested-config-retained.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/03-static-regression.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/04-failure-path-tests.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/05-benchmark-no-driver.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/06-release-gate-incomplete.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/07-wsl-environment.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/08-linux-build-host-check.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/09-qemu-windows-missing-image.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/10-corrected-word-guide.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/buildroot.kconfiglib.resolved.config` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/commands.json` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/git-status.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/guide-validation.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/no-driver-result.json` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/official-artifact-checks.json` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/original-archive-inventory.json` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/powershell-syntax.log` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `verification/static-results.json` | ADDED | Actual command/test output and source provenance; not runtime success evidence. |
| `docs/changes.md` | ADDED | This complete file-level change inventory. |
