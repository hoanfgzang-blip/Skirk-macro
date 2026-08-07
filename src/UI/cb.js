const BUILTIN_COMBOS = [
    "C0:  Combo Skirk C0 EQA 120fps",
    "C0:  Combo Skirk C0 EA 120fps",
    "C0:  Combo Skirk C0 EQA 60fps"
];

let currentConfig = { comboSignKeys: {}, FPS: 120, customCombos: [] };
let activeBindingTarget = null; // { isBuiltin, comboStr, id, name }
let keyCaptureKeyHandler = null;
let keyCaptureMouseHandler = null;
let comboLoaded = false;

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

function resolveKeyName(e) {
    // ── Mouse ────────────────────────────────────────────────────────────
    if (e.type === "mousedown") {
        // Chuột trái (0) và chuột phải (2) KHÔNG gán làm hotkey
        if (e.button === 0 || e.button === 2) return null;
        const mouseMap = { 1: "middle" };
        return mouseMap[e.button] ?? `mouse_${e.button}`;
    }

    // ── Keyboard ─────────────────────────────────────────────────────────
    const codeMap = {
        "ShiftLeft": "shift", "ShiftRight": "shift_r",
        "ControlLeft": "ctrl", "ControlRight": "ctrl_r",
        "AltLeft": "alt", "AltRight": "alt_gr",
        "MetaLeft": "cmd", "MetaRight": "cmd_r",
        "CapsLock": "caps_lock", "NumLock": "num_lock", "ScrollLock": "scroll_lock",
        "Space": "space", "Enter": "enter", "Backspace": "backspace",
        "Tab": "tab", "Escape": "esc", "Delete": "delete", "Insert": "insert",
        "Home": "home", "End": "end", "PageUp": "page_up", "PageDown": "page_down",
        "ArrowUp": "up", "ArrowDown": "down", "ArrowLeft": "left", "ArrowRight": "right",
        "PrintScreen": "print_screen", "Pause": "pause",
        "F1": "f1", "F2": "f2", "F3": "f3", "F4": "f4", "F5": "f5",
        "F6": "f6", "F7": "f7", "F8": "f8", "F9": "f9", "F10": "f10",
        "F11": "f11", "F12": "f12", "F13": "f13", "F14": "f14", "F15": "f15",
        "F16": "f16", "F17": "f17", "F18": "f18", "F19": "f19", "F20": "f20",
    };

    if (codeMap[e.code]) return codeMap[e.code];
    if (/^Key[A-Z]$/.test(e.code)) return e.code[3].toLowerCase();
    if (/^Digit[0-9]$/.test(e.code)) return e.code[5];
    if (/^Numpad\d$/.test(e.code)) return e.code[6];
    if (e.key && e.key.length === 1) return e.key.toLowerCase();
    return e.code ?? e.key;
}

async function fetchConfig() {
    try {
        const res = await fetch("http://localhost:5000/config");
        if (res.ok) {
            currentConfig = await res.json();
            localStorage.setItem("comboSignKeys", JSON.stringify(currentConfig.comboSignKeys || {}));
            localStorage.setItem("customCombos", JSON.stringify(currentConfig.customCombos || []));
            return;
        }
    } catch {}

    currentConfig = {
        comboSignKeys: JSON.parse(localStorage.getItem("comboSignKeys") || "{}"),
        FPS: Number(localStorage.getItem("FPS")) || 120,
        customCombos: JSON.parse(localStorage.getItem("customCombos") || "[]")
    };
}

async function saveConfig() {
    localStorage.setItem("comboSignKeys", JSON.stringify(currentConfig.comboSignKeys || {}));
    localStorage.setItem("customCombos", JSON.stringify(currentConfig.customCombos || []));
    try {
        await fetch("http://localhost:5000/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(currentConfig)
        });
    } catch (e) {
        console.warn("Backend save error, saved to localStorage", e);
    }
}

