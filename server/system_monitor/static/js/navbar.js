document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.search-input');
    const modal = document.getElementById('search-modal');
    const modalContent = document.querySelector('.modal-content');
    const hostItems = document.querySelectorAll('.host-item');
    const section = document.getElementById('section');

    const updateModalPosition = () => {
        const rect = searchInput.getBoundingClientRect();
        modal.style.top = `${rect.bottom + window.scrollY}px`;
        modal.style.left = `${rect.left + window.scrollX}px`;
        modal.style.width = `${rect.width}px`;
    };

    const filterHosts = (query) => {
        const lowerCaseQuery = query.toLowerCase();
        let hasResults = false;

        hostItems.forEach(hostItem => {
            const hostId = hostItem.getAttribute('data-host-id').toLowerCase();
            const hostOs = hostItem.getAttribute('data-host-os').toLowerCase();
            if (hostId.includes(lowerCaseQuery) || hostOs.includes(lowerCaseQuery)) {
                hostItem.style.display = 'block';
                hasResults = true;
            } else {
                hostItem.style.display = 'none';
            }
        });

        const noResultsElement = document.getElementById('no-results');
        if (hasResults) {
            noResultsElement.style.display = 'none';
        } else {
            noResultsElement.style.display = 'block';
        }
    };

    searchInput.addEventListener('input', () => {
        const query = searchInput.value;
        if (query.length > 0) {
            modal.style.display = 'block';
            section.classList.add('blurred');
            filterHosts(query);
            updateModalPosition();
        } else {
            modal.style.display = 'none';
            section.classList.remove('blurred');
        }
    });

    window.addEventListener('resize', () => {
        if (modal.style.display === 'block') {
            updateModalPosition();
        }
    });

    window.addEventListener('scroll', () => {
        if (modal.style.display === 'block') {
            updateModalPosition();
        }
    });

    window.addEventListener('click', (event) => {
        if (!modal.contains(event.target) && event.target !== searchInput) {
            modal.style.display = 'none';
            section.classList.remove('blurred');
        }
    });
});
