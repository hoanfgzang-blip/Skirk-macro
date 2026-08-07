const BUILTIN_COMBOS = [
    "C0:  Combo Skirk C0 EQA 120fps",
    "C0:  Combo Skirk C0 EA 120fps",
    "C0:  Combo Skirk C0 EQA 60fps"
];


function formatKey(key) {
    if (!key) return "";
    const map = {
        shift: "Shift", ctrl: "Ctrl", alt: "Alt", caps_lock: "CapsLock",
        space: "Space", enter: "Enter", esc: "Esc", delete: "Delete",
        middle: "Mouse Middle"
    };
    if (map[key]) return map[key];
    if (/^f\d+$/i.test(key)) return key.toUpperCase();
    if (/^mouse_\d+$/.test(key)) return `mouse_${key.slice(6)}`;
    return key.length === 1 ? key.toUpperCase() : key;
}

async function loadAndRenderBoundCombos() {
    let config = { comboSignKeys: {}, customCombos: [] };
    try {
        const res = await fetch("http://localhost:5000/config");
        if (res.ok) {
            config = await res.json();
        } else {
            throw new Error();
        }
    } catch {
        try {
            config.comboSignKeys = JSON.parse(localStorage.getItem("comboSignKeys") || "{}");
            config.customCombos = JSON.parse(localStorage.getItem("customCombos") || "[]");
        } catch {}
    }

    const boundCombos = [];

    // Built-in combos with bound keys
    BUILTIN_COMBOS.forEach((comboStr, idx) => {
        const key = config.comboSignKeys && config.comboSignKeys[comboStr];
        if (key) {
            boundCombos.push({
                name: `Combo ${idx + 1}: ${comboStr}`,
                key: formatKey(key)
            });
        }
    });

    // Custom combos with bound keys
    const customCombos = Array.isArray(config.customCombos) ? config.customCombos : [];
    customCombos.forEach((c) => {
        if (c.hotkey) {
            boundCombos.push({
                name: c.name || "Custom Combo",
                key: formatKey(c.hotkey)
            });
        }
    });

    const container = document.getElementById("boundCombosList");
    if (!container) return;

    if (boundCombos.length === 0) {
        container.innerHTML = `<div class="text-on-surface-variant/60 text-sm py-4 text-center">Chưa có combo nào được bind phím.</div>`;
        return;
    }

    // Slice max 4 items ("nhiều combo quá thì cũng bỏ qua")
    const displayCombos = boundCombos.slice(0, 4);

    container.innerHTML = displayCombos.map(item => `
        <div class="flex items-center justify-between p-3 rounded-lg bg-surface-container-high border border-outline/30 hover:border-teal/50 transition-colors">
            <span class="font-medium text-sm text-on-surface truncate max-w-[220px]" title="${item.name}">${item.name}</span>
            <span class="px-2.5 py-1 text-xs font-mono bg-teal/15 text-teal border border-teal/40 rounded flex items-center gap-1 font-semibold">
                <span>⌨</span> ${item.key}
            </span>
        </div>
    `).join("");

    // Update FPS input if loaded
    const fpsInput = document.getElementById("macroFpsInput");
    if (fpsInput && config.FPS) {
        fpsInput.value = config.FPS;
    }
}

// ── Status & FPS Manager ──────────────────────────────────────────────────────
async function saveMacroFps() {
    const fpsInput = document.getElementById("macroFpsInput");
    const msgEl = document.getElementById("fpsSaveMsg");
    if (!fpsInput) return;

    const val = Number(fpsInput.value) || 120;
    localStorage.setItem("FPS", val);

    let currentConfig = {};
    try {
        const res = await fetch("http://localhost:5000/config");
        if (res.ok) currentConfig = await res.json();
    } catch {}

    currentConfig.FPS = val;
    currentConfig.comboSignKeys = currentConfig.comboSignKeys || JSON.parse(localStorage.getItem("comboSignKeys") || "{}");
    currentConfig.customCombos = currentConfig.customCombos || JSON.parse(localStorage.getItem("customCombos") || "[]");

    try {
        await fetch("http://localhost:5000/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(currentConfig)
        });
        if (msgEl) {
            msgEl.textContent = `✓ Đã lưu FPS: ${val}`;
            setTimeout(() => { msgEl.textContent = ""; }, 2500);
        }
    } catch {
        if (msgEl) {
            msgEl.textContent = `! Đã lưu cục bộ FPS: ${val}`;
            setTimeout(() => { msgEl.textContent = ""; }, 2500);
        }
    }
}

async function checkBackendStatus() {
    const badge = document.getElementById("backendStatusBadge");
    const dot = document.getElementById("backendStatusDot");
    const text = document.getElementById("backendStatusText");
    if (!badge || !dot || !text) return;

    try {
        const res = await fetch("http://localhost:5000/config", { method: "GET", signal: AbortSignal.timeout(1500) });
        if (res.ok) {
            badge.className = "inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-semibold transition-all bg-teal/15 text-teal border-teal/40";
            dot.className = "w-2 h-2 rounded-full bg-teal animate-pulse";
            text.textContent = "Backend ổn định";
        } else {
            throw new Error();
        }
    } catch {
        badge.className = "inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-semibold transition-all bg-red-500/15 text-red-400 border-red-500/40";
        dot.className = "w-2 h-2 rounded-full bg-red-400 animate-ping";
        text.textContent = "Backend crash";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const heroImage = document.getElementById('hero-image');
    const heroContainer = document.getElementById('hero-container');
    
    if (heroImage && heroContainer) {
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
            const containerHeight = heroContainer.offsetHeight;
            let opacity = 1 - (scrollY / (containerHeight * 0.8));
            opacity = Math.max(0, Math.min(1, opacity));
            let scale = 1.05 + (scrollY * 0.0002);
            scale = Math.min(1.15, scale);
            heroImage.style.opacity = opacity;
            heroImage.style.transform = `scale(${scale})`;
        });
    }
    // Bind FPS Save button & Enter key
    const saveFpsBtn = document.getElementById("saveFpsBtn");
    const macroFpsInput = document.getElementById("macroFpsInput");
    if (saveFpsBtn) saveFpsBtn.addEventListener("click", saveMacroFps);
    if (macroFpsInput) {
        macroFpsInput.value = localStorage.getItem("FPS") || "120";
        macroFpsInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") saveMacroFps();
        });
    }

    loadAndRenderBoundCombos();
    checkBackendStatus();
    setInterval(checkBackendStatus, 2500);
});