function renderCombosFromConfig() {
    const allCombos = [];

    // Built-in combos
    BUILTIN_COMBOS.forEach((comboStr, idx) => {
        const key = currentConfig.comboSignKeys && currentConfig.comboSignKeys[comboStr];
        allCombos.push({
            id: `builtin_${idx}`,
            isBuiltin: true,
            comboStr: comboStr,
            name: `Combo ${idx + 1}: ${comboStr}`,
            key: key ? formatKey(key) : null,
            rawKey: key || null
        });
    });

    // Custom combos
    const customCombos = Array.isArray(currentConfig.customCombos) ? currentConfig.customCombos : [];
    customCombos.forEach((c) => {
        allCombos.push({
            id: c.id,
            isBuiltin: false,
            name: c.name || "Custom Combo",
            key: c.hotkey ? formatKey(c.hotkey) : null,
            rawKey: c.hotkey || null,
            actionCount: (c.timeline || []).length
        });
    });

    const grid = document.getElementById("comboGrid");
    if (!grid) return;

    grid.innerHTML = allCombos.map(combo => {
        const keyBadge = combo.key
            ? `<span class="px-3 py-1 text-xs font-mono bg-teal/15 text-teal border border-teal/40 rounded-md flex items-center gap-1.5 font-semibold">
                 <span>⌨</span> ${combo.key}
               </span>`
            : `<span class="px-3 py-1 text-xs font-mono bg-white/5 text-on-surface-variant/70 border border-outline/30 rounded-md">
                 Chưa gán phím
               </span>`;

        const badgeType = combo.isBuiltin
            ? `<span class="text-[11px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 font-medium">Mặc định</span>`
            : `<span class="text-[11px] px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20 font-medium">Tùy chỉnh (${combo.actionCount || 0} action)</span>`;

        const bindButton = `<button onclick="openKeyBindModal('${combo.id}')" class="text-xs px-3 py-1.5 rounded-lg bg-teal/10 text-teal hover:bg-teal/20 border border-teal/30 transition-colors flex items-center gap-1 font-medium" type="button">
            <span class="material-symbols-outlined text-sm">keyboard</span> ${combo.key ? 'Đổi phím' : 'Gán phím'}
        </button>`;

        const editTimelineBtn = !combo.isBuiltin
            ? `<button onclick="openComboModal('${combo.id}')" class="text-xs px-3 py-1.5 rounded-lg bg-surface-container-highest text-on-surface hover:text-teal hover:bg-teal/10 border border-outline/30 transition-colors flex items-center gap-1" type="button">
                 <span class="material-symbols-outlined text-sm">edit</span> Sửa timeline
               </button>`
            : '';

        const deleteBtn = !combo.isBuiltin
            ? `<button onclick="openDeleteModal('${combo.id}', '${combo.name.replace(/'/g, "\\'")}')"
                 class="text-xs px-3 py-1.5 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/30 transition-colors flex items-center gap-1" type="button">
                 <span class="material-symbols-outlined text-sm">delete</span> Xóa
               </button>`
            : '';

        return `
            <div class="bg-surface-container border border-outline/40 hover:border-teal/50 rounded-xl p-5 shadow-lg transition-all flex flex-col justify-between gap-4 group">
                <div>
                    <div class="flex items-center justify-between mb-3">
                        ${badgeType}
                        ${keyBadge}
                    </div>
                    <h3 class="font-semibold text-on-background text-base group-hover:text-teal transition-colors">${combo.name}</h3>
                </div>
                <div class="flex items-center justify-end gap-2 pt-3 border-t border-outline/20">
                    ${bindButton}
                    ${editTimelineBtn}
                    ${deleteBtn}
                </div>
            </div>
        `;
    }).join("");
}

// Load combo lần đầu (chỉ gọi 1 lần khi DOMContentLoaded)
async function initialLoadCombos() {
    if (comboLoaded) return;
    comboLoaded = true;
    await fetchConfig();
    renderCombosFromConfig();
}

