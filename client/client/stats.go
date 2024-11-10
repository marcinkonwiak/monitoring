package client

import (
	"context"
	"errors"
	"github.com/marcinkonwiak/monitoring-client/pb"
	"github.com/shirou/gopsutil/v4/cpu"
	"github.com/shirou/gopsutil/v4/host"
	"github.com/shirou/gopsutil/v4/mem"
	"log"
	"time"
)

type statsData struct {
	timestamp int64
	cpu       statsCpu
	ram       statsRam
	os        statsOs
}

type statsCpu struct {
	percent float64
}

type statsRam struct {
	total     uint64
	available uint64
	used      uint64
}

type statsOs struct {
	hostID          string
	os              string
	platform        string
	platformVersion string
	processes       uint64
}

func (s statsData) toRequestData() *pb.StatsDataInputRequest {
	return &pb.StatsDataInputRequest{
		Timestamp: int32(s.timestamp),
		Cpu: &pb.StatsCpuInputRequest{
			Percent: float32(s.cpu.percent),
		},
		Ram: &pb.StatsRamInputRequest{
			Total:     s.ram.total,
			Available: s.ram.available,
			Used:      s.ram.used,
		},
		Os: &pb.StatsOsInputRequest{
			HostID:          s.os.hostID,
			Os:              s.os.os,
			Platform:        s.os.platform,
			PlatformVersion: s.os.platformVersion,
			Processes:       s.os.processes,
		},
	}
}

type statsCollector struct {
	interval time.Duration
	data     chan statsData
}

func newStatsCollector(interval time.Duration) *statsCollector {
	return &statsCollector{
		interval: interval,
		data:     make(chan statsData),
	}
}

func (s *statsCollector) start(ctx context.Context) {
	ticker := time.NewTicker(s.interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			s.collectStats(ctx)
		}
	}
}

func (s *statsCollector) collectStats(ctx context.Context) {
	d := statsData{}
	d.cpu, _ = s.getCpuPercent()
	d.ram, _ = s.getRamData()
	d.os, _ = s.getOsData()
	d.timestamp = time.Now().Unix()

	select {
	case <-ctx.Done():
	case s.data <- d:
	default:
		log.Println("Data channel is full, dropping data!")
	}
}

func (s *statsCollector) getCpuPercent() (statsCpu, error) {
	c, err := cpu.Percent(s.interval, false)
	if len(c) != 1 {
		return statsCpu{}, errors.New("invalid cpu cores amount")
	}

	return statsCpu{percent: c[0]}, err
}

func (s *statsCollector) getRamData() (statsRam, error) {
	m, err := mem.VirtualMemory()
	if err != nil {
		return statsRam{}, err
	}

	return statsRam{
		total:     m.Total,
		available: m.Available,
		used:      m.Used,
	}, err
}

func (s *statsCollector) getOsData() (statsOs, error) {
	o, err := host.Info()
	if err != nil {
		return statsOs{}, err
	}

	return statsOs{
		hostID:          o.HostID,
		os:              o.OS,
		platform:        o.Platform,
		platformVersion: o.PlatformVersion,
		processes:       o.Procs,
	}, err
}
