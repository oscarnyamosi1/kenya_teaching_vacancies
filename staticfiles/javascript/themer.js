// Set the theme
function setTheme(theme) {
    const themeLink = document.getElementById("theme-style");
    if (themeLink) {
        themeLink.href = `/static/styling/themes/${theme}.css`;
    }
    localStorage.setItem("theme", theme);
}

// Initialize theme and bind buttons
document.addEventListener("DOMContentLoaded", () => {
    // 1. Apply saved theme or default
    const savedTheme = localStorage.getItem("theme");
    const themeToUse = savedTheme || 'macglass';
    setTheme(themeToUse);

    // 2. Bind click events using querySelectorAll
    const buttons = document.querySelectorAll(".menu-item[data-theme]");
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            const theme = btn.getAttribute("data-theme");
            setTheme(theme);
        });
    });
});