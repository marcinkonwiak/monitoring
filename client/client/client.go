package client

import (
	"context"
	"time"
)

type Client struct {
	statsCollector *statsCollector
}

func NewClient() *Client {
	return &Client{
		// Todo: make interval configurable
		statsCollector: newStatsCollector(time.Duration(1) * time.Second),
	}
}

func (c *Client) Start() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	c.statsCollector.start(ctx)
}
