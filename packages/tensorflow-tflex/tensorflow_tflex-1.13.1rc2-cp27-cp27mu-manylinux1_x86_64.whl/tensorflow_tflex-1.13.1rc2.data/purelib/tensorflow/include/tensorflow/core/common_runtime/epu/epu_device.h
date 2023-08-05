#ifndef TENSORFLOW_CORE_COMMON_RUNTIME_EPU_EPU_DEVICE_H_
#define TENSORFLOW_CORE_COMMON_RUNTIME_EPU_EPU_DEVICE_H_

#include "tensorflow/core/common_runtime/device_factory.h"
#include "tensorflow/core/common_runtime/local_device.h"
#include "tensorflow/core/common_runtime/epu/epu_device_context.h"
#include "tensorflow/core/common_runtime/epu/epu_allocator.h"
#include "tensorflow/core/common_runtime/epu/epu.h"
#include "tensorflow/core/common_runtime/epu/epu_dnn.h"

namespace tensorflow {

// EPU device implementation.
class EPUDevice : public LocalDevice {
 public:
  EPUDevice(const SessionOptions& options, const string& name,
                   Bytes memory_limit, const DeviceLocality& locality,
                   Allocator* allocator,
                   EPUAllocator* epu_allocator,
                   EPUDeviceContext* ctx,
                   string description,
                   EPU *epu,
                   EPUDNN *dnn);
  ~EPUDevice() override;

  void Compute(OpKernel* op_kernel, OpKernelContext* context) override;
  Allocator* GetAllocator(AllocatorAttributes attr) override;
  Status FillContextMap(const Graph *graph, DeviceContextMap *device_context_map) override; 
  Status MakeTensorFromProto(const TensorProto& tensor_proto,
                             const AllocatorAttributes alloc_attrs,
                             Tensor* tensor) override;

  Status Sync() override { 
    get_dnn()->Sync();
    return Status::OK(); 
  }
   
  void memcpyH2D(void *dst, const void *src, size_t count); 
  void memcpyD2H(void *dst, const void *src, size_t count);

  EPUDNN *get_dnn() {
    return dnn_;
  }

  EPUAllocator *get_epu_allocator() {
    return epu_allocator_;
  }

 private:
  EPU *epu_;                           // not owned
  EPUDNN *dnn_;                        // not owned
  Allocator* allocator_;               // Not owned
  EPUAllocator* epu_allocator_;        // not owned
  EPUDeviceContext* device_context_;   // not owned

  void memcpy(void* dst, const void* src, size_t count, ::corex::MemcpyKind kind);
};

}  // namespace tensorflow

#endif  // TENSORFLOW_CORE_COMMON_RUNTIME_EPU_EPU_DEVICE_H_
