document.addEventListener('DOMContentLoaded', () => {
    const showProcessesBtn = document.getElementById('show-processes-btn');
    const modal = document.getElementById('processes-modal');
    const processesList = document.getElementById('processes-list');
    const searchInput = document.getElementById('process-search');
    const section = document.querySelector('#section');
    const hostId = showProcessesBtn.getAttribute('data-host-id');

    function adjustModalWidth() {
        const sectionWidth = section.offsetWidth;
        modal.style.width = `${sectionWidth}px`;
        modal.style.left = `${section.offsetLeft}px`;
    }

    const resizeObserver = new ResizeObserver(() => {
        if (modal.style.display === 'flex') {
            adjustModalWidth();
        }
    });

    resizeObserver.observe(section);

    async function fetchProcesses(nameQuery = '') {
        const queryParams = new URLSearchParams({
            host_id: hostId,
            ...(nameQuery && { name: nameQuery })
        });

        try {
            const response = await fetch(`/api/host-processes/?${queryParams}`);
            if (!response.ok) throw new Error('Failed to fetch processes');

            const processes = await response.json();

            processesList.innerHTML = processes.map(process => `
                <tr>
                    <td>${process.pid}</td>
                    <td>${process.name}</td>
                    <td>${process.cpu.toFixed(2)}%</td>
                    <td>${process.mem.toFixed(2)}%</td>
                </tr>
            `).join('');
        } catch (error) {
            console.error('Error fetching processes:', error);
            processesList.innerHTML = '<tr><td colspan="4">Failed to load processes</td></tr>';
        }
    }

    showProcessesBtn.addEventListener('click', () => {
        fetchProcesses();
        modal.style.display = 'flex';
        adjustModalWidth();
    });

    searchInput.addEventListener('input', (event) => {
        const nameQuery = event.target.value;
        fetchProcesses(nameQuery);
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});
