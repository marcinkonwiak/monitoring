# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: system_monitor/grpc/system_monitor.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'system_monitor/grpc/system_monitor.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(system_monitor/grpc/system_monitor.proto\x12\x15\x63onfig.system_monitor\x1a\x1bgoogle/protobuf/empty.proto\"\'\n\x14StatsCpuInputRequest\x12\x0f\n\x07percent\x18\x01 \x01(\x02\"\xd6\x01\n\x15StatsDataInputRequest\x12\x11\n\ttimestamp\x18\x01 \x01(\x05\x12\x38\n\x03\x63pu\x18\x02 \x01(\x0b\x32+.config.system_monitor.StatsCpuInputRequest\x12\x38\n\x03ram\x18\x03 \x01(\x0b\x32+.config.system_monitor.StatsRamInputRequest\x12\x36\n\x02os\x18\x04 \x01(\x0b\x32*.config.system_monitor.StatsOsInputRequest\"o\n\x13StatsOsInputRequest\x12\x0e\n\x06hostID\x18\x01 \x01(\t\x12\n\n\x02os\x18\x02 \x01(\t\x12\x10\n\x08platform\x18\x03 \x01(\t\x12\x17\n\x0fplatformVersion\x18\x04 \x01(\t\x12\x11\n\tprocesses\x18\x05 \x01(\x04\"F\n\x14StatsRamInputRequest\x12\r\n\x05total\x18\x01 \x01(\x04\x12\x11\n\tavailable\x18\x02 \x01(\x04\x12\x0c\n\x04used\x18\x03 \x01(\x04\x32k\n\x13HostStatsController\x12T\n\x06Stream\x12,.config.system_monitor.StatsDataInputRequest\x1a\x16.google.protobuf.Empty\"\x00(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'system_monitor.grpc.system_monitor_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_STATSCPUINPUTREQUEST']._serialized_start=96
  _globals['_STATSCPUINPUTREQUEST']._serialized_end=135
  _globals['_STATSDATAINPUTREQUEST']._serialized_start=138
  _globals['_STATSDATAINPUTREQUEST']._serialized_end=352
  _globals['_STATSOSINPUTREQUEST']._serialized_start=354
  _globals['_STATSOSINPUTREQUEST']._serialized_end=465
  _globals['_STATSRAMINPUTREQUEST']._serialized_start=467
  _globals['_STATSRAMINPUTREQUEST']._serialized_end=537
  _globals['_HOSTSTATSCONTROLLER']._serialized_start=539
  _globals['_HOSTSTATSCONTROLLER']._serialized_end=646
# @@protoc_insertion_point(module_scope)
