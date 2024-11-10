package client

import (
	"context"
	"github.com/marcinkonwiak/monitoring-client/pb"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
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

func (c *Client) Start() {
	grpcConn, err := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Failed to connect to the server: %v", err)
	}
	defer func(grpcClient *grpc.ClientConn) {
		err := grpcClient.Close()
		if err != nil {
			log.Fatalf("Failed to close the connection: %v", err)
		}
	}(grpcConn)

	client := pb.NewHostStatsControllerClient(grpcConn)
	stream, err := client.Stream(context.Background())
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
			err := sendStats(stream, data)
			if err != nil {
				log.Printf("Failed to send data: %v\n", err)
				break mainLoop
			}
		}
	}
}

func sendStats(stream pb.HostStatsController_StreamClient, data statsData) error {
	log.Printf("🦆 Sending data: %+v\n", data)
	if err := stream.Send(data.toRequestData()); err != nil {
		return err
	}
	return nil
}
