<img src="/doc/img/s-niffer_logo.jpg?raw=true" width="130"/>

@project **S-Niffer**

@author Robert Zdunek

@document revision 0.1 (beta)

@date 24.02.2026

# 1. What is the S-Niffer?

## 1.1 Overview of the S-Niffer project

S-Niffer is a device used to measure [S-parameters](https://en.wikipedia.org/wiki/Scattering_parameters) of electronic components such as capacitors, inductors, and resistors. S-Niffer is an adapter that allows SMD components in 0402(c), 0603(c), and 0805(c) packages to be connected to a [Vector Network Analyzer](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)).

Experimental results confirm an upper measurement bandwidth of 1GHz. For less demanding applications, results up to 3GHz may still be usable. See section [4. S-Niffer Verification](#4-s-niffer-verification).

S-Niffer enables [S-parameters](https://en.wikipedia.org/wiki/Scattering_parameters) measurements in the following configurations:

| schematic diagram | description |
|------|------|
| <img src="/doc/img/s-niffer_photos/s-niffer_oneport_sch.jpg?raw=true" width="100" /> | one-port network |
| <img src="/doc/img/s-niffer_photos/s-niffer_shunt_sch.jpg?raw=true" width="100" /> | two-port network with parameters measured in shunt configuration |
| <img src="/doc/img/s-niffer_photos/s-niffer_series_sch.jpg?raw=true" width="100" /> | two-port network with parameters measured in series configuration |

## 1.2 S-Niffer photos

| photo | description |
|------|------|
| <img src="/doc/img/s-niffer_photos/s-niffer_photo1.jpg?raw=true" width="200" /> | - one-port network<br>- two-port network in shunt configuration<br>- two-port network in series configuration |
| <img src="/doc/img/s-niffer_photos/s-niffer_photo2.jpg?raw=true" width="200" /> | - the measured component does not need to be soldered<br>- the component is held in place by a spring.  |
| <img src="/doc/img/s-niffer_photos/s-niffer_photo3.jpg?raw=true" width="200" /> | - it is possible to measure 0402(c), 0603(c), and 0805(c) components<br>- a 0402(c) component is shown next to this |

## 1.3 Content of the README file

- [2. Hardware](#2-hardware) section presents the device design.
	- [2.1 S-Niffer design](#21-s-niffer-design)
	- [2.2 Calibration kit](#22-calibration-kit)
	- [2.3 Mechanical design](#23-mechanical-design)
	- [2.4 Photos](#2.4-photos)
- [3. Measurement Process](#3-measurement-process) section presents the measurement process
- [4. S-Niffer Verification](#4-s-niffer-verification) section presents verification and conclusions
	- [4.1 Verification Method](41-verification-method)
	- [4.2 Measurement results of the GCQ1555C1H470JB01 capacitor](42-measurement-results-of-the-gcq1555c1h470jb01-capacitor)
	- [4.3 Measurement results of the LQW15AN47NJ00 inductor](43-measurement-results-of-the-lqw15an47nj00-inductor)
	- [4.4 Conclusions](44-conclusions)

## 1.4 Contents of the repository 

- \doc
	- img\
		- ...
- \hardware
	- **S-Niffer_gerber.zip** - gerber files of the main board
	- **S-Niffer_hold-down_clamp_gerber.zip** gerber files of the hold-down clamp
	- **S-Niffer_hold-down_clamp_pcb.pdf** - PCB layout of the hold-down clamp
	- **S-Niffer_pcb.pdf** - PCB layout of the main board
	- **S-Niffer_sch.pdf** - schematic diagram of the main board
- \software
	- \models
		- **GCQ1555C1H470JB01.s2p** - [Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file) of GCQ1555C1H470JB01 capacitor (47pF, 0402(c)) downloaded from the [Murata](https://www.murata.com/) website
		- **GCQ1555C1H470JB01_measured.s2p** - [Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file) of GCQ1555C1H470JB01 capacitor (47pF, 0402(c)) measured with a [VNA](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) using S-Niffer
		- **LQW15AN47NJ00.s2p** - [Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file) of LQW15AN47NJ00 inductor (47nH, 0402(c)) downloaded from the [Murata](https://www.murata.com/) website
		- **LQW15AN47NJ00_measured.s2p** - [Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file) of LQW15AN47NJ00 inductor (47nH, 0402(c)) measured measured with a [VNA](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) using S-Niffer
	- \scripts
		- **instal.bat** - installs missing Python libraries
		- **s2p_plot.bat** - runs the s2p_plot.py Python script
		- **s2p_plot.py** - plots S11, S21, S12, and S22 parameters of the given [Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file)
		- **s2p_plot_compare.bat** - runs the s2p_plot_compare.py Python script
		- **s2p_plot_compare.py** - plots S11, S21, S12, and S22 parameters of the given [Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file) and compares them

# 2. Hardware

## 2.1 S-Niffer design

The project uses two PCBs: the main PCB and the hold-down clamp PCB. The main PCB is a four-layer board. The PCB layout and stack-up were designed so that the traces have a 50Ω impedance. On the TOP layer, the traces necessary for measurements in one of the following configurations are implemented:

| photo | schematic diagram | configuration |
|------|------|------|
| <img src="/doc/img/hardware_photos/hardware_oneport.jpg?raw=true" width="200" /> | <img src="/doc/img/hardware_photos/hardware_oneport_sch.jpg?raw=true" width="150" /> | one-port network |
| <img src="/doc/img/hardware_photos/hardware_shunt.jpg?raw=true" width="200" /> | <img src="/doc/img/hardware_photos/hardware_shunt_sch.jpg?raw=true" width="150" /> | two-port network with parameters measured in shunt configuration |
| <img src="/doc/img/hardware_photos/hardware_series.jpg?raw=true" width="200" />| <img src="/doc/img/hardware_photos/hardware_series_sch.jpg?raw=true" width="150" /> | two-port network with parameters measured in series configuration |

## 2.2 Calibration kit

The BOTTOM layer of the main PCB contains traces for building a [VNA](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) calibration kit. The calibration kit allows performing SOLT (Short-Open-Load-Through) calibration:

| photo | configuration |
|------|------|
| <img src="/doc/img/hardware_photos/hadrware_cal_short.jpg?raw=true" width="200" /> | short |
| <img src="/doc/img/hardware_photos/hadrware_cal_open.jpg?raw=true" width="200" /> | open |
| <img src="/doc/img/hardware_photos/hadrware_cal_load.jpg?raw=true" width="200" /> | load |
| <img src="/doc/img/hardware_photos/hadrware_cal_through.jpg?raw=true" width="200" /> | through |

## 2.3 Mechanical design 

The hold-down clamp PCB is a component of the S-Niffer and does not contain any measurement traces.

The S-Niffer is equipped with magnets in its feet, which allow secure attachment to a metal surface and convenient handling during measurements.

## 2.4 Photos

| photo | description |
|------|------|
| <img src="/doc/img/hardware_photos/hardware_photo1.jpg?raw=true" width="200" /> | the main PCB (TOP and BOTTOM side) and the hold-down clamp PCB |
| <img src="/doc/img/hardware_photos/hardware_photo2.jpg?raw=true" width="200" /> | the TOP side of the main PCB implements a one-port network, a two-port network in shunt configuration, and a two-port network in series configuration. |
| <img src="/doc/img/hardware_photos/hardware_photo3.jpg?raw=true" width="200" /> | the BOTTOM side of the main PCB implements the calibration kit for SOLT (Short-Open-Load-Through) calibration |

# 3. Measurement Process

| photo | description |
|------|------|
| <img src="/doc/img/measurement_photos/measurement_photo1.jpg?raw=true" width="200" /> | STEP 1<br>Remember about [ESD](https://en.wikipedia.org/wiki/Electrostatic_discharge) protection. The [Vector Network Analyzer](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) is sensitive to electrostatic discharge. |
| <img src="/doc/img/measurement_photos/measurement_photo2.jpg?raw=true" width="200" /> | STEP 2<br>Warm up your [Vector Network Analyzer](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) before measurements. |
| <img src="/doc/img/measurement_photos/measurement_photo3.jpg?raw=true" width="200" /> | STEP 3.1<br>[VNA](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) calibration. Port 1 calibration with the **short** and port 2 calibration with the **open**. |
| <img src="/doc/img/measurement_photos/measurement_photo4.jpg?raw=true" width="200" /> | STEP 3.2<br>[VNA](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) calibration. Port 1 calibration with a **load**. |
| <img src="/doc/img/measurement_photos/measurement_photo5.jpg?raw=true" width="200" /> | STEP 3.3<br>[VNA](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) calibration. Port 1 and Port 2 calibration with the **through**. |
| <img src="/doc/img/measurement_photos/measurement_photo6.jpg?raw=true" width="200" /> | STEP 3.4<br>[VNA](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) calibration. Port 1 calibration with the **open** and port 2 calibration with the **short**. |
| <img src="/doc/img/measurement_photos/measurement_photo7.jpg?raw=true" width="200" /> | STEP 3.5<br>[VNA](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) calibration. Port 2 calibration with the **load**. |
| <img src="/doc/img/measurement_photos/measurement_photo8.jpg?raw=true" width="200" /> | STEP 4.<br>Select the measurement configuration and connect the S-Niffer to the [VNA](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)). |
| <img src="/doc/img/measurement_photos/measurement_photo9.jpg?raw=true" width="200" /> | STEP 5.<br>Place and secure the component to be measured. |
|  | STEP 6.<br>Click the **Play** button on the [VNA](https://en.wikipedia.org/wiki/Network_analyzer_(electrical)) to start the measurement. |

# 4. S-Niffer Verification

## 4.1 Verification Method

To verify the operation of the S-Niffer, two components were selected: the GCQ1555C1H470JB01 capacitor (47pF, 0402(c)) and the LQW15AN47NJ00 inductor (47nH, 0402(c)). These components were chosen because the manufacturer provides models ([Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file)), which can be used as reference results to which the measured data should be compared.

The reference ([Touchstone files](https://en.wikipedia.org/wiki/Touchstone_file)) were downloaded from the [Murata](https://www.murata.com/) website and are located in the \software\models\ directory:
- **GCQ1555C1H470JB01.s2p** – ([Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file)) of the GCQ1555C1H470JB01 capacitor (47pF, 0402(c)).
- **LQW15AN47NJ00.s2p** – ([Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file)) of the LQW15AN47NJ00 inductor (47nH, 0402(c)).

In both cases, [Murata](https://www.murata.com/) performed measurements of the two-port network in series configuration.

Measurements of these components were performed using the S-Niffer and LibreVNA. The resulting files are located in the \software\models\ directory:
- **GCQ1555C1H470JB01_measured.s2p** - [Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file) of GCQ1555C1H470JB01 capacitor (47pF, 0402(c))
- **LQW15AN47NJ00_measured.s2p** - [Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file) of LQW15AN47NJ00 inductor (47nH, 0402(c))

The comparison was performed using Python scripts, which compared the reference [Touchstone files](https://en.wikipedia.org/wiki/Touchstone_file) with the measured data. The scripts are located in the \software\scripts\ directory:
- **instal.bat** - installs missing Python libraries
- **s2p_plot.bat** - runs the s2p_plot.py Python script
- **s2p_plot.py** - plots S11, S21, S12, and S22 parameters of the given [Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file)
- **s2p_plot_compare.bat** - runs the s2p_plot_compare.py Python script
- **s2p_plot_compare.py** - plots S11, S21, S12, and S22 parameters of the given [Touchstone file](https://en.wikipedia.org/wiki/Touchstone_file) and compares them

## 4.2 Measurement results of the GCQ1555C1H470JB01 capacitor

| plots | description |
|------|------|
| <img src="/doc/verification/GCQ1555C1H470JB01.jpg?raw=true"/> | reference results |
| <img src="/doc/verification/GCQ1555C1H470JB01_measured.jpg?raw=true"/> | results measured with the S-Niffer and LibreVNA |
| <img src="/doc/verification/GCQ1555C1H470JB01_comparison.jpg?raw=true"/> | comparison of reference and measured values |

## 4.3 Measurement results of the LQW15AN47NJ00 inductor

| plots | description |
|------|------|
| <img src="/doc/verification/LQW15AN47NJ00.jpg?raw=true"/> | reference results |
| <img src="/doc/verification/LQW15AN47NJ00_measured.jpg?raw=true"/> | results measured with the S-Niffer and LibreVNA |
| <img src="/doc/verification/LQW15AN47NJ00_comparison.jpg?raw=true"/> | comparison of reference and measured values |

## 4.4 Conclusions

So far, measurements have been performed only for the two-port network in series configuration. From the results, it can be concluded that measurements up to 1GHz are accurate, while measurements up to 3GHz can still be considered useful.

Measurement accuracy may be affected by:
- The universal footprint used for 0402, 0603, and 0805 packages.
- The component being pressed against the footprint. A soldered connection would likely result in lower inductance.
- The pressing element, made of polyamide, whose relative permittivity (electric and magnetic) is not close to that of air. Its presence near the measured component can affect the component’s parameters.
- The component under test is pressed, which induces mechanical stress. The presence of this stress may affect the component’s parameters.
