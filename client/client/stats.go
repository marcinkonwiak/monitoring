package client

import (
	"context"
	"errors"
	"fmt"
	"github.com/shirou/gopsutil/v4/cpu"
	"github.com/shirou/gopsutil/v4/host"
	"github.com/shirou/gopsutil/v4/mem"
	"time"
)

// - czas działania systemu,
// - użycie CPU,
// - użycie pamięci RAM,
// - użycie miejsca na dysku,
// - liczba działających procesów,
// - dla każdego kontenera docker uruchomionego w systemie: użycie CPU, użycie pamięci RAM, liczba działających procesów.

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
	os              string
	platform        string
	platformVersion string
	processes       uint64
}

type statsCollector struct {
	interval time.Duration
	data     chan []statsData
}

func newStatsCollector(interval time.Duration) *statsCollector {
	return &statsCollector{
		interval: interval,
		data:     make(chan []statsData),
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
			s.collectStats()
		}
	}
}

func (s *statsCollector) collectStats() statsData {
	d := statsData{}
	d.cpu, _ = s.getCpuPercent()
	d.ram, _ = s.getRamData()
	d.os, _ = s.getOsData()

	fmt.Printf("%+v\n", d)

	return d
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
		os:              o.OS,
		platform:        o.Platform,
		platformVersion: o.PlatformVersion,
		processes:       o.Procs,
	}, err
}
