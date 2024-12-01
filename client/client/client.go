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
			if err := sendStatsWithRetry(stream, data, 3, time.Second); err != nil {
				log.Printf("Failed to send data after 3 attempts: %v", err)
				break mainLoop
			}
			log.Printf("Data sent")
		}
	}
}

func sendStatsWithRetry(stream pb.HostStatsController_StreamClient, data statsData, maxRetries int, retryDelay time.Duration) error {
	var err error
	for attempt := 1; attempt <= maxRetries; attempt++ {
		err = stream.Send(data.toRequestData())
		if err == nil {
			return nil
		}

		log.Printf("Attempt %d to send data failed: %v", attempt, err)
		time.Sleep(retryDelay)
	}

	return err
}
