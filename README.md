# A CRITIC-Assisted Multi-Attribute Model for Cluster Head Selection in Agricultural Wireless Sensor Networks

> Major Project-II (YCS 8201)
> Bachelor of Technology (B.Tech) in Computer Science and Engineering

---

# 📌 Project Overview

Wireless Sensor Networks (WSNs) deployed in large-scale agricultural environments suffer from severe energy constraints due to the limited battery capacity of sensor nodes.

Traditional hierarchical routing protocols such as **LEACH (Low-Energy Adaptive Clustering Hierarchy)** improve energy efficiency by using Cluster Heads (CHs) for data aggregation. However, LEACH selects Cluster Heads randomly, without considering:

* Remaining battery power
* Node positioning
* Network density
* Distance from the Base Station

This often leads to:

* Rapid energy depletion
* Uneven load balancing
* Communication hotspots
* Reduced network lifetime

To overcome these limitations, this project introduces a **CRITIC-assisted Multi-Attribute Decision Making (MADM)** model for intelligent Cluster Head selection.

The proposed system evaluates nodes using:

* Residual Energy
* Distance to Sink/Base Station
* Local Node Density

The **CRITIC (Criteria Importance Through Inter-Criteria Correlation)** algorithm objectively calculates criterion weights by analyzing:

* Contrast intensity
* Standard deviation
* Inter-criteria conflict

This enables balanced and energy-efficient Cluster Head selection, resulting in:

✅ Improved network lifetime
✅ Reduced transmission delay
✅ Better load balancing
✅ Stable energy dissipation

---

# 🛠️ System Architecture & Workflow

The simulation models a dense agricultural monitoring environment over **2,000 communication rounds** in a:

* **300m × 300m** sensing field
* **100 sensor nodes**
* **0.05J initial energy per node**

The Base Station (Sink) is placed at:

```text
(50, 50)
```

---

## 🔄 Simulation Workflow

```text
[ Phase 1: Node Deployment ]
        ↓
Random deployment of 100 sensor nodes

[ Phase 2: Attribute Extraction ]
        ↓
Generate attribute matrix:
- Residual Energy
- Sink Distance
- Node Density

[ Phase 3: CRITIC Engine ]
        ↓
- Data normalization
- Standard deviation analysis
- Correlation analysis
- Weight calculation

[ Phase 4: Cluster Head Selection ]
        ↓
Top 10% high-scoring nodes selected as Cluster Heads

[ Phase 5: Radio Energy Model ]
        ↓
Data aggregation and routing using:
- Free Space Model (d²)
- Multipath Fading Model (d⁴)

[ Phase 6: Benchmark Evaluation ]
        ↓
Performance comparison with LEACH protocol
```

---

# ⚡ Radio Energy Model

The communication framework uses a **Dual Path Loss Model**:

| Distance Condition | Model Used                       |
| ------------------ | -------------------------------- |
| ( d < 87m )        | Free Space Model (( d^2 ))       |
| ( d ≥ 87m )        | Multipath Fading Model (( d^4 )) |

This improves transmission realism and energy consumption analysis.

---

# 🎯 Key Advantages of the CRITIC Model

## ✅ Objective Weight Calculation

The CRITIC algorithm removes subjective bias by automatically determining criterion importance from data statistics.

## ✅ Intelligent Load Balancing

High-energy and high-density nodes are strategically selected to distribute communication loads efficiently.

## ✅ Hotspot Reduction

The system minimizes random bottlenecks and stabilizes routing behavior across the network.

## ✅ Improved Network Stability

Results show smoother and more predictable energy dissipation curves compared to LEACH.

---

# 📂 Repository Structure

```text
├── src/
│   ├── __init__.py
│   ├── network_env.py
│   └── protocols.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## 📁 File Description

| File               | Description                                  |
| ------------------ | -------------------------------------------- |
| `network_env.py`   | Handles node deployment and network topology |
| `protocols.py`     | Implements LEACH and CRITIC algorithms       |
| `main.py`          | Runs simulations and generates graphs        |
| `requirements.txt` | Contains required Python dependencies        |

---

# ⚙️ Installation & Setup

## 🔹 Prerequisites

* Python 3.8 or above
* pip package manager

---

## 🔹 Clone the Repository

```bash
git clone https://github.com/ahana71/WSN-CRITIC-Clustering

cd critic-assisted-clustering-wsn
```

---

## 🔹 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Required Libraries

```text
numpy==2.4.2
pandas==3.0.1
matplotlib==3.10.8
scipy==1.17.1
```

---

# 🚀 Running the Project

Execute the simulation using:

```bash
python main.py
```

---

# 🖥️ Runtime Features

During execution, the program prompts users to enter custom filenames for saving generated graphs.

Generated outputs include:

1. **Network Lifetime Graph**

   * Tracks alive node count over rounds

2. **Transmission Delay Graph**

   * Measures communication latency

3. **Energy Consumption Graph**

   * Displays round-wise energy dissipation

4. **CRITIC Selected Nodes Energy Comparison**

   * Compares energy utilization of selected nodes

The system also includes duplicate filename protection to prevent accidental overwriting.

---

# 📊 Performance Analysis & Benchmark Results

## 🔹 Comparative Performance

| Performance Metric | Standard LEACH        | CRITIC-Assisted Model         |
| ------------------ | --------------------- | ----------------------------- |
| Network Lifetime   | Exhausted at Round 11 | Sustained till Round 16       |
| Energy Consumption | Highly unstable       | Stable & predictable          |
| Transmission Delay | > 3.5 Seconds         | ~2.1 Seconds                  |
| Routing Strategy   | Randomized            | Optimized using Sink Distance |

---

# 🔬 Sensor-Level Observations

## 📌 Sensor 7 & Sensor 2

* Significant reduction in energy depletion
* Prevented excessive communication overload
* Improved operational lifespan

## 📌 Sensor 82 & Sensor 3

* Consumed slightly higher energy intentionally
* Selected strategically as Cluster Heads
* Protected weaker nodes from heavy routing loads

---

# 📈 Key Outcomes

The CRITIC-assisted model achieved:

* ~45% improvement in network lifetime
* Lower transmission delays
* Balanced energy consumption
* Improved routing efficiency
* Better node survivability

---

# 🎓 Academic Information

## 🏫 Institution

Department of Computer Science and Engineering
JIS University
Kolkata, West Bengal, India

---

## 👨‍🏫 Project Supervisor

**Dr. Bidisha Bhabani**
Assistant Professor

---

## 👨‍💼 Head of Department

**Prof. Sandip Roy**
Professor & HOD

---

# 👥 Research Team (Group 44)

| Name           | Roll Number | JISU ID        |
| -------------- | ----------- | -------------- |
| Aalok Halder   | 22CS011001  | JISU/2022/1036 |
| Abhinanda Guha | 22CS011005  | JISU/2022/1395 |
| Ahana Bhowmik  | 22CS011011  | JISU/2022/0327 |
| Ankita Dhar    | 22CS011020  | JISU/2022/1386 |
| Oishe Sen      | 22CS011111  | JISU/2022/1429 |

---

# 📚 Research Domain

* Wireless Sensor Networks (WSN)
* Agricultural IoT
* Energy-Efficient Routing
* Cluster Head Optimization
* Multi-Attribute Decision Making (MADM)
* CRITIC Algorithm
* LEACH Protocol

---

# 📜 License

This project is developed strictly for academic and research purposes.

---

# ⭐ Acknowledgement

We sincerely thank:

* JIS University
* Department of Computer Science & Engineering
* Our project supervisor
* Faculty members and reviewers

for their guidance, support, and encouragement throughout the development of this project.
