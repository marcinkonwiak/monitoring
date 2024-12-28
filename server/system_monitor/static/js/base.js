document.addEventListener("DOMContentLoaded", function () {
    const toggleSidebarBtn = document.getElementById("toggle-sidebar-btn");
    const sidebar = document.querySelector(".sidebar");

toggleSidebarBtn.addEventListener("click", function () {
    sidebar.classList.toggle("hidden");
    if (document.getElementById("search-modal").style.display === "block") {
        const updateModalPositionEvent = new Event("resize");
        window.dispatchEvent(updateModalPositionEvent);
    }
});

});