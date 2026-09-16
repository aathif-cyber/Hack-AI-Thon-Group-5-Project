# 🌱 GreenGrid

## **Smart Energy Consumption & Carbon Tracker**

> ⚡ **Measure Energy.** 💰 **Understand Cost.** 🌍 **Track Carbon.** 💡 **Act Smarter.**

> *A Python-powered energy management prototype built with Object-Oriented Programming and aligned with the Sustainable Development Goals.*

---

## 🚀 Project at a Glance

**GreenGrid** is a smart energy-management application designed to record electricity consumption across **appliances, rooms, homes, or institutions** and transform that information into an understandable energy report.

Instead of looking at electricity usage as raw numbers, GreenGrid turns consumption data into actionable insights:

> **Energy → Cost → Carbon Impact → Top Consumers → Recommendations**

The prototype is primarily implemented in **Python** and demonstrates **Python fundamentals + Object-Oriented Programming (OOP)** through dedicated classes for appliances, energy records, and reports.

---

# 🎯 The Challenge

Electricity consumption is often difficult to understand at an appliance level.

A typical energy bill tells us **how much electricity was consumed**, but not necessarily:

* 🔌 Which appliance consumed the most?
* ⚡ How much energy did each appliance use?
* 💰 What is the estimated electricity cost?
* 🌍 What is the estimated carbon impact?
* 💡 Where can consumption be reduced?

### 💭 GreenGrid's Answer

**GreenGrid transforms raw energy usage into meaningful insights and practical actions.**

```text
Raw Energy Data
      ↓
⚡ Energy Consumption
      ↓
💰 Cost Estimation
      ↓
🌍 Carbon Impact
      ↓
🔥 Top Consumers
      ↓
💡 Smart Recommendations
```

---

# 🌍 Sustainable Development Goals

GreenGrid is aligned with three Sustainable Development Goals:

| 🌱 SDG     | Focus                              | GreenGrid Connection                                                  |
| ---------- | ---------------------------------- | --------------------------------------------------------------------- |
| **SDG 7**  | Affordable and Clean Energy        | Encourages better understanding and management of energy consumption. |
| **SDG 11** | Sustainable Cities and Communities | Supports energy awareness for homes, rooms, and institutions.         |
| **SDG 13** | Climate Action                     | Estimates carbon emissions associated with electricity consumption.   |

---

# ✨ Core Features

## ⚡ 1. Energy Consumption Tracking

Record essential appliance information:

* 🔌 Appliance name
* ⚡ Power rating
* ⏱️ Usage hours
* 📅 Date / usage period

---

## 📊 2. Energy Calculation

Calculate estimated electricity consumption in:

> **kWh — Kilowatt-hours**

---

## 💰 3. Electricity Cost Estimation

Estimate the electricity cost based on:

> **Energy Consumption × Electricity Rate**

The electricity rate can be configured according to the chosen scenario.

---

## 🌍 4. Carbon Impact

Estimate the environmental impact of electricity consumption using a configurable:

> **Carbon Emission Factor**

---

## 🔥 5. Top Energy Consumers

Identify the appliances responsible for the highest energy consumption.

This helps users quickly understand:

> **"Where is most of my energy going?"**

---

## 💡 6. Energy-Saving Recommendations

Generate practical recommendations based on consumption patterns.

The purpose is not only to **measure** consumption, but also to encourage **better decisions**.

---

## 📄 7. Energy Report

Generate a consolidated report containing:

* ⚡ **Total Energy Consumption**
* 💰 **Estimated Electricity Cost**
* 🌍 **Estimated Carbon Emissions**
* 🔥 **Top Energy-Consuming Appliances**
* 💡 **Recommended Actions**

---

# 🧠 How GreenGrid Works

```text
                    🌱 GREENGRID
                         │
                         ▼
                ┌─────────────────┐
                │  Appliance Data │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Energy Record  │
                └────────┬────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   ENERGY PROCESSING  │
              │                      │
              │ ⚡ kWh Calculation   │
              │ 💰 Cost Calculation  │
              │ 🌍 Carbon Calculation│
              └──────────┬───────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Energy Report  │
                └────────┬────────┘
                         │
               ┌─────────┴─────────┐
               ▼                   ▼
        🔥 Top Consumers     💡 Recommendations
```

