const searchInput = document.getElementById('search-list');
const hostCards = document.querySelectorAll('#host-list .card');

function filterCards() {
    const searchValue = searchInput.value.toLowerCase();

    hostCards.forEach(card => {
        const hostId = card.getAttribute('data-host-id').toLowerCase();
        const hostOs = card.getAttribute('data-host-os').toLowerCase();

        const matches = hostId.includes(searchValue) || hostOs.includes(searchValue);

        if (matches) {
            card.parentElement.style.display = '';
        } else {
            card.parentElement.style.display = 'none';
        }
    });
}

searchInput.addEventListener('input', filterCards);