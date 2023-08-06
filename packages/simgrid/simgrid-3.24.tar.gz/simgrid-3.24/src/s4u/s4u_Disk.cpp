/* Copyright (c) 2019. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "simgrid/s4u/Disk.hpp"
#include "simgrid/s4u/Engine.hpp"
#include "simgrid/s4u/Host.hpp"
#include "simgrid/s4u/Io.hpp"
#include "src/kernel/resource/DiskImpl.hpp"

namespace simgrid {
namespace xbt {
template class Extendable<s4u::Disk>;
} // namespace xbt

namespace s4u {

xbt::signal<void(Disk&)> Disk::on_creation;
xbt::signal<void(Disk const&)> Disk::on_destruction;
xbt::signal<void(Disk const&)> Disk::on_state_change;

Host* Disk::get_host()
{
  return pimpl_->get_host();
}

const std::unordered_map<std::string, std::string>* Disk::get_properties() const
{
  return pimpl_->get_properties();
}

const char* Disk::get_property(const std::string& key) const
{
  return this->pimpl_->get_property(key);
}

void Disk::set_property(const std::string& key, const std::string& value)
{
  kernel::actor::simcall([this, &key, &value] { this->pimpl_->set_property(key, value); });
}

IoPtr Disk::io_init(sg_size_t size, Io::OpType type)
{
  return IoPtr(new Io(this, size, type));
}

IoPtr Disk::read_async(sg_size_t size)
{
  return IoPtr(io_init(size, Io::OpType::READ))->start();
}

sg_size_t Disk::read(sg_size_t size)
{
  return IoPtr(io_init(size, Io::OpType::READ))->start()->wait()->get_performed_ioops();
}

IoPtr Disk::write_async(sg_size_t size)
{

  return IoPtr(io_init(size, Io::OpType::WRITE)->start());
}

sg_size_t Disk::write(sg_size_t size)
{
  return IoPtr(io_init(size, Io::OpType::WRITE))->start()->wait()->get_performed_ioops();
}

} // namespace s4u
} // namespace simgrid
