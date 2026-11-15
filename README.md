# CUDA Linux Distribution — Track C

**Submission readiness: NOT READY.** Source repairs and static checks are available; no rebuilt image, corrected QEMU boot, NVIDIA hardware execution, cuDNN execution, or stock comparison has been verified in this session. See [final audit](docs/final-audit-report.md) and [report](docs/report.md).

Team: L. Shashank Reddy (CS24B1010), M. V. N. Sathvik (CS24B1034), N. Jagan Mohan Reddy (CS24B1038), B. Pardhu Yadav (CS24B1051).

This preserves the original Buildroot external tree. The compute driver has a distinct package name, `cuda-nvidia-driver`, to avoid Buildroot's existing legacy driver recipe. Target: x86_64 UEFI, OpenRC, glibc, Linux 6.6.18, NVIDIA 550.127.05. CUDA deployment libraries are included by recipe; the full CUDA compiler toolkit is **not** installed.

## Build and verify

On an unprivileged Ubuntu 22.04 Linux account, use a Linux filesystem (not a Windows mounted directory):

```sh
sudo apt update
sudo apt install build-essential wget cpio file bc rsync unzip python3 bison flex patch perl xz-utils bzip2 libelf-dev libssl-dev libncurses-dev qemu-system-x86 ovmf
chmod +x scripts/*.sh buildroot/board/cuda-distro/*.sh
bash scripts/build.sh --check-host
python3 scripts/verify-project.py
python3 scripts/test-regressions.py
# Review NVIDIA licenses first; this flag records your acknowledgement only.
ACCEPT_NVIDIA_LICENSES=1 bash scripts/build.sh
bash scripts/run-qemu.sh
bash scripts/measure-boot-time.sh
```

Root is locked by default and SSH is omitted. For interactive serial demonstration, first create a private SHA-512 crypt password hash file outside the repository (`openssl passwd -6 > /private/path/demo.hash`, then `chmod 600`). Export `CUDA_DEMO_PASSWORD_HASH_FILE=/private/path/demo.hash` for the build. Do not commit or redistribute this demo credential/image. This enables local console authentication; it does not enable SSH.

No binary image is supplied. Build outputs go to `buildroot-src/output/images/`; timestamped logs and resolved package information go to `verification/`. GPT/ESP checks do not prove boot success. Default QEMU uses UEFI firmware; direct kernel boot is explicitly a separate test.

[Demo procedure](docs/demo.md) · [licenses](docs/licenses.md) · [package selection](docs/package-manifest.md) · [measurements](docs/measurement-protocol.md)

## Evidence policy

PASS means actually executed and verified within its stated scope. FAIL means executed unsuccessfully. BLOCKED identifies an unavailable environment or dependency. NOT TESTED means no execution evidence exists. A successful static command does not imply release readiness; `--release` fails when required evidence is absent.

Earlier reports, guides and the PyTorch benchmark are preserved in `docs/historical/`. Their numerical results and completion claims are not accepted evidence. Original `build.log` and `boot-logs/serial-20261115-*.log` are unchanged historical failures. `boot-baseline.txt` has no accepted comparable baseline provenance.
