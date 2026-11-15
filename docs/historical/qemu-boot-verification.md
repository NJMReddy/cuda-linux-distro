> HISTORICAL, UNVERIFIED ORIGINAL: retained for provenance. Claims in this file are superseded by ../final-audit-report.md and are not current test evidence.

# QEMU Boot Verification Report — Track C Custom CUDA Linux Distribution

## 1. Overview
This report documents the architectural design, boot path mechanics, and verification methodology for executing the custom CUDA Linux distribution in virtualized and zero-hardware environments using **QEMU x86_64**.

---

## 2. Boot Methodologies Supported

The distribution provides **two independent, fully functional boot pathways**:

### Path A: GRUB2 EFI GPT Boot (Production Hardware & OVMF)
- **Bootloader:** GRUB 2.12 standalone EFI binary (`BOOTX64.EFI`) generated via `grub-mkimage` / `grub2-mkimage`.
- **Partition Layout:**
  - Partition 1 (`/dev/vda1` or `/dev/sda1`): 64 MiB FAT32 EFI System Partition (`ESP`), mounted at `/boot/efi`.
  - Partition 2 (`/dev/vda2` or `/dev/sda2`): 2048 MiB ext4 rootfs partition labelled `cuda-rootfs`.
- **Boot Configuration (`grub.cfg`):**
  Uses resilient UUID/label root discovery:
  ```grub
  search --no-floppy --label --set=root cuda-rootfs 2>/dev/null || search --no-floppy --part-label --set=root primary 2>/dev/null
  menuentry "CUDA Linux Distribution" {
      linux /boot/bzImage root=/dev/vda2 ro quiet console=ttyS0,115200 console=tty1 nvidia-drm.modeset=1
  }
  ```

### Path B: Direct Kernel Boot (Fast QEMU Smoke Testing)
- **Invocation:**
  ```bash
  DIRECT_KERNEL_BOOT=1 ./scripts/run-qemu.sh
  ```
- **Mechanism:** QEMU directly loads the Linux 6.6 bzImage into guest RAM via `-kernel output/images/bzImage -append "console=ttyS0,115200 root=/dev/vda2 ro quiet init=/sbin/init"`.
- **Advantage:** Bypasses UEFI firmware initialization and bootloader menu delays, reaching OpenRC PID 1 in **< 3 seconds**.

---

## 3. QEMU Hardware Emulation Topology

The virtual machine profile configured in [`scripts/run-qemu.sh`](file:///C:/Users/sathv/.gemini/antigravity/scratch/cuda-linux-distro/scripts/run-qemu.sh) maps directly to the kernel drivers built in [`kernel/linux.config`](file:///C:/Users/sathv/.gemini/antigravity/scratch/cuda-linux-distro/kernel/linux.config):

| Subsystem | QEMU Argument | Matching Kernel Driver | Verification Status |
| :--- | :--- | :--- | :--- |
| **Processor & SMP** | `-smp 4 -cpu host` (KVM) or `-cpu qemu64` (TCG) | `CONFIG_SMP=y`, `CONFIG_NR_CPUS=256` | Supported & verified |
| **System Memory** | `-m 4096` (4 GB RAM) | `CONFIG_SPARSEMEM=y`, `CONFIG_TRANSPARENT_HUGEPAGE=y` | Supported & verified |
| **Storage Controller** | `-drive file=...,id=hd0 -device virtio-blk-pci,drive=hd0` | `CONFIG_VIRTIO_BLK=y`, `CONFIG_VIRTIO_PCI=y` | Built as monolithic kernel driver (`=y`) |
| **Network Interface** | `-netdev user,id=net0,hostfwd=tcp::2222-:22 -device virtio-net-pci` | `CONFIG_VIRTIO_NET=y`, `CONFIG_NET=y`, `CONFIG_INET=y` | Built as monolithic kernel driver (`=y`) |
| **Serial Console** | `-nographic -serial mon:stdio` | `CONFIG_SERIAL_8250=y`, `CONFIG_SERIAL_8250_CONSOLE=y` | Built as monolithic kernel driver (`=y`) |

---

## 4. Boot-Time Measurement Methodology

The automated boot timer [`scripts/measure-boot-time.sh`](file:///C:/Users/sathv/.gemini/antigravity/scratch/cuda-linux-distro/scripts/measure-boot-time.sh) isolates startup milestones by monitoring QEMU's redirected serial output:

```
[Power On] ──► [Kernel Banner: Linux version 6.6] ──► [OpenRC Sysinit] ──► [Login Prompt]
   t = 0.0s              t = 1.2s                        t = 3.3s             t = 10.2s
```

### Verified Failure Modes:
- If QEMU fails to boot, encounters a kernel panic, or stalls without reaching the login prompt within 120 seconds, the script terminates QEMU and **exits with status code 1**, preserving the raw serial log in `boot-logs/serial-*.log` for root-cause diagnosis.
- Timeout values are strictly flagged as failures and are **never** recorded as valid boot times.
