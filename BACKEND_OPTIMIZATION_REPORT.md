# Python backend performance and memory audit

## Executive summary

The backend is a small localhost HTTP service plus global keyboard/mouse hooks
and timing-sensitive automation. Its dominant intentional CPU cost is the
busy-wait timing in macro functions; changing those loops would alter input
timing, so it was not changed. The largest avoidable runtime cost was
unconditional synchronous debug-log I/O on every input and macro lifecycle
event.

The implementation disables that diagnostic logging by default and retains it
with `CRYSS_DEBUG_LOG=1`. It also removes repeated timing-table allocations in
the two most commonly invoked combo steps and replaces linear key-state scans
with equivalent set membership checks. HTTP endpoints, request JSON, response
JSON, configuration schema, timing loops, and macro sequence are unchanged.

## High impact optimizations

### Production debug logging

**Problem:** Every hook event and macro lifecycle event opened `debug.log`,
formatted a timestamp, wrote a line, and closed the file synchronously. Input
hooks can fire far more often than configuration requests, making this the
only clear avoidable per-event disk I/O in the codebase.

**Performance impact:** Eliminates synchronous log-file I/O in normal runs;
CPU and latency improvement scale with input-event volume. It also prevents
unbounded `debug.log` growth and its associated disk-cache memory pressure.

**Code patch:** `log_debug` is gated by `CRYSS_DEBUG_LOG=1`; set that
environment variable only for diagnostics.

**Risk:** Low. Debug-file output is opt-in; application automation and the
frontend protocol do not consume this file.

### Reused timing tables

**Problem:** `skk2as` and `skk3aw` repeatedly constructed nested calibration
lists during macro execution.

**Performance impact:** Removes several short-lived list allocations for each
call of these frequently used steps, reducing allocator/GC work. The impact is
small per call but accumulates across long macros.

**Code patch:** Replaced those local lists with immutable module-level tuples.

**Risk:** Low. Values and interpolation order are unchanged.

## Medium impact optimizations

### Key-state membership checks

**Problem:** The hook handlers and cancellation helper scanned the `pressed`
set with `any(key == item for item in pressed)`.

**Performance impact:** Direct set membership avoids generator creation and
linear scans; memory allocation per check is eliminated.

**Code patch:** Replaced the scans with `key in pressed` / `key not in pressed`.

**Risk:** Low. `pressed` is already a set of hashable pynput key/button
objects, so membership has the same equality semantics.

## Low impact optimizations

Removed the unused `subprocess` import, reducing a small amount of startup
work and module memory.

## Deliberately not changed

- Busy-wait loops are the largest CPU consumers while a macro is active, but
  they enforce sub-frame timing. Replacing them with sleeps would reduce CPU at
  the cost of changing timing and was rejected.
- The `skk3as` frame calculation is not simplified because its current result
  may be relied upon by existing timing behavior.
- `/save` still reloads the configuration after writing it; avoiding that read
  would change exception/order behavior for malformed `FPS` values.
- No HTTP server, endpoint, JSON, threading, config, or macro-sequence change
  was made.

## Memory optimization summary

- Eliminated repeated nested-list allocations in two hot macro steps.
- Eliminated generator allocations for pressed-key membership checks.
- Prevented debug-log growth during normal operation.

## CPU optimization summary

- Removed normal-run synchronous disk I/O from hook and worker logging.
- Reduced hot-path Python allocation and iteration overhead.
- Preserved the intentional busy waits that govern automation timing.

## Estimated improvements

| Optimization | CPU | Memory | Startup |
| --- | ---: | ---: | ---: |
| Disable production debug log | High for input-heavy use; workload-dependent | Prevents log-cache/file growth | Negligible |
| Reuse timing tables | Small | A few allocations per macro step | Negligible |
| Direct set membership | Small | One generator allocation per check | Negligible |
| Remove unused import | Negligible | Small | Small |

Exact CPU/RAM numbers require a Windows environment with the installed pynput
hooks and real macro input. No Python interpreter is available in this
workspace, so runtime profiling and executable smoke testing could not run.

## Implementation order

1. Run the packaged application with production logging disabled (default).
2. Verify all existing save/run/shutdown and binding flows.
3. Profile macro CPU only on the target system before considering any
   timing-loop change.

## Validation checklist

- Confirm `/save`, `/run`, and `/shutdown` still return `{"ok": true}`.
- Confirm configuration JSON and localhost protocol are unchanged.
- Confirm every combo and key binding behaves with the same timing.
- Set `CRYSS_DEBUG_LOG=1` and confirm diagnostic logging remains available.
- Build and launch the PyInstaller executable on Windows.
