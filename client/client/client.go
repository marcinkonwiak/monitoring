package client

type Client struct {
	statsCollector *statsCollector
}

func NewClient() *Client {
	return &Client{
		statsCollector: newStatsCollector(1), // Todo: make interval configurable
	}
}

func (c *Client) Start() {

}
