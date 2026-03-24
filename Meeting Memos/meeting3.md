# Meeting Minutes: CNC Retrofit Project

**Date:** March 24, 2026
**Time:** 13:00 – 15:30
**Location:** Project Workshop / Lab

---

## 1. Discussion Topics

### 1.1 System Architecture & Power Electronics
* **[x] Driver Topology:** Evaluated the transition from 220V AC to a regulated 180V DC. The team settled on a **Buck Converter** architecture followed by a full-wave bridge rectifier for superior efficiency.
* **[x] Isolation Strategy:** Confirmed the necessity of **galvanic isolation** (using high-speed opto-isolated gate drivers like the HCPL-3120) to protect the CNC control logic from the 310V DC power bus.

### 1.2 Case Study: Treadmill Motor Driver Analysis
* **Observation:** Conducted a teardown and technical analysis of a surplus treadmill DC motor driver.
* **Findings:** The unit provided valuable insight into high-voltage DC switching circuits and power component layout (SCRs/MOSFETs and large filter capacitors).
* **Decision:** Due to the physical condition and aging of the components, the team decided **not to use this specific driver** for the final CNC assembly. However, it may serve as a reference for our custom-built isolated driver design.

### 1.2 Musts for design
* **Encoder and Buttons:** It will be used for zeroing parts.
* **Screen:** It will be useful for feedback to users.

---

## 2. Weekly Objectives (Action Plan)

| Task | Description | Assigned To | Status |
| :--- | :--- | :--- | :--- |
| **BOM Finalization** | Select MOSFETs and Optocouplers for the Buck stage. | Team | In Progress |

---

## 3. Key Takeaways
* **Design Philosophy:** The custom driver must prioritize noise immunity (EMI) to prevent interference with the CNC controller's pulse-train signals.
