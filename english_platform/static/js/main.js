document.addEventListener("DOMContentLoaded", () => {
    const burger = document.getElementById("burger-toggle");
    const sidebar = document.getElementById("sidebar");

    if (burger && sidebar) {
        burger.addEventListener("click", (e) => {
            e.stopPropagation();
            sidebar.classList.toggle("sidebar--open");
        });

        document.addEventListener("click", (e) => {
            if (
                sidebar.classList.contains("sidebar--open") &&
                !sidebar.contains(e.target) &&
                e.target !== burger
            ) {
                sidebar.classList.remove("sidebar--open");
            }
        });
    }

    setTimeout(() => {
        document.querySelectorAll(".alert").forEach((el) => {
            el.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            el.style.opacity = "0";
            el.style.transform = "translateY(-6px)";
            setTimeout(() => el.remove(), 400);
        });
    }, 5000);
});
