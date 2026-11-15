#!/usr/bin/env bash
# Local import only. Packaging is not a runtime installed in the distro.
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
tarball="$ROOT/buildroot-src/output/images/rootfs.tar"
[[ -f $tarball ]] || { echo "Missing $tarball" >&2; exit 1; }
command -v docker >/dev/null || { echo 'BLOCKED: Docker unavailable' >&2; exit 1; }
docker import --change 'CMD ["/bin/sh"]' "$tarball" "${LOCAL_IMAGE:-cuda-distro:v1}"
echo 'Imported locally. Review proprietary licenses before sharing an image.'
