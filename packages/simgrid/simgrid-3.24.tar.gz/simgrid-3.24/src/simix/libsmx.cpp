/* libsmx.c - public interface to simix                                       */
/* --------                                                                   */
/* These functions are the only ones that are visible from the higher levels  */
/* (most of them simply add some documentation to the generated simcall body) */
/*                                                                            */
/* This is somehow the "libc" of SimGrid                                      */

/* Copyright (c) 2010-2019. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "mc/mc.h"
#include "simgrid/simix/blocking_simcall.hpp"
#include "src/kernel/activity/CommImpl.hpp"
#include "src/kernel/activity/ConditionVariableImpl.hpp"
#include "src/kernel/activity/ExecImpl.hpp"
#include "src/kernel/activity/IoImpl.hpp"
#include "src/kernel/activity/MailboxImpl.hpp"
#include "src/kernel/activity/MutexImpl.hpp"
#include "src/mc/mc_replay.hpp"
#include "src/plugins/vm/VirtualMachineImpl.hpp"

#include "popping_bodies.cpp"

/**
 * @ingroup simix_host_management
 * @brief Waits for the completion of an execution synchro and destroy it.
 *
 * @param execution The execution synchro
 */
e_smx_state_t simcall_execution_wait(const smx_activity_t& execution)
{
  return (e_smx_state_t)simcall_BODY_execution_wait(static_cast<simgrid::kernel::activity::ExecImpl*>(execution.get()));
}

bool simcall_execution_test(const smx_activity_t& execution)
{
  return simcall_BODY_execution_test(static_cast<simgrid::kernel::activity::ExecImpl*>(execution.get()));
}

unsigned int simcall_execution_waitany_for(simgrid::kernel::activity::ExecImpl* execs[], size_t count, double timeout)
{
  return simcall_BODY_execution_waitany_for(execs, count, timeout);
}

void simcall_process_join(smx_actor_t process, double timeout)
{
  SIMIX_process_self()->join(process, timeout);
}

void simcall_process_suspend(smx_actor_t process)
{
  process->iface()->suspend();
}

e_smx_state_t simcall_process_sleep(double duration)
{
  SIMIX_process_self()->sleep(duration);
  return SIMIX_DONE;
}

/**
 * @ingroup simix_comm_management
 */
void simcall_comm_send(smx_actor_t sender, smx_mailbox_t mbox, double task_size, double rate, void* src_buff,
                       size_t src_buff_size, int (*match_fun)(void*, void*, simgrid::kernel::activity::CommImpl*),
                       void (*copy_data_fun)(simgrid::kernel::activity::CommImpl*, void*, size_t), void* data,
                       double timeout)
{
  /* checking for infinite values */
  xbt_assert(std::isfinite(task_size), "task_size is not finite!");
  xbt_assert(std::isfinite(rate), "rate is not finite!");
  xbt_assert(std::isfinite(timeout), "timeout is not finite!");

  xbt_assert(mbox, "No rendez-vous point defined for send");

  if (MC_is_active() || MC_record_replay_is_active()) {
    /* the model-checker wants two separate simcalls */
    smx_activity_t comm = nullptr; /* MC needs the comm to be set to nullptr during the simcall */
    comm = simcall_comm_isend(sender, mbox, task_size, rate,
        src_buff, src_buff_size, match_fun, nullptr, copy_data_fun, data, 0);
    simcall_comm_wait(comm, timeout);
    comm = nullptr;
  }
  else {
    simcall_BODY_comm_send(sender, mbox, task_size, rate, static_cast<unsigned char*>(src_buff), src_buff_size,
                           match_fun, copy_data_fun, data, timeout);
  }
}

/**
 * @ingroup simix_comm_management
 */
smx_activity_t simcall_comm_isend(smx_actor_t sender, smx_mailbox_t mbox, double task_size, double rate, void* src_buff,
                                  size_t src_buff_size,
                                  int (*match_fun)(void*, void*, simgrid::kernel::activity::CommImpl*),
                                  void (*clean_fun)(void*),
                                  void (*copy_data_fun)(simgrid::kernel::activity::CommImpl*, void*, size_t),
                                  void* data, bool detached)
{
  /* checking for infinite values */
  xbt_assert(std::isfinite(task_size), "task_size is not finite!");
  xbt_assert(std::isfinite(rate), "rate is not finite!");

  xbt_assert(mbox, "No rendez-vous point defined for isend");

  return simcall_BODY_comm_isend(sender, mbox, task_size, rate, static_cast<unsigned char*>(src_buff), src_buff_size,
                                 match_fun, clean_fun, copy_data_fun, data, detached);
}

