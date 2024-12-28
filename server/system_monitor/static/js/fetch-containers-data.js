document.addEventListener('DOMContentLoaded', () => {
    const containersTableBody = document.querySelector('#containers-table tbody');
    const hostId = document.getElementById('show-processes-btn').getAttribute('data-host-id');

    async function fetchContainers() {
        try {
            const response = await fetch(`/api/host-containers/?host_id=${hostId}`);
            if (!response.ok) throw new Error('Failed to fetch containers data');

            const data = await response.json();

            if (data.message === "No containers found" || data.length === 0) {
                containersTableBody.innerHTML = `
                    <tr>
                        <td colspan="3" style="text-align: center;">No containers available</td>
                    </tr>`;
                return;
            }

            containersTableBody.innerHTML = data.map(container => `
                <tr>
                    <td>${container.id}</td>
                    <td>${container.name}</td>
                    <td>${container.image}</td>
                </tr>
            `).join('');
        } catch (error) {
            console.error('Error fetching containers:', error);
            containersTableBody.innerHTML = `
                <tr>
                    <td colspan="3" style="text-align: center;">Failed to load containers data</td>
                </tr>`;
        }
    }

    fetchContainers();
});
