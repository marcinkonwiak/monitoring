package client

import (
	"context"
	"github.com/marcinkonwiak/monitoring-client/pb"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/protobuf/types/known/emptypb"
	"log"
	"time"
)

type Client struct {
	statsCollector *statsCollector
}

func NewClient() *Client {
	return &Client{
		statsCollector: newStatsCollector(time.Duration(1) * time.Second),
	}
}

func getConnection() (*grpc.ClientConn, error) {
	grpcConn, err := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return nil, err
	}
	return grpcConn, nil
}

func (c *Client) getStream(conn *grpc.ClientConn) (grpc.BidiStreamingClient[pb.StatsDataInputRequest, emptypb.Empty], error) {
	client := pb.NewHostStatsControllerClient(conn)
	stream, err := client.Stream(context.Background())
	if err != nil {
		return nil, err
	}

	return stream, err
}

func (c *Client) Start() {
	grpcConn, err := getConnection()
	if err != nil {
		log.Fatalf("Failed to connect to the server: %v", err)
	}
	defer func(grpcClient *grpc.ClientConn) {
		err := grpcClient.Close()
		if err != nil {
			log.Fatalf("Failed to close the connection: %v", err)
		}
	}(grpcConn)

	stream, err := c.getStream(grpcConn)
	if err != nil {
		log.Fatalf("Failed to create stream: %v", err)
	}

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	go c.statsCollector.start(ctx)

mainLoop:
	for {
		select {
		case data := <-c.statsCollector.data:
			if err := stream.Send(data.toRequestData()); err != nil {
				log.Printf("Failed to send data: %v", err)
				break mainLoop
			}
			log.Printf("Data sent")
		}
	}
}
