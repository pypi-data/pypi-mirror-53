/* Copyright (c) 2007-2019. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */
#include "src/kernel/activity/IoImpl.hpp"
#include "mc/mc.h"
#include "simgrid/Exception.hpp"
#include "simgrid/kernel/resource/Action.hpp"
#include "simgrid/s4u/Host.hpp"
#include "src/kernel/resource/DiskImpl.hpp"
#include "src/mc/mc_replay.hpp"
#include "src/simix/smx_private.hpp"
#include "src/surf/StorageImpl.hpp"

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(simix_io, simix, "Logging specific to SIMIX (io)");

void simcall_HANDLER_io_wait(smx_simcall_t simcall, simgrid::kernel::activity::IoImpl* synchro)
{
  XBT_DEBUG("Wait for execution of synchro %p, state %d", synchro, (int)synchro->state_);

  /* Associate this simcall to the synchro */
  synchro->register_simcall(simcall);

  if (MC_is_active() || MC_record_replay_is_active())
    synchro->state_ = SIMIX_DONE;

  /* If the synchro is already finished then perform the error handling */
  if (synchro->state_ != SIMIX_RUNNING)
    synchro->finish();
}

namespace simgrid {
namespace kernel {
namespace activity {

IoImpl& IoImpl::set_type(s4u::Io::OpType type)
{
  type_ = type;
  return *this;
}

IoImpl& IoImpl::set_size(sg_size_t size)
{
  size_ = size;
  return *this;
}

IoImpl& IoImpl::set_disk(resource::DiskImpl* disk)
{
  disk_ = disk;
  return *this;
}

IoImpl& IoImpl::set_storage(resource::StorageImpl* storage)
{
  storage_ = storage;
  return *this;
}

IoImpl* IoImpl::start()
{
  state_       = SIMIX_RUNNING;
  if (storage_)
    surf_action_ = storage_->io_start(size_, type_);
  else
    surf_action_ = disk_->io_start(size_, type_);
  surf_action_->set_activity(this);

  XBT_DEBUG("Create IO synchro %p %s", this, get_cname());
  IoImpl::on_start(*this);

  return this;
}

void IoImpl::post()
{
  performed_ioops_ = surf_action_->get_cost();
  if (surf_action_->get_state() == resource::Action::State::FAILED) {
    if ((storage_ && not storage_->is_on()) || (disk_ && not disk_->is_on()))
      state_ = SIMIX_FAILED;
    else
      state_ = SIMIX_CANCELED;
  } else if (surf_action_->get_state() == resource::Action::State::FINISHED) {
    state_ = SIMIX_DONE;
  }
  on_completion(*this);

  /* Answer all simcalls associated with the synchro */
  finish();
}

void IoImpl::finish()
{
  while (not simcalls_.empty()) {
    smx_simcall_t simcall = simcalls_.front();
    simcalls_.pop_front();
    switch (state_) {
      case SIMIX_DONE:
        /* do nothing, synchro done */
        break;
      case SIMIX_FAILED:
        simcall->issuer_->context_->iwannadie = true;
        simcall->issuer_->exception_ =
            std::make_exception_ptr(StorageFailureException(XBT_THROW_POINT, "Storage failed"));
        break;
      case SIMIX_CANCELED:
        simcall->issuer_->exception_ = std::make_exception_ptr(CancelException(XBT_THROW_POINT, "I/O Canceled"));
        break;
      default:
        xbt_die("Internal error in IoImpl::finish(): unexpected synchro state %d", static_cast<int>(state_));
    }

    simcall->issuer_->waiting_synchro = nullptr;
    simcall->issuer_->simcall_answer();
  }
}

/*************
 * Callbacks *
 *************/
xbt::signal<void(IoImpl const&)> IoImpl::on_start;
xbt::signal<void(IoImpl const&)> IoImpl::on_completion;

} // namespace activity
} // namespace kernel
} // namespace simgrid
