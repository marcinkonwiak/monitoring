function updateCpuChart(cpuPercent) {
    const chart = document.getElementById("cpu-chart");
    const cpuValue = document.getElementById("cpu-value");

    chart.innerHTML = '';
    const roundedCpuPercent = Math.round(cpuPercent);
    const activeSquares = Math.floor(roundedCpuPercent / 5);

    for (let i = 0; i < 20; i++) {
        const square = document.createElement('div');
        square.classList.add('cpu-square');
        if (i < activeSquares) square.classList.add('active');
        chart.appendChild(square);
    }

    cpuValue.textContent = `${roundedCpuPercent}%`;
}

export { updateCpuChart };
