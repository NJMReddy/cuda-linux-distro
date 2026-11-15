# Runtime binaries; SDK headers go to staging only. No nvcc on the target.
CUDNN_RUNTIME_VERSION = 9.2.1.18
CUDNN_RUNTIME_SITE = https://developer.download.nvidia.com/compute/cudnn/redist/cudnn/linux-x86_64
CUDNN_RUNTIME_SOURCE = cudnn-linux-x86_64-9.2.1.18_cuda12-archive.tar.xz
CUDNN_RUNTIME_LICENSE = NVIDIA proprietary license
CUDNN_RUNTIME_LICENSE_FILES = LICENSE
CUDNN_RUNTIME_REDISTRIBUTE = NO
CUDNN_RUNTIME_DEPENDENCIES = cuda-runtime cublas-runtime nvrtc-runtime
CUDNN_RUNTIME_INSTALL_STAGING = YES

define CUDNN_RUNTIME_INSTALL_STAGING_CMDS
	$(INSTALL) -d $(STAGING_DIR)/usr/include $(STAGING_DIR)/usr/lib
	cp -a $(@D)/include/. $(STAGING_DIR)/usr/include/
	test -f $(@D)/lib/libcudnn.so.9
	cp -a $(@D)/lib/libcudnn*.so* $(STAGING_DIR)/usr/lib/
endef

define CUDNN_RUNTIME_INSTALL_TARGET_CMDS
	$(INSTALL) -d $(TARGET_DIR)/usr/lib
	test -f $(@D)/lib/libcudnn.so.9
	cp -a $(@D)/lib/libcudnn*.so* $(TARGET_DIR)/usr/lib/
	$(INSTALL) -D -m 0644 $(@D)/LICENSE $(TARGET_DIR)/usr/share/licenses/cudnn-runtime/LICENSE
endef

$(eval $(generic-package))
