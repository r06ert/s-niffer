import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from pathlib import Path

# =========================================================
# Touchstone S2P parser (RI / MA / DB)
# =========================================================
def read_s2p(filename):
    freq = []
    s = []
    data_format = None
    freq_unit = "HZ"

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("!"):
                continue

            # Touchstone option line
            if line.startswith("#"):
                tokens = line.upper().split()
                for u in ["HZ", "KHZ", "MHZ", "GHZ"]:
                    if u in tokens:
                        freq_unit = u
                        break
                for fmt in ["RI", "MA", "DB"]:
                    if fmt in tokens:
                        data_format = fmt
                        break
                continue

            values = list(map(float, line.split()))
            fval = values[0]
            raw = values[1:]

            # Frequency unit conversion
            if freq_unit == "GHZ":
                fval *= 1e9
            elif freq_unit == "MHZ":
                fval *= 1e6
            elif freq_unit == "KHZ":
                fval *= 1e3

            freq.append(fval)

            sp = []
            for i in range(0, 8, 2):
                a, b = raw[i], raw[i + 1]
                if data_format == "RI":
                    v = a + 1j * b
                elif data_format == "MA":
                    v = a * np.exp(1j * np.deg2rad(b))
                elif data_format == "DB":
                    v = 10 ** (a / 20) * np.exp(1j * np.deg2rad(b))
                else:
                    raise ValueError("Unknown data format")

                sp.append(v)

            # Touchstone order: S11 S21 S12 S22
            s.append([[sp[0], sp[2]],
                      [sp[1], sp[3]]])

    return np.array(freq), np.array(s)

# =========================================================
# Smith chart (pure matplotlib)
# =========================================================
def plot_smith(ax, S, title):
    r = np.abs(S)
    th = np.angle(S)
    ax.plot(r * np.cos(th), r * np.sin(th), '-o', markersize=2)
    ax.set_aspect('equal')
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_title(title)
    ax.grid(True)
    ax.add_artist(plt.Circle((0, 0), 1, fill=False, linestyle='--'))

# =========================================================
# MAIN
# =========================================================
if len(sys.argv) not in (2, 4):
    print("Usage:")
    print("  python s2p_plot_layout.py file.s2p")
    print("  python s2p_plot_layout.py file.s2p fmin_GHz fmax_GHz")
    sys.exit(1)

filename = Path(sys.argv[1])
if not filename.exists():
    print("Error: file does not exist")
    sys.exit(1)

fmin = float(sys.argv[2]) * 1e9 if len(sys.argv) == 4 else None
fmax = float(sys.argv[3]) * 1e9 if len(sys.argv) == 4 else None

freq, S = read_s2p(filename)

# Frequency range selection
if fmin is not None and fmax is not None:
    mask = (freq >= fmin) & (freq <= fmax)
    freq = freq[mask]
    S = S[mask]

freq_ghz = freq / 1e9

# =========================================================
# 2x2 LAYOUT
# =========================================================
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# ── S11 (top-left) – Smith chart
plot_smith(axs[0, 0], S[:, 0, 0], "S11")

# ── S12 (top-right) – magnitude + phase (dual Y-axis)
ax = axs[0, 1]
ax_p = ax.twinx()

amp_line, = ax.plot(
    freq_ghz,
    20 * np.log10(np.abs(S[:, 0, 1])),
    color="tab:blue",
    label="Magnitude [dB]"
)

phase_line, = ax_p.plot(
    freq_ghz,
    np.angle(S[:, 0, 1], deg=True),
    color="tab:orange",
    linestyle="--",
    label="Phase [°] (wrapped)"
)

ax.set_title("S12")
ax.set_xlabel("Frequency [GHz]")
ax.set_xscale("log")  # <-- logarithmic frequency axis
ax.set_ylabel("Magnitude [dB]", color="tab:blue")
ax_p.set_ylabel("Phase [°]", color="tab:orange")
ax.tick_params(axis='y', labelcolor="tab:blue")
ax_p.tick_params(axis='y', labelcolor="tab:orange")
ax.grid(True)
ax.legend([amp_line, phase_line],
          ["Magnitude [dB]", "Phase [°] (wrapped)"],
          loc="best")
Cursor(ax)

# ── S21 (bottom-left) – magnitude + phase (dual Y-axis)
ax = axs[1, 0]
ax_p = ax.twinx()

amp_line, = ax.plot(
    freq_ghz,
    20 * np.log10(np.abs(S[:, 1, 0])),
    color="tab:blue",
    label="Magnitude [dB]"
)

phase_line, = ax_p.plot(
    freq_ghz,
    np.angle(S[:, 1, 0], deg=True),
    color="tab:orange",
    linestyle="--",
    label="Phase [°] (wrapped)"
)

ax.set_title("S21")
ax.set_xlabel("Frequency [GHz]")
ax.set_xscale("log")  # <-- logarithmic frequency axis
ax.set_ylabel("Magnitude [dB]", color="tab:blue")
ax_p.set_ylabel("Phase [°]", color="tab:orange")
ax.tick_params(axis='y', labelcolor="tab:blue")
ax_p.tick_params(axis='y', labelcolor="tab:orange")
ax.grid(True)
ax.legend([amp_line, phase_line],
          ["Magnitude [dB]", "Phase [°] (wrapped)"],
          loc="best")
Cursor(ax)

# ── S22 (bottom-right) – Smith chart
plot_smith(axs[1, 1], S[:, 1, 1], "S22")

fig.suptitle(f"S-Parameters – {filename.name}")
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(filename.stem + ".jpg")

plt.show()