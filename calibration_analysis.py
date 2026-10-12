"""
Calibration analysis for the piezoelectric vibration sensor.

Reads calibration.csv (output voltage vs vibration amplitude at
100, 200 and 300 Hz), fits a straight line to each frequency, prints
sensitivity (mV/mm) and R^2, and saves calibration_curve.png.

Run from the repository root:
    python calibration_analysis.py
Requires: numpy, matplotlib
"""
import csv
import numpy as np
import matplotlib.pyplot as plt

with open("calibration.csv") as f:
    rows = list(csv.DictReader(f))

amp = np.array([float(r["amplitude_mm"]) for r in rows])
series = {
    "100 Hz": np.array([float(r["vout_100hz_mv"]) for r in rows]),
    "200 Hz": np.array([float(r["vout_200hz_mv"]) for r in rows]),
    "300 Hz": np.array([float(r["vout_300hz_mv"]) for r in rows]),
}

plt.figure(figsize=(8, 5))
print(f"{'Freq':<8}{'Sensitivity (mV/mm)':>22}{'Offset (mV)':>14}{'R^2':>8}")
for (label, v), marker in zip(series.items(), ["o", "s", "^"]):
    slope, intercept = np.polyfit(amp, v, 1)
    fit = slope * amp + intercept
    r2 = 1 - np.sum((v - fit) ** 2) / np.sum((v - v.mean()) ** 2)
    print(f"{label:<8}{slope:>22.0f}{intercept:>14.0f}{r2:>8.3f}")
    line = plt.plot(amp, v, marker=marker, linestyle="", label=f"{label} (measured)")[0]
    plt.plot(amp, fit, color=line.get_color(), linewidth=1,
             label=f"{label} fit: {slope:.0f} mV/mm, R²={r2:.3f}")

plt.xlabel("Vibration amplitude (mm)")
plt.ylabel("Output voltage (mV)")
plt.title("Piezo vibration sensor: calibration curves")
plt.grid(True, alpha=0.3)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig("calibration_curve.png", dpi=150)
print("Saved calibration_curve.png")