// Reload thủ công (nút Reload hoặc sau khi thêm combo)
async function reloadCombos() {
    await fetchConfig();
    renderCombosFromConfig();
}

// ── Key Binding Modal Logic ──────────────────────────────────────────────────

// Chặn browser navigation khi modal đóng (không chặn khi CaptureMouse đang hoạt động
// vì keyCaptureMouseHandler cần nhận được các sự kiện mouse 3/4 để gán phím)
let _navBlockHandler = null;
function startNavBlock() {
    stopNavBlock();
    _navBlockHandler = (e) => {
        // Chỉ chặn khi KHÔNG đang trong chế độ capture phím
        if (keyCaptureMouseHandler) return;
        if (e.button === 3 || e.button === 4) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
        }
    };
    window.addEventListener('mousedown', _navBlockHandler, true);
    window.addEventListener('auxclick',  _navBlockHandler, true);
}
function stopNavBlock() {
    if (_navBlockHandler) {
        window.removeEventListener('mousedown', _navBlockHandler, true);
        window.removeEventListener('auxclick',  _navBlockHandler, true);
        _navBlockHandler = null;
    }
}

function openKeyBindModal(id) {
    let target = null;

    if (id.startsWith("builtin_")) {
        const idx = parseInt(id.replace("builtin_", ""), 10);
        const comboStr = BUILTIN_COMBOS[idx];
        target = {
            id,
            isBuiltin: true,
            comboStr,
            name: `Combo ${idx + 1}: ${comboStr}`
        };
    } else {
        const c = (currentConfig.customCombos || []).find(item => item.id === id);
        if (c) {
            target = {
                id: c.id,
                isBuiltin: false,
                name: c.name || "Custom Combo"
            };
        }
    }

    if (!target) return;
    activeBindingTarget = target;

    const modal = document.getElementById("keyBindModal");
    const title = document.getElementById("bindModalTitle");
    title.textContent = `Gán phím cho "${target.name}"`;

    modal.classList.remove("hidden");
    modal.classList.add("flex");

    // Chặn browser navigation ngay khi modal mở (trước cả khi click Gán phím)
    startNavBlock();
    startKeyCapture();
}

function closeKeyBindModal() {
    stopKeyCapture();
    stopNavBlock(); // Gỡ chặn navigation khi đóng modal
    activeBindingTarget = null;
    const modal = document.getElementById("keyBindModal");
    modal.classList.add("hidden");
    modal.classList.remove("flex");
}

function startKeyCapture() {
    stopKeyCapture();

    // ── Keyboard capture handler ─────────────────────────────────────────
    keyCaptureKeyHandler = async (e) => {
        e.preventDefault();
        e.stopPropagation();

        // Remove listeners immediately
        window.removeEventListener("keydown", keyCaptureKeyHandler, true);
        window.removeEventListener("mousedown", keyCaptureMouseHandler, true);

        // ESC → hủy, không gán
        if (e.code === "Escape") {
            closeKeyBindModal();
            return;
        }

        const keyName = resolveKeyName(e);
        if (!keyName || !activeBindingTarget) return;

        applyKeyBinding(keyName);
    };

    // ── Mouse capture handler ────────────────────────────────────────────
    keyCaptureMouseHandler = async (e) => {
        // 1. Chuột trái (button 0): cho phép bấm nút "Hủy" / "Xóa phím gán" trong modal
        if (e.button === 0) {
            const btn = e.target.closest("button");
            if (btn) {
                // Người dùng click vào nút UI -> gỡ listener capture để nút hoạt động bình thường
                stopKeyCapture();
            }
            return; // Không gán chuột trái làm bind key
        }

        // 2. Chuột phải (button 2): không gán, chặn menu ngữ cảnh
        if (e.button === 2) {
            e.preventDefault();
            e.stopPropagation();
            return;
        }

        // 3. Các nút chuột khác (Middle / Mouse 3 / Mouse 4 / Mouse N):
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();

        const keyName = resolveKeyName(e);
        const target  = activeBindingTarget; // lưu trước khi gỡ listener

        // Gỡ listener capture ngay lập tức
        stopKeyCapture();

        // Chặn mouseup/click tiếp theo tránh sự kiện dư thừa
        const preventNext = (ev) => { ev.preventDefault(); ev.stopPropagation(); };
        window.addEventListener('mouseup', preventNext, { capture: true, once: true });
        window.addEventListener('click',   preventNext, { capture: true, once: true });

        if (!keyName || !target) return;
        await applyKeyBinding(keyName, target);
    };

    window.addEventListener("keydown", keyCaptureKeyHandler, true);
    window.addEventListener("mousedown", keyCaptureMouseHandler, true);
}

