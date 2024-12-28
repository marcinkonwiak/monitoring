let ramChart;

function initializeRamChart() {
    const ctx = document.getElementById('ram-chart').getContext('2d');
    ramChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'RAM Used (MB)',
                data: [],
                borderColor: '#4caf50',
                backgroundColor: 'rgba(76, 175, 80, 0.2)',
                fill: true,
                tension: 0.4,
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute',
                    },
                    title: {display: true, text: 'Time'},
                },
                y: {
                    title: {display: true, text: 'RAM Used (MB)'},
                    ticks: {
                        callback: value => `${value.toFixed(0)} MB`,
                    },
                },
            },
        },
    });
}


async function fetchRamData(hostId, limit) {
    try {
        const response = await fetch(`/api/host/${hostId}/stats-data/?limit=${limit}`);
        if (!response.ok) {
            console.error('Failed to fetch RAM data');
            return [];
        }
        const data = await response.json();
        console.log('Fetched RAM data:', data);
        return data.stats.map(stat => ({
            time: new Date(stat.time),
            ramUsed: stat.ram_used,
        }));
    } catch (error) {
        console.error('Error fetching RAM data:', error);
        return [];
    }
}

async function updateRamChart(hostId, limit) {
    const ramData = await fetchRamData(hostId, limit);
    if (ramChart) {
        ramChart.data.labels = ramData.map(data => data.time);
        ramChart.data.datasets[0].data = ramData.map(data => data.ramUsed / (1024 * 1024));
        ramChart.update();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const ramChartContainer = document.getElementById('ram-chart-container');
    const hostId = ramChartContainer.getAttribute('data-host-id');
    const limitSelect = document.getElementById('ram-data-limit');

    initializeRamChart();
    updateRamChart(hostId, limitSelect.value);

    limitSelect.addEventListener('change', () => {
        updateRamChart(hostId, limitSelect.value);
    });
});
