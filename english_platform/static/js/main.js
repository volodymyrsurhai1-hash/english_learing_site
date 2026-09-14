document.addEventListener("DOMContentLoaded", () => {
    const burger = document.getElementById("burger-toggle");
    const sidebar = document.getElementById("sidebar");

    if (burger && sidebar) {
        burger.addEventListener("click", () => {
            sidebar.classList.toggle("sidebar--open");
        });
    }
});