/**
 * @ingroup simix_comm_management
 */
void simcall_comm_recv(smx_actor_t receiver, smx_mailbox_t mbox, void* dst_buff, size_t* dst_buff_size,
                       int (*match_fun)(void*, void*, simgrid::kernel::activity::CommImpl*),
                       void (*copy_data_fun)(simgrid::kernel::activity::CommImpl*, void*, size_t), void* data,
                       double timeout, double rate)
{
  xbt_assert(std::isfinite(timeout), "timeout is not finite!");
  xbt_assert(mbox, "No rendez-vous point defined for recv");

  if (MC_is_active() || MC_record_replay_is_active()) {
    /* the model-checker wants two separate simcalls */
    smx_activity_t comm = nullptr; /* MC needs the comm to be set to nullptr during the simcall */
    comm = simcall_comm_irecv(receiver, mbox, dst_buff, dst_buff_size,
                              match_fun, copy_data_fun, data, rate);
    simcall_comm_wait(comm, timeout);
    comm = nullptr;
  }
  else {
    simcall_BODY_comm_recv(receiver, mbox, static_cast<unsigned char*>(dst_buff), dst_buff_size, match_fun,
                           copy_data_fun, data, timeout, rate);
  }
}
/**
 * @ingroup simix_comm_management
 */
smx_activity_t simcall_comm_irecv(smx_actor_t receiver, smx_mailbox_t mbox, void* dst_buff, size_t* dst_buff_size,
                                  int (*match_fun)(void*, void*, simgrid::kernel::activity::CommImpl*),
                                  void (*copy_data_fun)(simgrid::kernel::activity::CommImpl*, void*, size_t),
                                  void* data, double rate)
{
  xbt_assert(mbox, "No rendez-vous point defined for irecv");

  return simcall_BODY_comm_irecv(receiver, mbox, static_cast<unsigned char*>(dst_buff), dst_buff_size, match_fun,
                                 copy_data_fun, data, rate);
}

/**
 * @ingroup simix_comm_management
 */
smx_activity_t simcall_comm_iprobe(smx_mailbox_t mbox, int type,
                                   int (*match_fun)(void*, void*, simgrid::kernel::activity::CommImpl*), void* data)
{
  xbt_assert(mbox, "No rendez-vous point defined for iprobe");

  return simgrid::kernel::actor::simcall([mbox, type, match_fun, data] { return mbox->iprobe(type, match_fun, data); });
}

/**
 * @ingroup simix_comm_management
 */
unsigned int simcall_comm_waitany(smx_activity_t comms[], size_t count, double timeout)
{
  std::unique_ptr<simgrid::kernel::activity::CommImpl* []> rcomms(new simgrid::kernel::activity::CommImpl*[count]);
  std::transform(comms, comms + count, rcomms.get(), [](const smx_activity_t& comm) {
    return static_cast<simgrid::kernel::activity::CommImpl*>(comm.get());
  });
  return simcall_BODY_comm_waitany(rcomms.get(), count, timeout);
}

unsigned int simcall_comm_waitany(simgrid::kernel::activity::CommImpl* comms[], size_t count, double timeout)
{
  return simcall_BODY_comm_waitany(comms, count, timeout);
}

/**
 * @ingroup simix_comm_management
 */
int simcall_comm_testany(smx_activity_t comms[], size_t count)
{
  if (count == 0)
    return -1;
  std::unique_ptr<simgrid::kernel::activity::CommImpl* []> rcomms(new simgrid::kernel::activity::CommImpl*[count]);
  std::transform(comms, comms + count, rcomms.get(), [](const smx_activity_t& comm) {
    return static_cast<simgrid::kernel::activity::CommImpl*>(comm.get());
  });
  return simcall_BODY_comm_testany(rcomms.get(), count);
}

