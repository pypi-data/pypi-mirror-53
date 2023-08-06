/* Copyright (c) 2007-2019. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "private.hpp"

#include "smpi_file.hpp"
#include "smpi_datatype.hpp"

extern MPI_Errhandler SMPI_default_File_Errhandler;

int PMPI_File_open(MPI_Comm comm, const char *filename, int amode, MPI_Info info, MPI_File *fh){
  if (comm == MPI_COMM_NULL)
    return MPI_ERR_COMM;
  if (filename == nullptr)
    return MPI_ERR_FILE;
  if (amode < 0)
    return MPI_ERR_AMODE;
  smpi_bench_end();
  *fh =  new simgrid::smpi::File(comm, filename, amode, info);
  smpi_bench_begin();
  if ((*fh)->size() != 0 && (amode & MPI_MODE_EXCL)){
    delete fh;
    return MPI_ERR_AMODE;
  }
  if(amode & MPI_MODE_APPEND)
    (*fh)->seek(0,MPI_SEEK_END);
  return MPI_SUCCESS;
}

int PMPI_File_close(MPI_File *fh){
  if (fh==nullptr)
    return MPI_ERR_ARG;
  smpi_bench_end();
  int ret = simgrid::smpi::File::close(fh);
  *fh = MPI_FILE_NULL;
  smpi_bench_begin();
  return ret;
}
#define CHECK_FILE(fh)                                                                                                 \
  if ((fh) == MPI_FILE_NULL)                                                                                           \
    return MPI_ERR_FILE;
#define CHECK_BUFFER(buf, count)                                                                                       \
  if ((buf) == nullptr && (count) > 0)                                                                                 \
    return MPI_ERR_BUFFER;
#define CHECK_COUNT(count)                                                                                             \
  if ((count) < 0)                                                                                                     \
    return MPI_ERR_COUNT;
#define CHECK_OFFSET(offset)                                                                                           \
  if ((offset) < 0)                                                                                                    \
    return MPI_ERR_DISP;
#define CHECK_DATATYPE(datatype, count)                                                                                \
  if ((datatype) == MPI_DATATYPE_NULL && (count) > 0)                                                                  \
    return MPI_ERR_TYPE;
#define CHECK_STATUS(status)                                                                                           \
  if ((status) == nullptr)                                                                                             \
    return MPI_ERR_ARG;
#define CHECK_FLAGS(fh)                                                                                                \
  if ((fh)->flags() & MPI_MODE_SEQUENTIAL)                                                                             \
    return MPI_ERR_AMODE;
#define CHECK_RDONLY(fh)                                                                                               \
  if ((fh)->flags() & MPI_MODE_RDONLY)                                                                                 \
    return MPI_ERR_AMODE;

#define PASS_ZEROCOUNT(count)                                                                                          \
  if ((count) == 0) {                                                                                                  \
    status->count = 0;                                                                                                 \
    return MPI_SUCCESS;                                                                                                \
  }

int PMPI_File_seek(MPI_File fh, MPI_Offset offset, int whence){
  CHECK_FILE(fh);
  smpi_bench_end();
  int ret = fh->seek(offset,whence);
  smpi_bench_begin();
  return ret;

}

int PMPI_File_seek_shared(MPI_File fh, MPI_Offset offset, int whence){
  CHECK_FILE(fh)
  smpi_bench_end();
  int ret = fh->seek_shared(offset,whence);
  smpi_bench_begin();
  return ret;

}

int PMPI_File_get_position(MPI_File fh, MPI_Offset* offset){
  if (offset==nullptr)
    return MPI_ERR_DISP;
  smpi_bench_end();
  int ret = fh->get_position(offset);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_get_position_shared(MPI_File fh, MPI_Offset* offset){
  CHECK_FILE(fh)
  if (offset==nullptr)
    return MPI_ERR_DISP;
  smpi_bench_end();
  int ret = fh->get_position_shared(offset);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_read(MPI_File fh, void *buf, int count,MPI_Datatype datatype, MPI_Status *status){
  CHECK_FILE(fh)
  CHECK_BUFFER(buf, count)
  CHECK_COUNT(count)
  CHECK_DATATYPE(datatype, count)
  CHECK_STATUS(status)
  CHECK_FLAGS(fh)
  PASS_ZEROCOUNT(count)
  smpi_bench_end();
  int rank_traced = simgrid::s4u::this_actor::get_pid();
  TRACE_smpi_comm_in(rank_traced, __func__, new simgrid::instr::CpuTIData("IO - read", count * datatype->size()));
  int ret = simgrid::smpi::File::read(fh, buf, count, datatype, status);
  TRACE_smpi_comm_out(rank_traced);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_read_shared(MPI_File fh, void *buf, int count,MPI_Datatype datatype, MPI_Status *status){
  CHECK_FILE(fh)
  CHECK_BUFFER(buf, count)
  CHECK_COUNT(count)
  CHECK_DATATYPE(datatype, count)
  CHECK_STATUS(status)
  CHECK_FLAGS(fh)
  PASS_ZEROCOUNT(count)
  smpi_bench_end();
  int rank_traced = simgrid::s4u::this_actor::get_pid();
  TRACE_smpi_comm_in(rank_traced, __func__,
                     new simgrid::instr::CpuTIData("IO - read_shared", count * datatype->size()));
  int ret = simgrid::smpi::File::read_shared(fh, buf, count, datatype, status);
  TRACE_smpi_comm_out(rank_traced);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_write(MPI_File fh, const void *buf, int count,MPI_Datatype datatype, MPI_Status *status){
  CHECK_FILE(fh)
  CHECK_BUFFER(buf, count)
  CHECK_COUNT(count)
  CHECK_DATATYPE(datatype, count)
  CHECK_STATUS(status)
  CHECK_FLAGS(fh)
  CHECK_RDONLY(fh)
  PASS_ZEROCOUNT(count)
  smpi_bench_end();
  int rank_traced = simgrid::s4u::this_actor::get_pid();
  TRACE_smpi_comm_in(rank_traced, __func__, new simgrid::instr::CpuTIData("IO - write", count * datatype->size()));
  int ret = simgrid::smpi::File::write(fh, const_cast<void*>(buf), count, datatype, status);
  TRACE_smpi_comm_out(rank_traced);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_write_shared(MPI_File fh, const void *buf, int count,MPI_Datatype datatype, MPI_Status *status){
  CHECK_FILE(fh)
  CHECK_BUFFER(buf, count)
  CHECK_COUNT(count)
  CHECK_DATATYPE(datatype, count)
  CHECK_STATUS(status)
  CHECK_FLAGS(fh)
  CHECK_RDONLY(fh)
  PASS_ZEROCOUNT(count)
  smpi_bench_end();
  int rank_traced = simgrid::s4u::this_actor::get_pid();
  TRACE_smpi_comm_in(rank_traced, __func__,
                     new simgrid::instr::CpuTIData("IO - write_shared", count * datatype->size()));
  int ret = simgrid::smpi::File::write_shared(fh, buf, count, datatype, status);
  TRACE_smpi_comm_out(rank_traced);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_read_all(MPI_File fh, void *buf, int count,MPI_Datatype datatype, MPI_Status *status){
  CHECK_FILE(fh)
  CHECK_BUFFER(buf, count)
  CHECK_COUNT(count)
  CHECK_DATATYPE(datatype, count)
  CHECK_STATUS(status)
  CHECK_FLAGS(fh)
  smpi_bench_end();
  int rank_traced = simgrid::s4u::this_actor::get_pid();
  TRACE_smpi_comm_in(rank_traced, __func__, new simgrid::instr::CpuTIData("IO - read_all", count * datatype->size()));
  int ret = fh->op_all<simgrid::smpi::File::read>(buf, count, datatype, status);
  TRACE_smpi_comm_out(rank_traced);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_read_ordered(MPI_File fh, void *buf, int count,MPI_Datatype datatype, MPI_Status *status){
  CHECK_FILE(fh)
  CHECK_BUFFER(buf, count)
  CHECK_COUNT(count)
  CHECK_DATATYPE(datatype, count)
  CHECK_STATUS(status)
  CHECK_FLAGS(fh)
  smpi_bench_end();
  int rank_traced = simgrid::s4u::this_actor::get_pid();
  TRACE_smpi_comm_in(rank_traced, __func__,
                     new simgrid::instr::CpuTIData("IO - read_ordered", count * datatype->size()));
  int ret = simgrid::smpi::File::read_ordered(fh, buf, count, datatype, status);
  TRACE_smpi_comm_out(rank_traced);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_write_all(MPI_File fh, const void *buf, int count,MPI_Datatype datatype, MPI_Status *status){
  CHECK_FILE(fh)
  CHECK_BUFFER(buf, count)
  CHECK_COUNT(count)
  CHECK_DATATYPE(datatype, count)
  CHECK_STATUS(status)
  CHECK_FLAGS(fh)
  CHECK_RDONLY(fh)
  smpi_bench_end();
  int rank_traced = simgrid::s4u::this_actor::get_pid();
  TRACE_smpi_comm_in(rank_traced, __func__, new simgrid::instr::CpuTIData("IO - write_all", count * datatype->size()));
  int ret = fh->op_all<simgrid::smpi::File::write>(const_cast<void*>(buf), count, datatype, status);
  TRACE_smpi_comm_out(rank_traced);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_write_ordered(MPI_File fh, const void *buf, int count,MPI_Datatype datatype, MPI_Status *status){
  CHECK_FILE(fh)
  CHECK_BUFFER(buf, count)
  CHECK_COUNT(count)
  CHECK_DATATYPE(datatype, count)
  CHECK_STATUS(status)
  CHECK_FLAGS(fh)
  CHECK_RDONLY(fh)
  smpi_bench_end();
  int rank_traced = simgrid::s4u::this_actor::get_pid();
  TRACE_smpi_comm_in(rank_traced, __func__,
                     new simgrid::instr::CpuTIData("IO - write_ordered", count * datatype->size()));
  int ret = simgrid::smpi::File::write_ordered(fh, buf, count, datatype, status);
  TRACE_smpi_comm_out(rank_traced);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_read_at(MPI_File fh, MPI_Offset offset, void *buf, int count,MPI_Datatype datatype, MPI_Status *status){
  CHECK_FILE(fh)
  CHECK_BUFFER(buf, count)
  CHECK_OFFSET(offset)
  CHECK_COUNT(count)
  CHECK_DATATYPE(datatype, count)
  CHECK_STATUS(status)
  CHECK_FLAGS(fh)
  PASS_ZEROCOUNT(count);
  smpi_bench_end();
  int rank_traced = simgrid::s4u::this_actor::get_pid();
  TRACE_smpi_comm_in(rank_traced, __func__, new simgrid::instr::CpuTIData("IO - read", count * datatype->size()));
  int ret = fh->seek(offset,MPI_SEEK_SET);
  if(ret!=MPI_SUCCESS)
    return ret;
  ret = simgrid::smpi::File::read(fh, buf, count, datatype, status);
  TRACE_smpi_comm_out(rank_traced);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_read_at_all(MPI_File fh, MPI_Offset offset, void *buf, int count,MPI_Datatype datatype, MPI_Status *status){
  CHECK_FILE(fh)
  CHECK_BUFFER(buf, count)
  CHECK_OFFSET(offset)
  CHECK_COUNT(count)
  CHECK_DATATYPE(datatype, count)
  CHECK_STATUS(status)
  CHECK_FLAGS(fh)
  smpi_bench_end();
  int rank_traced = simgrid::s4u::this_actor::get_pid();
  TRACE_smpi_comm_in(rank_traced, __func__,
                     new simgrid::instr::CpuTIData("IO - read_at_all", count * datatype->size()));
  int ret = fh->seek(offset,MPI_SEEK_SET);
  if(ret!=MPI_SUCCESS)
    return ret;
  ret = fh->op_all<simgrid::smpi::File::read>(buf, count, datatype, status);
  TRACE_smpi_comm_out(rank_traced);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_write_at(MPI_File fh, MPI_Offset offset, const void *buf, int count,MPI_Datatype datatype, MPI_Status *status){
  CHECK_FILE(fh)
  CHECK_BUFFER(buf, count)
  CHECK_OFFSET(offset)
  CHECK_COUNT(count)
  CHECK_DATATYPE(datatype, count)
  CHECK_STATUS(status)
  CHECK_FLAGS(fh)
  CHECK_RDONLY(fh)
  PASS_ZEROCOUNT(count);
  smpi_bench_end();
  int rank_traced = simgrid::s4u::this_actor::get_pid();
  TRACE_smpi_comm_in(rank_traced, __func__, new simgrid::instr::CpuTIData("IO - write", count * datatype->size()));
  int ret = fh->seek(offset,MPI_SEEK_SET);
  if(ret!=MPI_SUCCESS)
    return ret;
  ret = simgrid::smpi::File::write(fh, const_cast<void*>(buf), count, datatype, status);
  TRACE_smpi_comm_out(rank_traced);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_write_at_all(MPI_File fh, MPI_Offset offset, const void *buf, int count,MPI_Datatype datatype, MPI_Status *status){
  CHECK_FILE(fh)
  CHECK_BUFFER(buf, count)
  CHECK_OFFSET(offset)
  CHECK_COUNT(count)
  CHECK_DATATYPE(datatype, count)
  CHECK_STATUS(status)
  CHECK_FLAGS(fh)
  CHECK_RDONLY(fh)
  smpi_bench_end();
  int rank_traced = simgrid::s4u::this_actor::get_pid();
  TRACE_smpi_comm_in(rank_traced, __func__,
                     new simgrid::instr::CpuTIData("IO - write_at_all", count * datatype->size()));
  int ret = fh->seek(offset,MPI_SEEK_SET);
  if(ret!=MPI_SUCCESS)
    return ret;
  ret = fh->op_all<simgrid::smpi::File::write>(const_cast<void*>(buf), count, datatype, status);
  TRACE_smpi_comm_out(rank_traced);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_delete(const char *filename, MPI_Info info){
  if (filename == nullptr)
    return MPI_ERR_FILE;
  smpi_bench_end();
  int ret = simgrid::smpi::File::del(filename, info);
  smpi_bench_begin();
  return ret;
}

int PMPI_File_get_info(MPI_File  fh, MPI_Info* info)
{
  CHECK_FILE(fh)
  *info = fh->info();
  return MPI_SUCCESS;
}

int PMPI_File_set_info(MPI_File  fh, MPI_Info info)
{
  CHECK_FILE(fh)
  fh->set_info(info);
  return MPI_SUCCESS;
}

int PMPI_File_get_size(MPI_File  fh, MPI_Offset* size)
{
  CHECK_FILE(fh)
  *size = fh->size();
  return MPI_SUCCESS;
}

int PMPI_File_get_amode(MPI_File  fh, int* amode)
{
  CHECK_FILE(fh)
  *amode = fh->flags();
  return MPI_SUCCESS;
}

int PMPI_File_get_group(MPI_File  fh, MPI_Group* group)
{
  CHECK_FILE(fh)
  *group = fh->comm()->group();
  return MPI_SUCCESS;
}

int PMPI_File_sync(MPI_File  fh)
{
  CHECK_FILE(fh)
  fh->sync();
  return MPI_SUCCESS;
}

int PMPI_File_create_errhandler(MPI_File_errhandler_function* function, MPI_Errhandler* errhandler){
  *errhandler=new simgrid::smpi::Errhandler(function);
  return MPI_SUCCESS;
}

int PMPI_File_get_errhandler(MPI_File file, MPI_Errhandler* errhandler){
  if (errhandler==nullptr){
    return MPI_ERR_ARG;
  } else if (file == MPI_FILE_NULL) {
    *errhandler = SMPI_default_File_Errhandler;
    return MPI_SUCCESS;
  }
  *errhandler=file->errhandler();
  return MPI_SUCCESS;
}

int PMPI_File_set_errhandler(MPI_File file, MPI_Errhandler errhandler){
  if (errhandler==nullptr){
    return MPI_ERR_ARG;
  } else if (file == MPI_FILE_NULL) {
    SMPI_default_File_Errhandler = errhandler;
    return MPI_SUCCESS;
  }
  file->set_errhandler(errhandler);
  return MPI_SUCCESS;
}

int PMPI_File_call_errhandler(MPI_File file,int errorcode){
  if (file == nullptr) {
    return MPI_ERR_WIN;
  }
  file->errhandler()->call(file, errorcode);
  return MPI_SUCCESS;
}
