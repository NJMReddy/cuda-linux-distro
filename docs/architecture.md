# Architecture

```mermaid
flowchart TD
  A[Pinned Buildroot source and BR2_EXTERNAL] --> B[Toolchain and custom Linux]
  A --> C[NVIDIA and CUDA runtime recipes]
  B --> D[ext4 root and Buildroot GRUB EFI]
  C --> D
  D --> E[genimage GPT disk]
  E --> F[UEFI / GRUB / Linux ro root]
  F --> G[OpenRC localmount]
  G --> H[cuda-writable overlays and sysctls]
  H --> I[GPU benchmark or explicit BLOCKED result]
  H --> J[Optional OCI CPU smoke]
```

Recipe presence is not installation evidence. GPT checks are not boot evidence. QEMU without passthrough is not GPU evidence. The x86_64 target uses ACPI/PCI enumeration, so no device tree is applicable.
