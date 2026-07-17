const COMBO_ACTIONS = Object.freeze([
    { label: "n3w", pythonFunction: "skk3aw" },
    { label: "n2d", pythonFunction: "skk2as" },
    { label: "n3d", pythonFunction: "skk3as" },
    { label: "n2c", pythonFunction: "skk2az" },
    { label: "n2cd", pythonFunction: "skk2azs" },
    { label: "n2cd_slow", pythonFunction: "skk2azs_slow" },
    { label: "n2q", pythonFunction: "skk2aq" },
    { label: "E", pythonFunction: "skke" },
    { label: "n5d", pythonFunction: "skk5as" }
]);

const ACTION_LABEL_MAP = new Map(
    COMBO_ACTIONS.map(a => [a.pythonFunction, a.label])
);

const BACKEND_URL = "http://localhost:5000";

let allCombos = [];
let fullConfig = {};
let pendingDeleteId = null;

const el = {};

document.addEventListener("DOMContentLoaded", async () => {
    Object.assign(el, {
        comboList: document.getElementById("comboList"),
        emptyState: document.getElementById("emptyState"),
        deleteModal: document.getElementById("deleteModal"),
        deleteModalText: document.getElementById("deleteModalText"),
        cancelDelete: document.getElementById("cancelDelete"),
        confirmDelete: document.getElementById("confirmDelete")
    });

    el.cancelDelete.addEventListener("click", closeDeleteModal);
    el.confirmDelete.addEventListener("click", confirmDeleteCombo);
    el.deleteModal.addEventListener("click", (e) => {
        if (e.target === el.deleteModal) closeDeleteModal();
    });

    await loadCombos();
    renderCombos();
});

async function loadCombos() {
    try {
        const res = await fetch(`${BACKEND_URL}/config`);
        if (!res.ok) throw new Error();
        fullConfig = await res.json();
        allCombos = Array.isArray(fullConfig.customCombos) ? fullConfig.customCombos : [];
        // Sync to localStorage as well
        localStorage.setItem("customCombos", JSON.stringify(allCombos));
    } catch {
        // Fallback to localStorage
        try {
            allCombos = JSON.parse(localStorage.getItem("customCombos")) || [];
        } catch { allCombos = []; }
        fullConfig = {
            comboSignKeys: JSON.parse(localStorage.getItem("comboSignKeys") || "{}"),
            FPS: Number(localStorage.getItem("FPS")) || 120,
            customCombos: allCombos
        };
    }
}

function renderCombos() {
    el.comboList.innerHTML = "";
    el.emptyState.hidden = allCombos.length > 0;

    allCombos.forEach((combo) => {
        const card = document.createElement("div");
        card.className = "combo-card";
        card.dataset.id = combo.id;

        const hotkeyDisplay = combo.hotkey
            ? `<span class="combo-hotkey has-key">⌨ ${formatHotkey(combo.hotkey)}</span>`
            : `<span class="combo-hotkey no-key">Chưa gán phím</span>`;

        const timelineTags = (combo.timeline || []).map(fn => {
            const label = ACTION_LABEL_MAP.get(fn) || fn;
            return `<span class="preview-tag">${label}</span>`;
        }).join("");

        card.innerHTML = `
            <div class="combo-info">
                <h3 class="combo-name">${escapeHtml(combo.name || "Unnamed")}</h3>
                <div class="combo-meta">
                    ${hotkeyDisplay}
                    <span class="combo-actions-count">${(combo.timeline || []).length} action</span>
                </div>
                <div class="combo-timeline-preview">${timelineTags}</div>
            </div>
            <div class="combo-card-actions">
                <button class="btn-edit" data-id="${combo.id}" type="button">✏️ Sửa</button>
                <button class="btn-delete" data-id="${combo.id}" data-name="${escapeHtml(combo.name || '')}" type="button">🗑 Xóa</button>
            </div>
        `;

        card.querySelector(".btn-edit").addEventListener("click", () => editCombo(combo.id));
        card.querySelector(".btn-delete").addEventListener("click", () => openDeleteModal(combo.id, combo.name));

        el.comboList.appendChild(card);
    });
}

function editCombo(id) {
    window.location.href = `cuscombo.html?edit=${id}`;
}

function openDeleteModal(id, name) {
    pendingDeleteId = id;
    el.deleteModalText.textContent = `Bạn có chắc muốn xóa combo "${name || 'Unnamed'}"?`;
    el.deleteModal.hidden = false;
}

function closeDeleteModal() {
    pendingDeleteId = null;
    el.deleteModal.hidden = true;
}

async function confirmDeleteCombo() {
    if (!pendingDeleteId) return;
    const id = pendingDeleteId;
    closeDeleteModal();

    allCombos = allCombos.filter(c => c.id !== id);
    fullConfig.customCombos = allCombos;
    localStorage.setItem("customCombos", JSON.stringify(allCombos));
    renderCombos();

    try {
        const res = await fetch(`${BACKEND_URL}/save`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(fullConfig)
        });
        if (!res.ok) throw new Error();
        showToast("Đã xóa combo.");
    } catch {
        showToast("Đã xóa cục bộ. Backend chưa phản hồi.", true);
    }
}

function formatHotkey(hotkey) {
    if (!hotkey) return "";
    const labels = {
        shift: "Shift", ctrl: "Ctrl", alt: "Alt", caps_lock: "CapsLock",
        space: "Space", enter: "Enter", esc: "Esc", delete: "Delete"
    };
    if (labels[hotkey]) return labels[hotkey];
    if (/^f\d+$/.test(hotkey)) return hotkey.toUpperCase();
    if (/^mouse_\d+$/.test(hotkey)) return `Mouse${hotkey.slice(6)}`;
    if (/^mouse\d+$/.test(hotkey)) return `Mouse${hotkey.slice(5)}`;
    return hotkey.length === 1 ? hotkey.toUpperCase() : hotkey;
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

function showToast(message, isError = false) {
    const existing = document.querySelector(".toast");
    if (existing) existing.remove();

    const toast = document.createElement("div");
    toast.className = `toast${isError ? " is-error" : ""}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("is-hidden");
        setTimeout(() => toast.remove(), 350);
    }, 2500);
}
