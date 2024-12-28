document.addEventListener('DOMContentLoaded', initializeUsageCard);

function initializeUsageCard() {
    const usageCard = document.getElementById('usage-card');
    const hostId = usageCard?.getAttribute('data-host-id');
    const limitSelect = document.getElementById('usage-limit');
    const tableBody = document.querySelector('#usage-stats-table tbody');

    if (!hostId) return logError('Host ID not found in usage-card');

    limitSelect.addEventListener('change', () => updateUsageTable(hostId, limitSelect.value, tableBody));
    updateUsageTable(hostId, limitSelect.value, tableBody);
}

async function fetchUsageData(hostId, limit) {
    try {
        const response = await fetch(`/api/host/${hostId}/stats-data/?limit=${limit}`);
        if (!response.ok) throw new Error(`HTTP error: ${response.statusText}`);
        const data = await response.json();
        return data.stats || [];
    } catch (error) {
        logError('Error fetching usage data:', error);
        return [];
    }
}

function renderUsageTable(tableBody, stats) {
    tableBody.innerHTML = stats
        .map(stat => `
            <tr>
                <td id="time">${formatDate(stat.time)}</td>
                <td>${stat.cpu_percent.toFixed(2)}</td>
                <td>${formatMB(stat.ram_total)}</td>
                <td>${formatMB(stat.ram_available)}</td>
                <td>${formatMB(stat.ram_used)}</td>
                <td>${stat.processes}</td>
            </tr>
        `)
        .join('');
}


async function updateUsageTable(hostId, limit, tableBody) {
    const stats = await fetchUsageData(hostId, limit);
    renderUsageTable(tableBody, stats);
}


function formatDate(dateStr) {
    return new Date(dateStr).toLocaleString();
}


function formatMB(bytes) {
    return (bytes / (1024 * 1024)).toFixed(0);
}

function logError(message, error) {
    console.error(message, error || '');
}
