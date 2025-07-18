# Starlink Network Simulator

A Python-based simulation and visualization of a satellite internet network inspired by SpaceX's **Starlink** constellation. The project analyzes bandwidth load, optimal routing, and real-time positions of satellites using real orbital data and simulates different usage scenarios.

## 🔭 Project Overview

This project simulates the flow of data in a satellite network using real satellite positioning (TLE) data. It allows for:

- Visualizing satellites and users in real-time.
- Calculating maximum network throughput.
- Mapping heatmaps of satellite bandwidth load under various conditions.

## 🌐 Key Technologies

- **Python**
- **Skyfield** – For satellite orbit calculations from TLE/3LE data
- **NetworkX** – For modeling and analyzing the graph of satellite connections
- **Matplotlib + Cartopy** – For geospatial visualizations and heatmaps
- **PyQt5** – For GUI-based real-time visualizations

## 📁 Project Structure

```
📦Starlink-Network-Simulator
 ┣ 📂data            # Satellite & ground station data
 ┣ 📂scripts         # Code for simulation and visualization
 ┣ 📂output          # Simulation results (heatmaps, GIFs)
 ┣ 📜README.md       # This file
 ┗ 📜requirements.txt
```

## 🚀 Features

- **3LE/TLE Parsing:** Satellite orbit data is fetched and processed to determine real-time positions.
- **Graph Construction:** The satellite network is modeled as a directed graph with:
  - Dual nodes for each satellite (IN/OUT)
  - Optical Inter-Satellite Links (OISL)
  - Ground station integration
  - User-to-satellite assignments based on line of sight
- **Flow Simulation:** Uses max-flow algorithms to find network throughput and detect bottlenecks.
- **Heatmap Generation:** Displays network load distribution under different user and bandwidth conditions.
- **GUI:** A real-time visualization of satellite positions and connections with a PyQt5 interface.

## 📊 Simulations

Simulations were conducted using:

- Different satellite bandwidths: `20GB` and `200GB`
- Varying user distributions: only USA vs. global spread (USA, EU, AU, AF)
- 90-minute intervals at 5-minute steps (real orbit cycle)
- Max throughput calculations

Each simulation generates a heatmap and a combined GIF animation of network load.

## 📷 Visual Outputs

- [📽️ Real-time Satellite Visualization (Demo)](https://drive.google.com/file/d/1pYGyJIS_oXtIvnS5d7zEWYfvmYnyYYVE/view)
- [📊 Simulation GIFs](https://drive.google.com/drive/folders/1MkQT2XhFJ01PfE8hzRuLzA5LDgqoNIyW)

## 🔧 Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/wajdifadool/Starlink-Network-Simulator.git
   cd Starlink-Network-Simulator
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the simulation or visualization:
   ```bash
   python main.py
   ```

## 📈 Example Results

| Simulation    | Satellite Capacity | Max Network Load |
| ------------- | ------------------ | ---------------- |
| USA, 20GB     | Low                | ~2.3 TB          |
| USA, 200GB    | High               | ~9.6 TB          |
| Global, 20GB  | Medium             | ~5.1 TB          |
| Global, 200GB | High               | ~9.6 TB          |

## 📊 Simulation Results Analysis

Based on the **heatmaps** and **simulations** we conducted, several insights can be drawn. The table below summarizes the input data for each simulation along with the resulting network load:

| Simulation | Satellite Count | User Count | Ground Stations | Ground Station Capacity | Satellite Capacity | User Download Capacity | Max Network Load | Heatmap Scenario          |
| ---------- | --------------- | ---------- | --------------- | ----------------------- | ------------------ | ---------------------- | ---------------- | ------------------------- |
| 1          | 1215–1225       | 250,000    | 121             | 80 GB                   | 200 GB             | 200 MB                 | ~9600 GB         | {200GB, USA}              |
| 2          | 1215–1225       | 250,000    | 121             | 80 GB                   | 20 GB              | 200 MB                 | ~2300 GB         | {20GB, USA}               |
| 3          | 1215–1225       | 250,000    | 121             | 80 GB                   | 200 GB             | 200 MB                 | ~9600 GB         | {200GB, USA, EU, AUS, AF} |
| 4          | 1215–1225       | 250,000    | 121             | 80 GB                   | 20 GB              | 200 MB                 | ~5180 GB         | {20GB, USA, EU, AUS, AF}  |

---

## 📌 Key Insights:

### 1. Impact of Satellite Bandwidth

- The simulations clearly show that when satellite bandwidth is higher (200GB), the **maximum data flow** across the network increases significantly.
- This is evident from Simulations **1 and 3** compared to **2 and 4**.
- Additionally, heatmaps indicate **reduced congestion** on specific satellites in higher-bandwidth scenarios, implying that the network handles **traffic more efficiently** when bandwidth per satellite is greater.
- Thus, a **higher satellite capacity** allows the network to **support more users** in the same regions before experiencing performance degradation.

### 2. Impact of User Distribution

- Comparing Simulations **2 and 4** shows that when users are **spread across multiple continents** (USA, EU, AUS, AF), the **overall network flow increases** (5180GB vs. 2300GB) even when bandwidth is equal (20GB).
- A wider geographic **distribution of users** leads to **better utilization** of the satellite network and helps **reduce local congestion**.

## 💡 Potential Improvements

- Switch to 3D visualization using CesiumJS/WebGL
- Real-time traffic prediction and adaptive routing
- Better topographical line-of-sight validation (e.g., terrain blocking)
- Advanced load balancing strategies
- Integration of atmospheric or magnetic interference models

## 🙌 Acknowledgements

Special thanks to Dr. Shlomo Khoury for his guidance and mentorship throughout the project.

Developed by:

- Wajdi Fadul
- Milka Shishportish

**A detailed project notebook is available as part of this work. It includes all technical explanations, simulation architecture, visualizations, and results.**

🗂️ If you're interested in reviewing the full notebook, feel free to contact me directly:

## 📚 References

- [Starlink Official](https://www.starlink.com)
- [CelesTrak TLE Data](https://celestrak.org/NORAD/elements/)
- [Skyfield Library](https://rhodesmill.org/skyfield/)
- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [Starlink Ground Stations](https://starlinkspot.com/starlink-ground-station-locations)
