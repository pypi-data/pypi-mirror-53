#ifndef TENSORFLOW_COMMON_RUNTIME_EPU_EPU_DEVICE_FACTORY_H_
#define TENSORFLOW_COMMON_RUNTIME_EPU_EPU_DEVICE_FACTORY_H_

// Register a factory that provides EPU devices.
#include "tensorflow/core/common_runtime/epu/epu_device.h"

#include <vector>
#include "tensorflow/core/common_runtime/device_factory.h"
#include "tensorflow/core/framework/allocator.h"
#include "tensorflow/core/public/session_options.h"

namespace tensorflow {

class EPUDeviceFactory : public DeviceFactory {
 public:
  Status CreateDevices(const SessionOptions& options, const string& name_prefix,
                       std::vector<std::unique_ptr<Device>>* devices) override;
  ~EPUDeviceFactory();

 private:
  bool inited = false;
  int chipid[MAX_EPU_CHIP_NUM];
  Allocator* calloc;
  EPU* epu;
  EPUAllocator* ealloc[EPU_NUM];
  EPUDeviceContextCoreX* ctx[EPU_NUM];
  EPUDNN* dnn[EPU_NUM];
  string name[EPU_NUM];
};

}  // namespace tensorflow
#endif
