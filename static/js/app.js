const THEME_STORAGE_KEY = "tourismo-theme";

function getPreferredTheme() {
    const saved = localStorage.getItem(THEME_STORAGE_KEY);
    if (saved === "light" || saved === "dark") {
        return saved;
    }

    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_STORAGE_KEY, theme);

    const icon = document.querySelector("#theme-toggle i");
    if (icon) {
        icon.className = theme === "dark" ? "fas fa-sun" : "fas fa-moon";
    }

    document.dispatchEvent(new CustomEvent("theme:changed", { detail: { theme } }));
}

function setupThemeToggle() {
    const toggle = document.getElementById("theme-toggle");
    if (!toggle) {
        return;
    }

    toggle.addEventListener("click", () => {
        const current = document.documentElement.getAttribute("data-theme") || "light";
        applyTheme(current === "dark" ? "light" : "dark");
    });
}

function setupMobileSidebar() {
    const button = document.getElementById("mobile-menu-btn");
    const sidebar = document.getElementById("sidebar");

    if (!button || !sidebar) {
        return;
    }

    button.addEventListener("click", () => {
        sidebar.classList.toggle("mobile-open");
    });

    document.addEventListener("click", (event) => {
        const isInsideSidebar = sidebar.contains(event.target);
        const isButton = button.contains(event.target);
        if (!isInsideSidebar && !isButton) {
            sidebar.classList.remove("mobile-open");
        }
    });
}

(function initLayout() {
    applyTheme(getPreferredTheme());
    setupThemeToggle();
    setupMobileSidebar();
})();
