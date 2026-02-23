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
# Smith chart
# =========================================================
def plot_smith(ax, S, label, color):
    r = np.abs(S)
    th = np.angle(S)
    ax.plot(r * np.cos(th),
            r * np.sin(th),
            '-o',
            markersize=2,
            label=label,
            color=color)

# =========================================================
# MAIN
# =========================================================
if len(sys.argv) not in (3, 5):
    print("Usage:")
    print("  python s2p_plot_compare.py file1.s2p file2.s2p")
    print("  python s2p_plot_compare.py file1.s2p file2.s2p fmin_GHz fmax_GHz")
    sys.exit(1)

file1 = Path(sys.argv[1])
file2 = Path(sys.argv[2])

if not file1.exists() or not file2.exists():
    print("Error: one or both files do not exist")
    sys.exit(1)

fmin = float(sys.argv[3]) * 1e9 if len(sys.argv) == 5 else None
fmax = float(sys.argv[4]) * 1e9 if len(sys.argv) == 5 else None

freq1, S1 = read_s2p(file1)
freq2, S2 = read_s2p(file2)

if fmin is not None and fmax is not None:
    m1 = (freq1 >= fmin) & (freq1 <= fmax)
    m2 = (freq2 >= fmin) & (freq2 <= fmax)
    freq1, S1 = freq1[m1], S1[m1]
    freq2, S2 = freq2[m2], S2[m2]

freq1_ghz = freq1 / 1e9
freq2_ghz = freq2 / 1e9

# =========================================================
# 2x2 LAYOUT
# =========================================================
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

colors = ["tab:blue", "tab:red"]

# ── S11 (top-left) – Smith
axs[0, 0].add_artist(plt.Circle((0, 0), 1, fill=False, linestyle='--'))
axs[0, 0].set_aspect('equal')
axs[0, 0].set_xlim(-1.1, 1.1)
axs[0, 0].set_ylim(-1.1, 1.1)
axs[0, 0].grid(True)
axs[0, 0].set_title("S11")

plot_smith(axs[0, 0], S1[:, 0, 0], file1.name, colors[0])
plot_smith(axs[0, 0], S2[:, 0, 0], file2.name, colors[1])
axs[0, 0].legend()

# ── S12 (top-right)
ax = axs[0, 1]
ax_p = ax.twinx()

ax.plot(freq1_ghz,
        20 * np.log10(np.abs(S1[:, 0, 1])),
        color=colors[0],
        label=f"{file1.name} | Mag")

ax.plot(freq2_ghz,
        20 * np.log10(np.abs(S2[:, 0, 1])),
        color=colors[1],
        label=f"{file2.name} | Mag")

ax_p.plot(freq1_ghz,
          np.angle(S1[:, 0, 1], deg=True),
          '--',
          color=colors[0])

ax_p.plot(freq2_ghz,
          np.angle(S2[:, 0, 1], deg=True),
          '--',
          color=colors[1])

ax.set_title("S12")
ax.set_xlabel("Frequency [GHz]")
ax.set_xscale("log")  # <-- logarithmic frequency axis
ax.set_ylabel("Magnitude [dB]")
ax_p.set_ylabel("Phase [°] (wrapped)")
ax.grid(True)
ax.legend()
Cursor(ax)

# ── S21 (bottom-left)
ax = axs[1, 0]
ax_p = ax.twinx()

ax.plot(freq1_ghz,
        20 * np.log10(np.abs(S1[:, 1, 0])),
        color=colors[0],
        label=f"{file1.name} | Mag")

ax.plot(freq2_ghz,
        20 * np.log10(np.abs(S2[:, 1, 0])),
        color=colors[1],
        label=f"{file2.name} | Mag")

ax_p.plot(freq1_ghz,
          np.angle(S1[:, 1, 0], deg=True),
          '--',
          color=colors[0])

ax_p.plot(freq2_ghz,
          np.angle(S2[:, 1, 0], deg=True),
          '--',
          color=colors[1])

ax.set_title("S21")
ax.set_xlabel("Frequency [GHz]")
ax.set_xscale("log")  # <-- logarithmic frequency axis
ax.set_ylabel("Magnitude [dB]")
ax_p.set_ylabel("Phase [°] (wrapped)")
ax.grid(True)
ax.legend()
Cursor(ax)

# ── S22 (bottom-right) – Smith
axs[1, 1].add_artist(plt.Circle((0, 0), 1, fill=False, linestyle='--'))
axs[1, 1].set_aspect('equal')
axs[1, 1].set_xlim(-1.1, 1.1)
axs[1, 1].set_ylim(-1.1, 1.1)
axs[1, 1].grid(True)
axs[1, 1].set_title("S22")

plot_smith(axs[1, 1], S1[:, 1, 1], file1.name, colors[0])
plot_smith(axs[1, 1], S2[:, 1, 1], file2.name, colors[1])
axs[1, 1].legend()

fig.suptitle("S-Parameter Comparison")
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(file1.stem + "_comparison.jpg")

plt.show()