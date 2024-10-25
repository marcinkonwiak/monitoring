package main

import "github.com/marcinkonwiak/monitoring-client/client"

func main() {
	client.NewClient().Start()
}