async function applyKeyBinding(keyName, target) {
    // target có thể được truyền vào hoặc dùng activeBindingTarget
    const tgt = target || activeBindingTarget;
    if (!tgt) return;
    if (tgt.isBuiltin) {
        if (!currentConfig.comboSignKeys) currentConfig.comboSignKeys = {};
        currentConfig.comboSignKeys[tgt.comboStr] = keyName;
    } else {
        const c = (currentConfig.customCombos || []).find(item => item.id === tgt.id);
        if (c) c.hotkey = keyName;
    }

    await saveConfig();
    closeKeyBindModal();
    renderCombosFromConfig();
}

function stopKeyCapture() {
    if (keyCaptureKeyHandler) {
        window.removeEventListener("keydown", keyCaptureKeyHandler, true);
        keyCaptureKeyHandler = null;
    }
    if (keyCaptureMouseHandler) {
        window.removeEventListener("mousedown", keyCaptureMouseHandler, true);
        keyCaptureMouseHandler = null;
    }
}

async function clearCurrentBind() {
    if (!activeBindingTarget) return;

    if (activeBindingTarget.isBuiltin) {
        if (currentConfig.comboSignKeys) {
            delete currentConfig.comboSignKeys[activeBindingTarget.comboStr];
        }
    } else {
        const c = (currentConfig.customCombos || []).find(item => item.id === activeBindingTarget.id);
        if (c) delete c.hotkey;
    }

    await saveConfig();
    closeKeyBindModal();
    renderCombosFromConfig(); // Re-render từ config đã có
}

// ── Custom Combo Iframe Modal Logic ─────────────────────────────────────────
function openComboModal(editId) {
    const modal = document.getElementById("comboModal");
    const iframe = document.getElementById("comboIframe");
    let src = "cuscombo.html";
    if (editId) {
        src += `?edit=${editId}`;
    }
    iframe.src = src;
    modal.classList.remove("hidden");
    modal.classList.add("flex");
}

function closeComboModal() {
    const modal = document.getElementById("comboModal");
    const iframe = document.getElementById("comboIframe");
    iframe.src = "about:blank";
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    reloadCombos(); // Reload khi đóng modal thêm/sửa combo
}

// ── Delete Combo Modal Logic ────────────────────────────────────────────────
let pendingDeleteId = null;
let pendingDeleteName = null;

function openDeleteModal(id, name) {
    pendingDeleteId = id;
    pendingDeleteName = name;
    const modal = document.getElementById("deleteModal");
    const text = document.getElementById("deleteModalText");
    text.textContent = `Bạn có chắc muốn xóa combo "${name}"?`;
    modal.classList.remove("hidden");
    modal.classList.add("flex");
}

function closeDeleteModal() {
    pendingDeleteId = null;
    pendingDeleteName = null;
    const modal = document.getElementById("deleteModal");
    modal.classList.add("hidden");
    modal.classList.remove("flex");
}

async function confirmDeleteCombo() {
    if (!pendingDeleteId) return;
    const id = pendingDeleteId;
    closeDeleteModal();

    currentConfig.customCombos = (currentConfig.customCombos || []).filter(c => c.id !== id);
    await saveConfig();
    renderCombosFromConfig();
}

document.addEventListener('DOMContentLoaded', () => {
    initialLoadCombos();
});
