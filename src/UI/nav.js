document.addEventListener("DOMContentLoaded", () => {
    const currentPage = window.location.pathname.split("/").pop() || "index.html";

    const pages = [
        { href: "index.html", icon: "🎮", label: "Combo chính" },
        { href: "cuscombo.html", icon: "✨", label: "Tạo Custom Combo" },
        { href: "manage.html", icon: "📋", label: "Quản lý Combo" }
    ];

    const nav = document.createElement("aside");
    nav.className = "sidebar";
    nav.innerHTML = `
        <div class="sidebar-logo">
            <img src="icon.png" alt="Skirk Macro">
            <span>Skirk Macro</span>
        </div>
        <nav class="sidebar-nav">
            ${pages.map(p => `
                <a href="${p.href}" class="nav-link${currentPage === p.href ? ' active' : ''}">
                    <span class="nav-icon">${p.icon}</span>
                    <span>${p.label}</span>
                </a>
            `).join("")}
        </nav>
        <div class="sidebar-footer">Skirk Macro v0.8</div>
    `;

    // Wrap existing body content in main-content div
    const mainContent = document.createElement("div");
    mainContent.className = "main-content";
    while (document.body.firstChild) {
        mainContent.appendChild(document.body.firstChild);
    }
    document.body.appendChild(nav);
    document.body.appendChild(mainContent);
    document.body.classList.add("app-layout");
});
