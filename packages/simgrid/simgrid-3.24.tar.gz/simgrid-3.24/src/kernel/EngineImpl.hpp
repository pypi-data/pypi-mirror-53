/* Copyright (c) 2016-2019. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include <simgrid/s4u/NetZone.hpp>

#include <map>
#include <string>
#include <unordered_map>

namespace simgrid {
namespace kernel {

class EngineImpl {
  std::map<std::string, s4u::Host*> hosts_;
  std::map<std::string, s4u::Link*> links_;
  std::map<std::string, s4u::Storage*> storages_;
  std::unordered_map<std::string, routing::NetPoint*> netpoints_;
  friend s4u::Engine;

public:
  EngineImpl() = default;

  EngineImpl(const EngineImpl&) = delete;
  EngineImpl& operator=(const EngineImpl&) = delete;
  virtual ~EngineImpl();
  routing::NetZoneImpl* netzone_root_ = nullptr;
};

} // namespace kernel
} // namespace simgrid
