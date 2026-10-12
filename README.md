# Piezoelectric Vibration Sensor (Analog Only)

> A low-cost vibration sensor for machinery and structures, built entirely from analog parts: a piezoelectric element, one op-amp and two resistors. No microcontroller.

![Calibration setup](media/calibration_setup.jpg)

**Course:** EE251 – Semester 3 Sensor Project, University of Peradeniya · **Duration:** Dec 2024 – Apr 2025
**Team:** Harishraj T., Shakthidharan S., Nirojan A.
**My role:** *(fill in, e.g. "Amplifier design and Proteus simulation, calibration measurements")*

---

## Problem
Vibration levels in motors, industrial machines and structures are an early warning of wear and failure. Commercial vibration sensors are expensive. The goal was a simple, cheap sensor whose output voltage tracks vibration amplitude in the 100–500 Hz band typical of rotating machinery.

## Choosing the sensing principle
| Method | Outcome |
|---|---|
| Capacitive | Tried first. A 0.1 mm plate gap and ~1 pF capacitance changes were too small to fabricate and measure reliably with an analog setup. |
| Optical fibre | Too expensive for the project scope. |
| Microphone-based | Too sensitive to ambient noise in industrial settings. |
| **Piezoelectric** ✅ | High sensitivity and directly generates a measurable voltage. Chosen. |

## How it works
1. A **piezoelectric disc with a seismic mass** is attached to the vibrating surface.
2. Mechanical stress from vibration makes the crystal generate a small voltage, a few millivolts, proportional to vibration intensity.
3. An **LM741 non-inverting amplifier** boosts the signal:
   **Gain = 1 + R2/R1 = 1 + 500 kΩ / 10 kΩ = 51** (≈ 34 dB).
4. The amplified output is read on an oscilloscope, and a calibration curve converts voltage to amplitude.

![Amplifier schematic](hardware/amplifier_schematic.png)

Power: two 9 V batteries (±9 V split supply).

## Calibration
A speaker driven by a signal generator acted as a controlled vibration source. The piezo sensor was mounted on the speaker, and the output voltage was recorded against vibration amplitude (0.1–2.5 mm) at 100, 200 and 300 Hz.

![Calibration curves](docs/calibration_curve.png)

Linear fit for each frequency, from [`analysis/calibration_analysis.py`](analysis/calibration_analysis.py):

| Frequency | Sensitivity | R² |
|---|---|---|
| 100 Hz | **≈ 1790 mV/mm** | 0.991 |
| 200 Hz | ≈ 560 mV/mm | 0.955 |
| 300 Hz | ≈ 2240 mV/mm | 0.928 |

Raw data: [`data/calibration.csv`](data/calibration.csv)

**What the data shows**
- At **100 Hz** the response is highly linear (R² = 0.99) across the full 0.1–2.5 mm range.
- **Sensitivity depends strongly on frequency.** It changes by about 4× between 200 Hz and 300 Hz, so each frequency needs its own calibration curve. This is consistent with the mechanical resonances of the speaker-and-sensor setup.
- At **300 Hz** the response becomes non-linear above about 1.8 mm, with a spike at 2.1 mm. This is likely a resonance or clipping effect in the setup.

## Challenges & how we solved them
- **Capacitive method failed:** the capacitance changes were too small to measure. → Switched to piezoelectric sensing.
- **Limited lab access:** the oscilloscope and signal generator were only available during lab hours. → Built a home test rig: a **Bluetooth speaker playing test tones from a phone** as the vibration source, with the **Arduino Serial Plotter** as a stand-in oscilloscope.
- **Debugging without lab equipment:** → Checked each component and connection with a multimeter to isolate faults.

## Limitations & future work
- Calibration was measured at 100–300 Hz. The 400–500 Hz end of the target band still needs characterizing.
- The calibration curve depends on the mounting surface, so the sensor needs recalibrating for each installation.
- The LM741 is an old, noisy op-amp that needs a split supply. A modern rail-to-rail op-amp would allow single-supply operation and lower noise.
- Future work: add an ADC or microcontroller to compute RMS amplitude and frequency automatically, a threshold alarm for predictive maintenance, and vibration energy harvesting.

## Repository structure
```
├── analysis/   # calibration_analysis.py — linear fits + plot
├── data/       # calibration.csv — output voltage vs amplitude
├── docs/       # report.pdf, calibration_curve.png
├── hardware/   # amplifier schematic (Proteus)
└── media/      # calibration setup photo
```

## Reproduce the analysis
```bash
pip install numpy matplotlib
python analysis/calibration_analysis.py
```

## Acknowledgements
Teammates Shakthidharan S. and Nirojan A., and the EE251 course staff, Department of EEE, University of Peradeniya.
