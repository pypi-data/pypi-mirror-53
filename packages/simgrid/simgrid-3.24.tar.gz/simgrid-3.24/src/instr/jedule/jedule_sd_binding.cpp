/* Copyright (c) 2010-2019. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "simgrid/jedule/jedule.hpp"
#include "src/simdag/simdag_private.hpp"

#include "simgrid/s4u/Engine.hpp"
#include "simgrid/s4u/NetZone.hpp"

#if SIMGRID_HAVE_JEDULE

XBT_LOG_NEW_CATEGORY(jedule, "Logging specific to Jedule");
XBT_LOG_NEW_DEFAULT_SUBCATEGORY(jed_sd, jedule, "Logging specific to Jedule SD binding");

jedule_t my_jedule;

void jedule_log_sd_event(SD_task_t task)
{
  xbt_assert(task != nullptr);

  simgrid::jedule::Event event(std::string(SD_task_get_name(task)), SD_task_get_start_time(task),
                               SD_task_get_finish_time(task), "SD");
  event.add_resources(*task->allocation);
  my_jedule->event_set_.emplace_back(std::move(event));
}

void jedule_sd_init()
{
  sg_netzone_t root_comp = simgrid::s4u::Engine::get_instance()->get_netzone_root();
  XBT_DEBUG("root name %s\n", root_comp->get_cname());

  my_jedule = new simgrid::jedule::Jedule(root_comp->get_name());
  my_jedule->root_container_.create_hierarchy(root_comp);
}

void jedule_sd_exit()
{
  delete my_jedule;
}

void jedule_sd_dump(const char * filename)
{
  if (my_jedule) {
    char *fname;
    if (not filename) {
      fname = bprintf("%s.jed", xbt_binary_name);
    } else {
      fname = xbt_strdup(filename);
    }

    FILE *fh = fopen(fname, "w");

    my_jedule->write_output(fh);

    fclose(fh);
    xbt_free(fname);
  }
}
#endif
