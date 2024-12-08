package client

import (
	"context"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/client"
	"github.com/marcinkonwiak/monitoring-client/pb"
	"github.com/shirou/gopsutil/v4/cpu"
	"github.com/shirou/gopsutil/v4/host"
	"github.com/shirou/gopsutil/v4/mem"
	"github.com/shirou/gopsutil/v4/process"
	"log"
	"sync"
	"time"
)

type statsData struct {
	Timestamp  int64
	Cpu        statsCpu
	Ram        statsRam
	Os         statsOs
	Processes  []processData
	Containers []containerData
}

type statsCpu struct {
	Percent float64
}

type statsRam struct {
	Total     uint64
	Available uint64
	Used      uint64
}

type statsOs struct {
	HostID          string
	Os              string
	Platform        string
	PlatformVersion string
	Processes       uint64
}

type processData struct {
	Pid  int32
	Name string
	Cpu  float64
	Mem  float32
}

type containerData struct {
	ID    string
	Name  string
	Image string
}

func (s statsData) toRequestData() *pb.StatsDataInputRequest {
	processes := make([]*pb.ProcessInputRequest, 0, len(s.Processes))
	for _, p := range s.Processes {
		processes = append(processes, &pb.ProcessInputRequest{
			Pid:  p.Pid,
			Name: p.Name,
			Cpu:  float32(p.Cpu),
			Mem:  p.Mem,
		})
	}

	containers := make([]*pb.ContainerInputRequest, 0, len(s.Containers))
	for _, c := range s.Containers {
		containers = append(containers, &pb.ContainerInputRequest{
			ID:    c.ID,
			Name:  c.Name,
			Image: c.Image,
		})
	}

	return &pb.StatsDataInputRequest{
		Timestamp: int32(s.Timestamp),
		Cpu: &pb.StatsCpuInputRequest{
			Percent: float32(s.Cpu.Percent),
		},
		Ram: &pb.StatsRamInputRequest{
			Total:     s.Ram.Total,
			Available: s.Ram.Available,
			Used:      s.Ram.Used,
		},
		Os: &pb.StatsOsInputRequest{
			HostID:          s.Os.HostID,
			Os:              s.Os.Os,
			Platform:        s.Os.Platform,
			PlatformVersion: s.Os.PlatformVersion,
			Processes:       s.Os.Processes,
		},
		Processes:  processes,
		Containers: containers,
	}
}

type statsCollector struct {
	interval     time.Duration
	data         chan statsData
	dockerClient *client.Client
}

func newStatsCollector(interval time.Duration) *statsCollector {
	dc, err := client.NewClientWithOpts(client.FromEnv)
	if err != nil {
		log.Printf("Docker stats not available")
	}

	return &statsCollector{
		interval:     interval,
		data:         make(chan statsData),
		dockerClient: dc,
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
	var wg sync.WaitGroup
	var mu sync.Mutex

	d := statsData{}
	d.Timestamp = time.Now().Unix()

	wg.Add(4)
	go s.getCpuData(&d.Cpu, &wg, &mu)
	go s.getRamData(&d.Ram, &wg, &mu)
	go s.getOsData(&d.Os, &wg, &mu)
	go s.getProcessesData(&d, &wg, &mu)
	if s.dockerClient != nil {
		wg.Add(1)
		go s.getContainersData(&d, &wg, &mu)
	}

	wg.Wait()

	select {
	case <-ctx.Done():
	case s.data <- d:
	default:
		log.Println("Data channel is full, dropping data!")
	}
}

func (s *statsCollector) getCpuData(d *statsCpu, wg *sync.WaitGroup, mu *sync.Mutex) {
	defer wg.Done()

	c, err := cpu.Percent(s.interval, false)
	if err != nil {
		log.Printf("Failed to collect data: %v\n", err)
		return
	}

	if len(c) != 1 {
		log.Println("Invalid cpu cores data")
		return
	}

	mu.Lock()
	d.Percent = c[0]
	mu.Unlock()
}

func (s *statsCollector) getRamData(d *statsRam, wg *sync.WaitGroup, mu *sync.Mutex) {
	defer wg.Done()

	m, err := mem.VirtualMemory()
	if err != nil {
		log.Printf("Failed to collect data: %v\n", err)
		return
	}

	mu.Lock()
	d.Total = m.Total
	d.Available = m.Available
	d.Used = m.Used
	mu.Unlock()
}

func (s *statsCollector) getOsData(d *statsOs, wg *sync.WaitGroup, mu *sync.Mutex) {
	defer wg.Done()

	o, err := host.Info()
	if err != nil {
		log.Printf("Failed to collect data: %v\n", err)
		return
	}

	mu.Lock()
	d.HostID = o.HostID
	d.Os = o.OS
	d.Platform = o.Platform
	d.PlatformVersion = o.PlatformVersion
	d.Processes = o.Procs
	mu.Unlock()
}

func (s *statsCollector) getProcessesData(d *statsData, wg *sync.WaitGroup, mu *sync.Mutex) {
	defer wg.Done()

	procs, err := process.Processes()
	if err != nil {
		log.Printf("Failed to collect data: %v\n", err)
		return
	}

	for _, p := range procs {
		pName, err := p.Name()
		if err != nil {
			log.Printf("Failed to collect data: %v\n", err)
			return
		}

		pCpu, err := p.CPUPercent()
		if err != nil {
			log.Printf("Failed to collect data: %v\n", err)
			return
		}

		pMem, err := p.MemoryPercent()
		if err != nil {
			log.Printf("Failed to collect data: %v\n", err)
			return
		}

		mu.Lock()
		d.Processes = append(d.Processes, processData{
			Pid:  p.Pid,
			Name: pName,
			Cpu:  pCpu,
			Mem:  pMem,
		})
		mu.Unlock()
	}
}

func (s *statsCollector) getContainersData(d *statsData, wg *sync.WaitGroup, mu *sync.Mutex) {
	defer wg.Done()

	containers, err := s.dockerClient.ContainerList(
		context.Background(), container.ListOptions{},
	)
	if err != nil {
		log.Printf("Failed to get docker containers: %v\n", err)
		return
	}

	for _, c := range containers {
		mu.Lock()
		d.Containers = append(d.Containers, containerData{
			ID:    c.ID,
			Name:  c.Names[0],
			Image: c.Image,
		})
		mu.Unlock()
	}
}