int simcall_comm_testany(simgrid::kernel::activity::CommImpl* comms[], size_t count)
{
  if (count == 0)
    return -1;
  return simcall_BODY_comm_testany(comms, count);
}

/**
 * @ingroup simix_comm_management
 */
void simcall_comm_wait(const smx_activity_t& comm, double timeout)
{
  xbt_assert(std::isfinite(timeout), "timeout is not finite!");
  simcall_BODY_comm_wait(static_cast<simgrid::kernel::activity::CommImpl*>(comm.get()), timeout);
}

/**
 * @ingroup simix_comm_management
 *
 */
bool simcall_comm_test(const smx_activity_t& comm)
{
  return simcall_BODY_comm_test(static_cast<simgrid::kernel::activity::CommImpl*>(comm.get()));
}

/**
 * @ingroup simix_synchro_management
 *
 */
smx_mutex_t simcall_mutex_init()
{
  if (simix_global == nullptr) {
    fprintf(stderr, "You must initialize the SimGrid engine before using it\n"); // We can't use xbt_die since we may
                                                                                 // get there before the initialization
    xbt_abort();
  }
  return simgrid::kernel::actor::simcall([] { return new simgrid::kernel::activity::MutexImpl(); });
}

/**
 * @ingroup simix_synchro_management
 *
 */
void simcall_mutex_lock(smx_mutex_t mutex)
{
  simcall_BODY_mutex_lock(mutex);
}

/**
 * @ingroup simix_synchro_management
 *
 */
int simcall_mutex_trylock(smx_mutex_t mutex)
{
  return simcall_BODY_mutex_trylock(mutex);
}

/**
 * @ingroup simix_synchro_management
 *
 */
void simcall_mutex_unlock(smx_mutex_t mutex)
{
  simcall_BODY_mutex_unlock(mutex);
}

/**
 * @ingroup simix_synchro_management
 *
 */
smx_cond_t simcall_cond_init()
{
  return simgrid::kernel::actor::simcall([] { return new simgrid::kernel::activity::ConditionVariableImpl(); });
}

/**
 * @ingroup simix_synchro_management
 *
 */
void simcall_cond_wait(smx_cond_t cond, smx_mutex_t mutex)
{
  simcall_BODY_cond_wait(cond, mutex);
}

/**
 * @ingroup simix_synchro_management
 *
 */
int simcall_cond_wait_timeout(smx_cond_t cond, smx_mutex_t mutex, double timeout)
{
  xbt_assert(std::isfinite(timeout), "timeout is not finite!");
  return simcall_BODY_cond_wait_timeout(cond, mutex, timeout);
}

/**
 * @ingroup simix_synchro_management
 *
 */
void simcall_sem_acquire(smx_sem_t sem)
{
  simcall_BODY_sem_acquire(sem);
}

/**
 * @ingroup simix_synchro_management
 *
 */
int simcall_sem_acquire_timeout(smx_sem_t sem, double timeout)
{
  xbt_assert(std::isfinite(timeout), "timeout is not finite!");
  return simcall_BODY_sem_acquire_timeout(sem, timeout);
}

e_smx_state_t simcall_io_wait(const smx_activity_t& io)
{
  return (e_smx_state_t)simcall_BODY_io_wait(static_cast<simgrid::kernel::activity::IoImpl*>(io.get()));
}

void simcall_run_kernel(std::function<void()> const& code, simgrid::mc::SimcallInspector* t)
{
  SIMIX_process_self()->simcall.inspector_ = t;
  simcall_BODY_run_kernel(&code);
}

void simcall_run_blocking(std::function<void()> const& code, simgrid::mc::SimcallInspector* t = nullptr)
{
  SIMIX_process_self()->simcall.inspector_ = t;
  simcall_BODY_run_blocking(&code);
}

int simcall_mc_random(int min, int max) {
  return simcall_BODY_mc_random(min, max);
}

/* ************************************************************************** */

/** @brief returns a printable string representing a simcall */
const char *SIMIX_simcall_name(e_smx_simcall_t kind) {
  return simcall_names[kind];
}

namespace simgrid {
namespace simix {

void unblock(smx_actor_t actor)
{
  xbt_assert(SIMIX_is_maestro());
  actor->simcall_answer();
}
} // namespace simix
} // namespace simgrid

