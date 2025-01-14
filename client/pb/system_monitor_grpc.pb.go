// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.5.1
// - protoc             v5.28.2
// source: system_monitor.proto

package pb

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	emptypb "google.golang.org/protobuf/types/known/emptypb"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.64.0 or later.
const _ = grpc.SupportPackageIsVersion9

const (
	HostStatsController_Stream_FullMethodName = "/config.system_monitor.HostStatsController/Stream"
)

// HostStatsControllerClient is the client API for HostStatsController service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type HostStatsControllerClient interface {
	Stream(ctx context.Context, opts ...grpc.CallOption) (grpc.BidiStreamingClient[StatsDataInputRequest, emptypb.Empty], error)
}

type hostStatsControllerClient struct {
	cc grpc.ClientConnInterface
}

func NewHostStatsControllerClient(cc grpc.ClientConnInterface) HostStatsControllerClient {
	return &hostStatsControllerClient{cc}
}

func (c *hostStatsControllerClient) Stream(ctx context.Context, opts ...grpc.CallOption) (grpc.BidiStreamingClient[StatsDataInputRequest, emptypb.Empty], error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	stream, err := c.cc.NewStream(ctx, &HostStatsController_ServiceDesc.Streams[0], HostStatsController_Stream_FullMethodName, cOpts...)
	if err != nil {
		return nil, err
	}
	x := &grpc.GenericClientStream[StatsDataInputRequest, emptypb.Empty]{ClientStream: stream}
	return x, nil
}

// This type alias is provided for backwards compatibility with existing code that references the prior non-generic stream type by name.
type HostStatsController_StreamClient = grpc.BidiStreamingClient[StatsDataInputRequest, emptypb.Empty]

// HostStatsControllerServer is the server API for HostStatsController service.
// All implementations must embed UnimplementedHostStatsControllerServer
// for forward compatibility.
type HostStatsControllerServer interface {
	Stream(grpc.BidiStreamingServer[StatsDataInputRequest, emptypb.Empty]) error
	mustEmbedUnimplementedHostStatsControllerServer()
}

// UnimplementedHostStatsControllerServer must be embedded to have
// forward compatible implementations.
//
// NOTE: this should be embedded by value instead of pointer to avoid a nil
// pointer dereference when methods are called.
type UnimplementedHostStatsControllerServer struct{}

func (UnimplementedHostStatsControllerServer) Stream(grpc.BidiStreamingServer[StatsDataInputRequest, emptypb.Empty]) error {
	return status.Errorf(codes.Unimplemented, "method Stream not implemented")
}
func (UnimplementedHostStatsControllerServer) mustEmbedUnimplementedHostStatsControllerServer() {}
func (UnimplementedHostStatsControllerServer) testEmbeddedByValue()                             {}

// UnsafeHostStatsControllerServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to HostStatsControllerServer will
// result in compilation errors.
type UnsafeHostStatsControllerServer interface {
	mustEmbedUnimplementedHostStatsControllerServer()
}

func RegisterHostStatsControllerServer(s grpc.ServiceRegistrar, srv HostStatsControllerServer) {
	// If the following call pancis, it indicates UnimplementedHostStatsControllerServer was
	// embedded by pointer and is nil.  This will cause panics if an
	// unimplemented method is ever invoked, so we test this at initialization
	// time to prevent it from happening at runtime later due to I/O.
	if t, ok := srv.(interface{ testEmbeddedByValue() }); ok {
		t.testEmbeddedByValue()
	}
	s.RegisterService(&HostStatsController_ServiceDesc, srv)
}

func _HostStatsController_Stream_Handler(srv interface{}, stream grpc.ServerStream) error {
	return srv.(HostStatsControllerServer).Stream(&grpc.GenericServerStream[StatsDataInputRequest, emptypb.Empty]{ServerStream: stream})
}

// This type alias is provided for backwards compatibility with existing code that references the prior non-generic stream type by name.
type HostStatsController_StreamServer = grpc.BidiStreamingServer[StatsDataInputRequest, emptypb.Empty]

// HostStatsController_ServiceDesc is the grpc.ServiceDesc for HostStatsController service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var HostStatsController_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "config.system_monitor.HostStatsController",
	HandlerType: (*HostStatsControllerServer)(nil),
	Methods:     []grpc.MethodDesc{},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "Stream",
			Handler:       _HostStatsController_Stream_Handler,
			ServerStreams: true,
			ClientStreams: true,
		},
	},
	Metadata: "system_monitor.proto",
}
