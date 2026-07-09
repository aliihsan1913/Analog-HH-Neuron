# Biological Reference and Hardware Parameters: Neuron 1-10-8

This project aims to transform the theoretical Hodgkin-Huxley (HH) neuron model into a physical analog computer hardware. None of the capacitor or resistor values in the designed electronic circuit are hypothetical; all of them are derived from the morphological data of a real biological cell using fundamental principles of physics.

## 1. Reference Biological Neuron Data
The neuron named **1-10-8** from the NeuroMorpho database was selected for the simulation and hardware design.

* **Neuron Name:** 1-10-8
* **Species:** Rat
* **Region:** Neocortex
* **Soma Surface Area:** 1147.99 µm²
* **Original Data Source (Link):** [https://neuromorpho.org/neuron_info.jsp?neuron_name=1-10-8](https://neuromorpho.org/neuron_info.jsp?neuron_name=1-10-8)

---

## 2. Conversion from Biological Data to Electronic Values (Mathematical Proof)

Specific cell membrane parameters, measured by biophysicists and universally accepted in literature, were multiplied by the surface area ($A$) obtained from NeuroMorpho to derive specific electronic component values (Farads and Ohms).

Converting the 1147.99 µm² soma area to square centimeters:
$$A \approx 1.15 \times 10^{-5}\ cm^{2}$$

### A. Cell Membrane Capacitance Calculation
The cell membrane (lipid bilayer) acts as an insulating barrier between conductive ionic fluids, naturally behaving like a parallel-plate capacitor. The capacitance of 1 cm² of membrane is universally accepted as $C_{m} = 1\ \mu F / cm^{2}$.

The actual capacitor equivalent of the 1-10-8 neuron in the circuit is calculated as follows:
$$C_{total} = C_{m} \times A$$
$$C_{total} = (1\ \mu F / cm^{2}) \times (1.15 \times 10^{-5}\ cm^{2})$$
**Hardware Equivalent (Soma Capacitor):** $\approx 11.5\ pF$

### B. Ion Channel Conductance and Resistance Calculations
In the Hodgkin-Huxley model, the maximum sodium ($Na$) and potassium ($K$) conductances per 1 cm² are specific constants. These conductances ($G$) were calculated, and their inverses ($R = \frac{1}{G}$) were taken to obtain the resistor values to be used in the hardware.

**Sodium (Na) Channel:**
Standard $Na$ conductance: $120\ mS / cm^{2}$
$$G_{Na} = (120\ mS / cm^{2}) \times (1.15 \times 10^{-5}\ cm^{2}) \approx 1.38 \times 10^{-3}\ mS$$
$$R_{Na} = \frac{1}{G_{Na}}$$
**Hardware Equivalent ($Na$ Channel Resistance):** $\approx 724\ k\Omega$

**Potassium (K) Channel:**
Standard $K$ conductance: $36\ mS / cm^{2}$
$$G_{K} = (36\ mS / cm^{2}) \times (1.15 \times 10^{-5}\ cm^{2}) \approx 4.14 \times 10^{-4}\ mS$$
$$R_{K} = \frac{1}{G_{K}}$$
**Hardware Equivalent ($K$ Channel Resistance):** $\approx 2.41\ M\Omega$

**Leakage (Threshold) Channel:**
Standard leakage conductance: $0.3\ mS / cm^{2}$
$$G_{L} = (0.3\ mS / cm^{2}) \times (1.15 \times 10^{-5}\ cm^{2}) \approx 3.45 \times 10^{-6}\ mS$$
$$R_{L} = \frac{1}{G_{L}}$$
**Hardware Equivalent (Threshold Setting Resistor):** $\approx 289\ M\Omega$

---

## 3. Analog Hardware Architecture and Mapping

These calculated physical values were mapped to the following hardware blocks on the PCB:

* **Soma (Central Processing):** The capacitor acting as the cell membrane. Biological charge and discharge events occur directly on this component.
* **Voltage-Controlled Channels (TL072 and MPY634):** An active control circuit that integrates the non-linear opening and closing rates ($m, h, n$ variables) of Sodium and Potassium gates with time constants and multiplies them analogously. The $m^3h$ and $n^4$ functions are physically solved by MPY634 multiplier ICs.
* **STIM (Stimulus) and THRESH (Threshold):** The nanoampere-level current input applying external synaptic pressure to the circuit, and the leakage mechanism allowing the system to maintain its resting voltage (-65 mV).

Through this architecture, without using any software "If-Else" logic, time and voltage equations are solved in real-time directly by the laws of physics and analog electronics.