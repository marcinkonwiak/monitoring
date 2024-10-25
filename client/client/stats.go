package client

import (
	"context"
	"time"
)

type statsData struct {
	timestamp      int64
	cpuPercent     float64
	ramTotal       uint64
	ramAvailable   uint64
	ramUsed        uint64
	ramUsedPercent float64
}

type statsCollector struct {
	interval int
	data     chan []statsData
}

func newStatsCollector(interval int) *statsCollector {
	return &statsCollector{
		interval: interval,
		data:     make(chan []statsData),
	}
}

func (s *statsCollector) start(ctx context.Context) {
	ticker := time.NewTicker(time.Duration(s.interval) * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			s.collectStats()
		}
	}
}

func (s *statsCollector) collectStats() {

}

func (s *statsCollector) getCpuData() {

}

func (s *statsCollector) getRamData() {

}