---

# 🏗️ Object-Oriented Design

GreenGrid is built around clear **Object-Oriented Programming concepts**.

The three core classes required by the challenge are:

---

## 🔌 `Appliance`

Represents an electrical appliance.

### Key Information

* **Name**
* **Power Rating**
* **Category / Identification**

### Example

```text
Appliance
├── Name: Air Conditioner
├── Power: 1500 W
└── Category: Cooling
```

---

## 📝 `EnergyRecord`

Represents the usage of an appliance over a defined period.

### Key Information

* Appliance
* Usage hours
* Date / period

### Example

```text
EnergyRecord
├── Appliance: Air Conditioner
├── Usage: 5 hours
└── Period: Daily
```

---

## 📊 `EnergyReport`

Aggregates the calculated information and provides the final energy insights.

### Includes

* Total kWh
* Estimated cost
* Estimated emissions
* Top-consuming appliances
* Recommended actions

---

# 🧮 Energy Intelligence

GreenGrid converts appliance usage into measurable energy insights.

## ⚡ Energy Consumption

```text
Energy (kWh)
=
Power (kW) × Usage Hours
```

---

## 💰 Estimated Electricity Cost

```text
Estimated Cost
=
Energy Consumption (kWh) × Electricity Rate
```

---

## 🌍 Estimated Carbon Emissions

```text
Estimated Emissions
=
Energy Consumption (kWh) × Emission Factor
```

> **Note:** The electricity rate and emission factor are configurable, allowing the prototype to be used with different scenarios and assumptions.

---

# 🔄 Application Workflow

```text
               👤 USER / INPUT
                     │
                     ▼
            🔌 Appliance Details
                     │
                     ▼
             📝 Energy Records
                     │
                     ▼
             ⚙️ Energy Engine
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        ⚡ kWh       💰 Cost    🌍 Carbon
          │          │          │
          └──────────┼──────────┘
                     ▼
              📊 Energy Report
                     │
            ┌────────┴────────┐
            ▼                 ▼
      🔥 Top Consumers   💡 Recommendations
```

---

# 📂 Repository Structure

```text
GreenGrid/
│
├── 📄 README.md
│
├── 📁 src/
│   └── 🐍 greengrid.py
│
├── 📁 documentation/
│   ├── 🎞️ presentation.pptx
│   └── 📑 report.docx
│
├── 📁 images/
│   ├── 🖼️ img1.jpg
│   ├── 🖼️ img2.jpg
│   ├── 🖼️ img3.jpg
│   ├── 🖼️ img4.jpg
│   └── 🖼️ ...
│
└── 📁 videos/
    └── 🎥 explanation.mp4
```

---

# 📌 Repository Guide

| File / Folder                     | Purpose                                  |
| --------------------------------- | ---------------------------------------- |
| `README.md`                       | 📖 Main project documentation            |
| `src/greengrid.py`                | 🐍 Complete Python prototype             |
| `documentation/presentation.pptx` | 🎞️ Hackathon presentation               |
| `documentation/report.docx`       | 📑 Detailed project report               |
| `images/`                         | 🖼️ Screenshots and project visuals      |
| `videos/explanation.mp4`          | 🎥 Project explanation and demonstration |

---

# 🛠️ Technology Stack

| Technology                      | Purpose                  |
| ------------------------------- | ------------------------ |
| 🐍 **Python**                   | Core application         |
| 🧩 **OOP**                      | Application architecture |
| 📊 **Energy Calculations**      | Consumption analysis     |
| 🌍 **Sustainability Analytics** | Carbon impact estimation |

### Core Concepts Demonstrated

* ✅ Python Fundamentals
* ✅ Classes and Objects
* ✅ Encapsulation
* ✅ Methods
* ✅ Data Processing
* ✅ Conditional Logic
* ✅ Calculations
* ✅ Report Generation

---

# ▶️ Getting Started

## 1️⃣ Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

## 2️⃣ Open the Project

```bash
cd GreenGrid
```

## 3️⃣ Run the Application

```bash
python src/greengrid.py
```

### 💡 Python 3 Alternative

```bash
python3 src/greengrid.py
```

---

# 🧪 Demonstration

