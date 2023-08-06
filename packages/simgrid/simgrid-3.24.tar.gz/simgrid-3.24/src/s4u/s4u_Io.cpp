/* Copyright (c) 2018-2019. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "simgrid/s4u/Disk.hpp"
#include "simgrid/s4u/Io.hpp"
#include "simgrid/s4u/Storage.hpp"
#include "src/kernel/activity/IoImpl.hpp"
#include "xbt/log.h"

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(s4u_io, s4u_activity, "S4U asynchronous IOs");

namespace simgrid {
namespace s4u {

Io::Io(sg_disk_t disk, sg_size_t size, OpType type) : disk_(disk), size_(size), type_(type)
{
  Activity::set_remaining(size_);
  pimpl_ = kernel::activity::IoImplPtr(new kernel::activity::IoImpl());
}

Io::Io(sg_storage_t storage, sg_size_t size, OpType type) : storage_(storage), size_(size), type_(type)
{
  Activity::set_remaining(size_);
  pimpl_ = kernel::activity::IoImplPtr(new kernel::activity::IoImpl());
}

Io* Io::start()
{
  kernel::actor::simcall([this] {
    if (storage_) {
      (*boost::static_pointer_cast<kernel::activity::IoImpl>(pimpl_))
          .set_name(name_)
          .set_storage(storage_->get_impl())
          .set_size(size_)
          .set_type(type_)
          .start();
    } else {
      (*boost::static_pointer_cast<kernel::activity::IoImpl>(pimpl_))
          .set_name(name_)
          .set_disk(disk_->get_impl())
          .set_size(size_)
          .set_type(type_)
          .start();
    }
  });
  state_ = State::STARTED;
  return this;
}

Io* Io::cancel()
{
  simgrid::kernel::actor::simcall([this] { boost::static_pointer_cast<kernel::activity::IoImpl>(pimpl_)->cancel(); });
  state_ = State::CANCELED;
  return this;
}

Io* Io::wait()
{
  simcall_io_wait(pimpl_);
  state_ = State::FINISHED;
  return this;
}

Io* Io::wait_for(double)
{
  THROW_UNIMPLEMENTED;
}

bool Io::test()
{
  xbt_assert(state_ == State::INITED || state_ == State::STARTED || state_ == State::FINISHED);

  if (state_ == State::FINISHED)
    return true;

  if (state_ == State::INITED)
    this->start();

  THROW_UNIMPLEMENTED;

  // return false
}

/** @brief Returns the amount of flops that remain to be done */
double Io::get_remaining()
{
  return kernel::actor::simcall(
      [this]() { return boost::static_pointer_cast<kernel::activity::IoImpl>(pimpl_)->get_remaining(); });
}

sg_size_t Io::get_performed_ioops()
{
  return kernel::actor::simcall(
      [this]() { return boost::static_pointer_cast<kernel::activity::IoImpl>(pimpl_)->get_performed_ioops(); });
}

void intrusive_ptr_release(simgrid::s4u::Io* i)
{
  if (i->refcount_.fetch_sub(1, std::memory_order_release) == 1) {
    std::atomic_thread_fence(std::memory_order_acquire);
    delete i;
  }
}

void intrusive_ptr_add_ref(simgrid::s4u::Io* i)
{
  i->refcount_.fetch_add(1, std::memory_order_relaxed);
}
} // namespace s4u
} // namespace simgrid
