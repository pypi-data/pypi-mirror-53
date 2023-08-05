#ifndef __EPU_HPP_
#define __EPU_HPP_

#include <vector>
#include <stdexcept>
#include <cassert>

#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>

#include <sys/types.h>
#include <sys/stat.h>

#include "tensorflow/core/platform/mutex.h"
#include "tensorflow/core/platform/logging.h"

#define PRINT_DEBUG_INFO TF_PREDICT_FALSE(VLOG_IS_ON(1))

#define MAX_EPU_CHIP_NUM 16

#define EPU_NUM          2

#define EPU_MEM_BASE     0x200000000
#define EPU0_MEM_BASE    0x201000000
#define EPU0_MEM_SIZE    0x070000000
#define EPU1_MEM_BASE    0x271000000
#define EPU1_MEM_SIZE    0x070000000

#define EPU0_REG_BASE    0x00200000
#define EPU1_REG_BASE    0x00300000

#define EPU_MP_DONE_REG  0x20C
#define EPU_MP_CLR_REG   0x210
#define EPU_DONE_O_REG   0x130
#define EPU_DONE_O_MASK  (1 << 24)

#define EPU_RST_REG      0x40300
#define EPU0_RST_VAL1    0xFFBF
#define EPU0_RST_VAL2    0xFFFF
#define EPU1_RST_VAL1    0xFF7F
#define EPU1_RST_VAL2    0xFFFF

#define EPU0_BUSY        0
#define EPU1_BUSY        1
#define H2D_BUSY         2
#define D2H_BUSY         3
#define EPU_BUSY_MASK    0x3
#define DMA_BUSY_MASK    0xC

#define WAIT_DONE_TIMEOUT_LOOPS 1000000
#define WAIT_EPU_INTERVAL_SECS  1

using namespace std;


class EPU {
public:
    EPU(int chipid);
    ~EPU(void);

    void reg_write(off_t target, uint32_t writeval);

    uint32_t reg_read(off_t target);

    // Memcpy H2D & D2H
    void memcpyH2D(void* dest, const void* source, size_t count);

    void memcpyD2H(void* dest, const void* source, size_t count);

    void reset(int index);

    void clear_done_status(int index);

    int read_done_status(int index);

private:
    //string get_file_content(string path);
    //bool find_epu_path(string vendor_id, string device_id, string& found_path);
    int file_open(const char *file_name, int timeout);
    int mmap_open(const char *file_name, void **base, uint32_t size);
    void file_close(int fd);
    void mmap_close(int fd, void *base, uint32_t size);

    mutable tensorflow::mutex dma_mu_;
    mutable tensorflow::mutex rst_mu_;
    mutable tensorflow::mutex clr_mu_;
    mutable tensorflow::mutex rdr_mu_;
    mutable tensorflow::mutex wrr_mu_;

    void* _mem_base;
    void* _reg_base;
    void* _iatu_base;
    int _mem_fd = -1;
    int _reg_fd = -1;
    int _iatu_fd = -1;
    int _ctrl_fd = -1;
    int _conf_fd = -1;
};

#endif // __EPU_HPP_
