#ifndef TENSORFLOW_COMMON_RUNTIME_EPU_EPU_ALLOCATOR_H_
#define TENSORFLOW_COMMON_RUNTIME_EPU_EPU_ALLOCATOR_H_

#include "tensorflow/core/common_runtime/bfc_allocator.h"

namespace tensorflow {

  /* low-level sub-allocator which allocates the physical memory address of device */
  class EPUMemAllocator : public SubAllocator {
    public:
      EPUMemAllocator(void *base_addr, size_t mem_size)
        : SubAllocator({}, {}), base_addr_(base_addr), mem_size_(mem_size), offset_(0) {}
      ~EPUMemAllocator() override {}

      void* Alloc(size_t alignment, size_t num_bytes) override;
      void Free(void* ptr, size_t num_bytes) override {}

    private:
      void *base_addr_;
      size_t mem_size_;
      size_t offset_;

      TF_DISALLOW_COPY_AND_ASSIGN(EPUMemAllocator);
  };

  /* high-level allocator which wraps the BFCAllocator */
  class EPUAllocator : public Allocator {
    public:
      EPUAllocator(void *base_addr, size_t mem_size);
      ~EPUAllocator() override {}
      string Name() override { return "epu_allocator"; }

      void* AllocateRaw(size_t alignnment, size_t num_bytes) override;
      void* AllocateRaw(size_t alignnment, size_t num_bytes,
                        const AllocationAttributes& allocation_attr) override;
      void DeallocateRaw(void* ptr) override;

    private:
      mutable mutex mu_;
      BFCAllocator* bfc_allocator;

      TF_DISALLOW_COPY_AND_ASSIGN(EPUAllocator);
  };

}

#endif
