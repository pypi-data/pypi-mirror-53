# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hedgehog/protocol/proto/subscription.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='hedgehog/protocol/proto/subscription.proto',
  package='hedgehog.protocol.proto',
  syntax='proto3',
  serialized_pb=_b('\n*hedgehog/protocol/proto/subscription.proto\x12\x17hedgehog.protocol.proto\"y\n\x0cSubscription\x12\x11\n\tsubscribe\x18\x01 \x01(\x08\x12\x0f\n\x07timeout\x18\x02 \x01(\r\x12\x1b\n\x13granularity_timeout\x18\x03 \x01(\r\x12\x19\n\x0fint_granularity\x18\x04 \x01(\rH\x00\x42\r\n\x0bgranularityB0\n\x1f\x61t.pria.hedgehog.protocol.protoB\rSubscriptionPb\x06proto3')
)




_SUBSCRIPTION = _descriptor.Descriptor(
  name='Subscription',
  full_name='hedgehog.protocol.proto.Subscription',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='subscribe', full_name='hedgehog.protocol.proto.Subscription.subscribe', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeout', full_name='hedgehog.protocol.proto.Subscription.timeout', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='granularity_timeout', full_name='hedgehog.protocol.proto.Subscription.granularity_timeout', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int_granularity', full_name='hedgehog.protocol.proto.Subscription.int_granularity', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='granularity', full_name='hedgehog.protocol.proto.Subscription.granularity',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=71,
  serialized_end=192,
)

_SUBSCRIPTION.oneofs_by_name['granularity'].fields.append(
  _SUBSCRIPTION.fields_by_name['int_granularity'])
_SUBSCRIPTION.fields_by_name['int_granularity'].containing_oneof = _SUBSCRIPTION.oneofs_by_name['granularity']
DESCRIPTOR.message_types_by_name['Subscription'] = _SUBSCRIPTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Subscription = _reflection.GeneratedProtocolMessageType('Subscription', (_message.Message,), dict(
  DESCRIPTOR = _SUBSCRIPTION,
  __module__ = 'hedgehog.protocol.proto.subscription_pb2'
  # @@protoc_insertion_point(class_scope:hedgehog.protocol.proto.Subscription)
  ))
_sym_db.RegisterMessage(Subscription)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\037at.pria.hedgehog.protocol.protoB\rSubscriptionP'))
# @@protoc_insertion_point(module_scope)