GreenGrid is designed as a **functional prototype**, not just a concept.

The demonstration follows the complete process:

```text
Input
  ↓
🔌 Appliance & Usage Records
  ↓
⚡ Energy Calculation
  ↓
💰 Cost Estimation
  ↓
🌍 Carbon Estimation
  ↓
📊 Consumption Analysis
  ↓
🔥 Top Consumers
  ↓
💡 Energy-Saving Recommendations
  ↓
📄 Final Energy Report
```

---

# 📚 Documentation

## 📑 Project Report

> 📄 **[Open Project Report](documentation/report.docx)**

The project report covers:

* 🎯 Problem Statement
* 🌍 SDG Mapping
* 🎯 Objectives
* 🏗️ System Design
* 🧩 Classes and OOP Concepts
* 🧮 Algorithms and Logic
* 🔄 Input / Output Flow
* 🧪 Testing
* ⚠️ Limitations
* 🔮 Future Scope

---

## 🎞️ Presentation

> 📊 **[Open Presentation](documentation/presentation.pptx)**

The presentation covers:

* 🎯 Problem
* 🌍 SDG Relevance
* 💡 Solution
* 🏗️ Architecture / Workflow
* ✨ Key Features
* 🧩 OOP Implementation
* 🧪 Demo / Results
* 🔮 Future Improvements

---

# 🏆 Why GreenGrid?

GreenGrid brings together three important dimensions of energy management:

```text
                    ⚡ ENERGY
                       │
                       ▼
                 ┌───────────┐
                 │  GREENGRID │
                 └─────┬─────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
          💰 COST             🌍 CARBON
             │                   │
             └─────────┬─────────┘
                       ▼
                    💡 ACTION
```

GreenGrid is designed to answer a simple but important question:

> **"How can we turn energy consumption data into better decisions?"**

The answer is:

> **Measure → Understand → Analyze → Act**

---

# 🌱 Sustainability Impact

GreenGrid promotes energy awareness by connecting everyday electricity consumption with:

### ⚡ Energy

Understanding how much electricity is actually being consumed.

### 💰 Cost

Understanding the estimated financial impact of that consumption.

### 🌍 Carbon

Understanding the estimated environmental impact.

### 💡 Action

Identifying opportunities to reduce unnecessary consumption.

---

# 🔮 Future Scope

GreenGrid can be extended into a more advanced energy intelligence platform.

### 🏠 Smart Energy Management

* Multi-room monitoring
* Multi-home monitoring
* Institutional energy tracking

### 📈 Advanced Analytics

* Historical consumption trends
* Daily / weekly / monthly comparisons
* Peak consumption identification
* Consumption forecasting

### 📊 Interactive Dashboard

* Visual analytics
* Interactive charts
* Real-time statistics
* Appliance comparison

### 🔔 Intelligent Alerts

* High-consumption warnings
* Unusual usage detection
* Cost threshold notifications

### 📡 IoT Integration

* Smart meters
* Smart plugs
* Sensor-based energy measurement
* Real-time appliance monitoring

### ☁️ Cloud Integration

* Cloud-based records
* Remote monitoring
* Multi-user access

### 🤖 Advanced Intelligence

* Personalized recommendations
* Consumption pattern analysis
* Automated energy-saving suggestions

### 🌍 Expanded Sustainability Analytics

* Broader carbon analysis
* Sustainability benchmarking
* Long-term environmental impact tracking

---

# 🎯 Project Vision

> ## **Turn Energy Data Into Sustainable Action.**

GreenGrid aims to make energy information:

**Simple.**
**Understandable.**
**Measurable.**
**Actionable.**

---

# 🧩 Project Philosophy

> ### ⚡ Measure what you consume.
>
> ### 💰 Understand what it costs.
>
> ### 🌍 See its environmental impact.
>
> ### 💡 Take action.

---

# 👥 Author

## **Group 5**

**Mohamed Aathif**
**Paras Shah**
**Vetri Selvan**
**Sanket Hore**

---

# 🌱 GreenGrid

> **Smart Energy Consumption & Carbon Tracker**

**⚡ Energy • 💰 Cost • 🌍 Carbon • 💡 Action**

---

### ⭐ Built with Python • OOP • Sustainability in Mind
