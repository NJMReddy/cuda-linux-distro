#!/bin/sh
# Validate applied runtime controls; never write into the build host's /etc.
set -eu
exec /usr/local/bin/verify-runtime