/* ****************************DEPRECATED CALLS******************************* */
void simcall_process_set_kill_time(smx_actor_t process, double kill_time)
{
  simgrid::kernel::actor::simcall([process, kill_time] { process->set_kill_time(kill_time); });
}
void simcall_comm_cancel(smx_activity_t comm)
{
  simgrid::kernel::actor::simcall(
      [comm] { boost::static_pointer_cast<simgrid::kernel::activity::CommImpl>(comm)->cancel(); });
}
void simcall_execution_cancel(smx_activity_t exec)
{
  simgrid::kernel::actor::simcall(
      [exec] { boost::static_pointer_cast<simgrid::kernel::activity::ExecImpl>(exec)->cancel(); });
}

void simcall_execution_set_bound(smx_activity_t exec, double bound)
{
  simgrid::kernel::actor::simcall(
      [exec, bound] { boost::static_pointer_cast<simgrid::kernel::activity::ExecImpl>(exec)->set_bound(bound); });
}

// deprecated
smx_activity_t simcall_execution_start(const std::string& name, const std::string& category, double flops_amount,
                                       double sharing_penalty, double bound, sg_host_t host)
{
  return simgrid::kernel::actor::simcall([name, category, flops_amount, sharing_penalty, bound, host] {
    simgrid::kernel::activity::ExecImpl* exec = new simgrid::kernel::activity::ExecImpl();
    (*exec)
        .set_name(name)
        .set_tracing_category(category)
        .set_host(host)
        .set_sharing_penalty(sharing_penalty)
        .set_bound(bound)
        .set_flops_amount(flops_amount)
        .start();
    return simgrid::kernel::activity::ExecImplPtr(exec);
  });
}

// deprecated
smx_activity_t simcall_execution_parallel_start(const std::string& name, int host_nb, const sg_host_t* host_list,
                                                const double* flops_amount, const double* bytes_amount, double rate,
                                                double timeout)
{
  /* Check that we are not mixing VMs and PMs in the parallel task */
  bool is_a_vm = (nullptr != dynamic_cast<simgrid::s4u::VirtualMachine*>(host_list[0]));
  for (int i = 1; i < host_nb; i++) {
    bool tmp_is_a_vm = (nullptr != dynamic_cast<simgrid::s4u::VirtualMachine*>(host_list[i]));
    xbt_assert(is_a_vm == tmp_is_a_vm, "parallel_execute: mixing VMs and PMs is not supported (yet).");
  }

  /* checking for infinite values */
  for (int i = 0; i < host_nb; ++i) {
    if (flops_amount != nullptr)
      xbt_assert(std::isfinite(flops_amount[i]), "flops_amount[%d] is not finite!", i);
    if (bytes_amount != nullptr) {
      for (int j = 0; j < host_nb; ++j) {
        xbt_assert(std::isfinite(bytes_amount[i + host_nb * j]), "bytes_amount[%d+%d*%d] is not finite!", i, host_nb,
                   j);
      }
    }
  }
  xbt_assert(std::isfinite(rate), "rate is not finite!");

  std::vector<simgrid::s4u::Host*> hosts(host_list, host_list + host_nb);
  std::vector<double> flops_parallel_amount;
  std::vector<double> bytes_parallel_amount;
  if (flops_amount != nullptr)
    flops_parallel_amount = std::vector<double>(flops_amount, flops_amount + host_nb);
  if (bytes_amount != nullptr)
    bytes_parallel_amount = std::vector<double>(bytes_amount, bytes_amount + host_nb * host_nb);
  return simgrid::kernel::actor::simcall([name, hosts, flops_parallel_amount, bytes_parallel_amount, timeout] {
    simgrid::kernel::activity::ExecImpl* exec = new simgrid::kernel::activity::ExecImpl();
    (*exec)
        .set_name(name)
        .set_hosts(hosts)
        .set_timeout(timeout)
        .set_flops_amounts(flops_parallel_amount)
        .set_bytes_amounts(bytes_parallel_amount)
        .start();
    return simgrid::kernel::activity::ExecImplPtr(exec);
  });
}

// deprecated
void SIMIX_comm_finish(smx_activity_t synchro)
{
  boost::static_pointer_cast<simgrid::kernel::activity::CommImpl>(synchro)->finish();
}
