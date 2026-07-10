const chooseCombo = [
    "Combo gảy chan",
    "C0:22q223 223 22cd23 25",
    "C0:222q 223 223 22c3 223 3",
    "C0:qe 2cd23 223 223 2cd23 222",
]

const STORAGE_KEY = "selectedCombo"
const SIGN_KEY_STORAGE = "comboSignKeys" // NEW: { comboValue: "KeyName", ... }
const FPS_STORAGE = "FPS" // NEW: store FPS value

document.addEventListener("DOMContentLoaded", () => {
    const chooseTb = document.getElementById("chooseTb")
    const saveBtn = document.getElementById("saveBtn")
    const bindKeyBtn = document.getElementById("bindKeyBtn")    // NEW
    const savedKeyBadge = document.getElementById("savedKeyBadge") // NEW

    // ── Populate combo dropdown ──────────────────────────────────────────────
    chooseCombo.forEach((combo, index) => {
        const option = document.createElement("option")
        option.value = combo
        option.textContent = `Combo ${index + 1}: ${combo}`
        chooseTb.appendChild(option)
    })

    const savedCombo = localStorage.getItem(STORAGE_KEY)
    if (savedCombo && chooseCombo.includes(savedCombo)) {
        chooseTb.value = savedCombo
    }

    const fpsInput = document.getElementById("FPS")
    if (fpsInput) {
        fpsInput.value = LoadFPS()
    }

    function LoadFPS() {
        const savedFPS = localStorage.getItem(FPS_STORAGE)
        if (savedFPS) {
            return parseInt(savedFPS, 10)
        }
        return 120 // default FPS
    }

    // ── NEW: Sign Key (bind key) helpers ─────────────────────────────────────

    /** Load map of { comboValue: keyName } from localStorage */
    function loadSignKeys() {
        try {
            return JSON.parse(localStorage.getItem(SIGN_KEY_STORAGE)) || {}
        } catch {
            return {}
        }
    }

    /** Save the full map back to localStorage */
    function saveSignKeys(map) {
        localStorage.setItem(SIGN_KEY_STORAGE, JSON.stringify(map))
    }

    /** Pending key captured but not yet saved */
    let pendingKey = null

    /** Update the capture button text and the saved badge for current combo */
    function refreshBindUI() {
        const map = loadSignKeys()
        const combo = chooseTb.value
        const saved = map[combo]

        if (pendingKey !== null) {
            // Show pending (unsaved) state
            bindKeyBtn.textContent = `⌨ ${pendingKey}`
            bindKeyBtn.classList.add("bind-key-captured")
            bindKeyBtn.classList.remove("bind-key-listening")
        } else {
            bindKeyBtn.textContent = saved ? `⌨ ${saved}` : "Click to bind a key..."
            bindKeyBtn.classList.toggle("bind-key-captured", !!saved)
            bindKeyBtn.classList.remove("bind-key-listening")
        }

        if (saved) {
            savedKeyBadge.textContent = `Saved: ${saved}`
            savedKeyBadge.style.display = "inline-block"
        } else {
            savedKeyBadge.style.display = "none"
        }
    }

    /**
     * Convert a raw key/button event into a pynput-compatible name string.
     * Output must match what parse_input(name) in main.py accepts:
     *   - Button.{name}   → "left", "right", "middle"
     *   - Key.{name}      → "caps_lock", "f1", "shift", "enter", ...
     *   - single char     → "a", "1", "q", ...
     */
    function resolveKeyName(e) {
        // ── Mouse ────────────────────────────────────────────────────────────
        if (e.type === "mousedown") {
            const mouseMap = { 0: "left", 1: "middle", 2: "right" }
            return mouseMap[e.button] ?? `mouse_${e.button}`
        }

        // ── Keyboard: map browser e.code → pynput Key enum name ─────────────
        const codeMap = {
            // Modifier keys
            "ShiftLeft": "shift",
            "ShiftRight": "shift_r",
            "ControlLeft": "ctrl",
            "ControlRight": "ctrl_r",
            "AltLeft": "alt",
            "AltRight": "alt_gr",
            "MetaLeft": "cmd",
            "MetaRight": "cmd_r",

            // Toggle keys
            "CapsLock": "caps_lock",
            "NumLock": "num_lock",
            "ScrollLock": "scroll_lock",

            // Whitespace / editing
            "Space": "space",
            "Enter": "enter",
            "Backspace": "backspace",
            "Tab": "tab",
            "Escape": "esc",
            "Delete": "delete",
            "Insert": "insert",

            // Navigation
            "Home": "home",
            "End": "end",
            "PageUp": "page_up",
            "PageDown": "page_down",
            "ArrowUp": "up",
            "ArrowDown": "down",
            "ArrowLeft": "left",
            "ArrowRight": "right",

            // System
            "PrintScreen": "print_screen",
            "Pause": "pause",

            // Function keys F1–F20
            "F1": "f1", "F2": "f2", "F3": "f3", "F4": "f4", "F5": "f5",
            "F6": "f6", "F7": "f7", "F8": "f8", "F9": "f9", "F10": "f10",
            "F11": "f11", "F12": "f12", "F13": "f13", "F14": "f14", "F15": "f15",
            "F16": "f16", "F17": "f17", "F18": "f18", "F19": "f19", "F20": "f20",

            // Mouse side buttons
            "MouseBack": "x1",
            "MouseForward": "x2",
        };

        if (codeMap[e.code]) return codeMap[e.code]

        // ── Regular character keys: KeyA→"a", Digit1→"1" ────────────────────
        if (/^Key[A-Z]$/.test(e.code)) return e.code[3].toLowerCase()  // "KeyA" → "a"
        if (/^Digit[0-9]$/.test(e.code)) return e.code[5]                // "Digit3" → "3"

        // ── Numpad ───────────────────────────────────────────────────────────
        if (/^Numpad\d$/.test(e.code)) return e.code[6]                // "Numpad5" → "5"

        // ── Fallback: dùng e.key nếu là ký tự đơn ───────────────────────────
        if (e.key && e.key.length === 1) return e.key.toLowerCase()

        return e.code ?? e.key
    }


    /** Start listening for the next key/mouse press */
    function startCapture() {
        bindKeyBtn.textContent = "Press any key or mouse button... (ESC to cancel)"
        bindKeyBtn.classList.add("bind-key-listening")
        bindKeyBtn.classList.remove("bind-key-captured")
        savedKeyBadge.style.display = "none"
        pendingKey = null

        function onCapture(e) {
            e.preventDefault()
            e.stopPropagation()

            // Remove both listeners immediately
            window.removeEventListener("keydown", onCapture, true)
            window.removeEventListener("mousedown", onCapture, true)

            // ESC → xoá bind đã lưu của combo này
            if (e.type === "keydown" && e.code === "Escape") {
                const map = loadSignKeys()
                delete map[chooseTb.value]
                saveSignKeys(map)
                refreshBindUI()  // UI revert về idle (không có bind)
                return
            }

            pendingKey = resolveKeyName(e)
            refreshBindUI()
        }

        window.addEventListener("keydown", onCapture, true)
        window.addEventListener("mousedown", onCapture, true)
    }

    bindKeyBtn.addEventListener("click", () => {
        // If already listening, ignore (will be captured by window listener)
        if (bindKeyBtn.classList.contains("bind-key-listening")) return
        startCapture()
    })

    // When user switches combo, reset pending key and refresh UI
    chooseTb.addEventListener("change", () => {
        pendingKey = null
        refreshBindUI()
    })

    // Show bind UI on page load
    refreshBindUI()

    // NEW: Run button
    const runBtn = document.getElementById("runBtn")
    let runActive = false

    runBtn.addEventListener("click", () => {
        runActive = !runActive
        runBtn.classList.toggle("run-active", runActive)
        runBtn.textContent = runActive ? "⏹ STOP" : "▶ RUN"
        fetch("http://localhost:5000/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ enabled: runActive })
        }).catch(() => { })
    })

    // ── Save button ──────────────────────────────────────────────────────────
    saveBtn.addEventListener("click", () => {
        localStorage.setItem(STORAGE_KEY, chooseTb.value)
        localStorage.setItem(FPS_STORAGE, FPS.value)
        // Persist pending bind key for this combo
        if (pendingKey !== null) {
            const map = loadSignKeys()
            map[chooseTb.value] = pendingKey
            saveSignKeys(map)
            pendingKey = null
        }

        // POST full comboSignKeys map to Python backend
        fetch("http://localhost:5000/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ comboSignKeys: loadSignKeys(), FPS: LoadFPS() })
        }).catch(() => { })

        refreshBindUI()

        saveBtn.textContent = "SAVED!"
        setTimeout(() => {
            saveBtn.textContent = "SAVE"
        }, 1000)
    })
})
