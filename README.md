
# 🌱 ADAPTIVE CROP DEFENCE SYSTEM FOR SMART AGRICULTURE

### Croycore – Smart Farming Through IoT, Climate Monitoring & Intelligent Risk Analysis

Croycore is a responsive, farmer-focused Progressive Web Application (PWA) prototype designed to monitor agricultural environmental conditions, identify climate-related risks, and support localized crop protection.

The system integrates sensor, farm, crop-yield, and district-level climate datasets to simulate agricultural monitoring. It focuses on detecting frost, extreme heat, drought, and heavy rainfall conditions through an interactive dashboard, voice alerts, and device-control simulation.

---

## 🚀 Key Features

- 🌡️ **Live Farm Monitoring** – Displays environmental readings and zone-wise conditions.
- ❄️ **Climate Risk Detection** – Identifies frost, heat stress, drought, and heavy rainfall scenarios.
- 🌾 **Smart Zone Management** – Monitors multiple agricultural zones independently.
- 🎮 **Demo Simulator** – Simulates different weather conditions without physical hardware.
- 🔊 **Voice Alerts** – Provides spoken notifications using the browser Web Speech API.
- 🔥 **Device Control** – Demonstrates zone-based heater control through the dashboard.
- 🚨 **Alert Management** – Displays alerts and supports alert acknowledgement.
- 📊 **Historical Monitoring** – Provides access to sensor reading history.
- 🌱 **Crop Profiles** – Supports crop-specific environmental threshold information.
- 📱 **Progressive Web App** – Provides an app-like experience with service-worker caching.
- 📲 **Responsive Interface** – Designed for mobile, tablet, and desktop screens.

---

## 🏗️ System Architecture

```text
             AGRICULTURAL FIELD
                     |
             Smart Climate Nodes
                     |
             Sensor Data Collection
                     |
              LoRa / MQTT Boundary
                     |
                Backend Server
               (Node.js + Express)
                     |
              Climate Risk Engine
                     |
             Agricultural Datasets
                     |
                API / SSE
                     |
              React PWA Dashboard
                     |
          +----------+----------+
          |          |          |
        Alerts   Monitoring  Device Control
          |          |          |
          +----------+----------+
                     |
                   Farmer
```

**Note:** The current prototype uses a backend simulator and supplied datasets. Physical sensor and LoRa/MQTT communication are planned integration boundaries.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, TypeScript |
| UI | Responsive PWA, Touch-Friendly Interface |
| Backend | Node.js, Express |
| Data Processing | CSV Data Processing |
| Communication | REST API, Server-Sent Events (SSE) |
| Voice Feedback | Browser Web Speech API |
| Offline Support | Service Worker |
| Data Sources | Sensor, Farm, Yield & District Climate CSV |
| Risk Analysis | Simulator-Based Climate Risk Engine |

---

## 🌡️ Climate Risk Monitoring

Croycore is designed to identify important agricultural climate conditions and provide understandable alerts.

| Climate Condition | System Response |
|---|---|
| Frost Night | Detects low-temperature conditions and highlights frost risk |
| Heat Wave | Identifies extreme temperature conditions |
| Drought | Highlights insufficient moisture conditions |
| Heavy Rain | Demonstrates rainfall-related risk alerts |
| All Clear | Resets the simulated risk condition |

### 🎮 Demo Scenario

1. Open the **Farm** screen.
2. Select **Frost Night** under Demo Simulator.
3. Zone 3 temperature changes to **2.5°C**, with high humidity.
4. The risk card and alert timeline update.
5. Press the speaker button to hear the voice alert.
6. Open the **Control** screen and switch on the Zone 3 heater.
7. Return to **Alerts** and acknowledge the notification.

Other scenarios:
- Heat Wave
- Drought
- Heavy Rain
- All Clear

---

## 📊 Dataset Integration

The prototype uses four supplied CSV datasets:

- **Sensor Dataset:** Environmental readings collected from sensor nodes.
- **Farm Dataset:** Farm and agricultural zone information.
- **Yield Dataset:** Crop yield information for agricultural insights.
- **District Climate Dataset:** District-level climate information.

**Data Handling:** The 76 MB climate dataset remains server-side. The browser receives only the required aggregate and profile responses.

---

## 🔌 API Documentation

The backend provides REST API endpoints for monitoring, simulation, device control, risk analysis, and data integration.

### Farm & Zone Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/zones` | Retrieve agricultural zones |
| GET | `/api/farms/demo` | Retrieve demo farm information |
| GET | `/api/zones/:id/history` | Retrieve historical readings |

### Alerts & Device Control

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/alerts` | Retrieve climate alerts |
| POST | `/api/alerts/:id/ack` | Acknowledge an alert |
| POST | `/api/devices/:zone/:device` | Control a zone-based device |

### Simulation & Risk Analysis

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/simulate` | Simulate climate conditions |
| GET | `/api/risk` | Retrieve climate risk information |
| GET | `/api/crop-profile` | Retrieve crop-specific profiles |
| GET | `/api/insights/yield` | Retrieve crop yield insights |

### Data Integration & Streaming

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/ingest` | Receive sensor data |
| POST | `/api/push/subscribe` | Handle push subscription requests |
| GET | `/live` | Receive live updates through SSE |

**Backend Implementation:** `server/index.mjs` manages CSV loading, simulator operations, and the risk engine.

---

## 📁 Project Structure

```text
Croycore/
│
├── data/
│   ├── sensor-data.csv
│   ├── farm-data.csv
│   ├── yield-data.csv
│   └── district-climate.csv
│
├── server/
│   └── index.mjs
│
├── public/
│   └── service-worker.js
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── assets/
│   └── ...
│
├── package.json
├── package-lock.json
├── index.html
└── README.md
```

*Note: Update the example filenames and folders to match your actual repository.*

---

## ⚙️ Installation & Setup

### Prerequisites

- Node.js
- npm
- Git

### Step 1: Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### Step 2: Navigate to the Project Folder

```bash
cd Croycore
```

### Step 3: Install Dependencies

```bash
npm install
```

### Step 4: Start the Application

```bash
npm run dev
```

### Step 5: Open in Browser

```text
http://localhost:5173
```

The Vite development server proxies `/api` requests to the Express simulator running on port `8787`.

### Run Only the Backend API

```bash
npm run server
```

---

## 🔄 Data Flow

1. Sensor datasets provide environmental readings.
2. The backend loads and manages agricultural data.
3. The simulator generates different climate conditions.
4. The risk engine evaluates environmental conditions.
5. API endpoints provide processed information to the frontend.
6. SSE delivers live updates to the dashboard.
7. The dashboard displays readings, alerts, and zone status.
8. Farmers interact with demo device controls and acknowledge alerts.

---

## 🔊 Voice Alert System

Croycore integrates the browser Web Speech API to provide audio feedback.

- Announces important climate-risk alerts.
- Helps users understand abnormal environmental conditions.
- Supports voice feedback through a user-triggered speaker button.
- Requires a user gesture in browsers that restrict automatic audio playback.

---

## 📱 Progressive Web Application (PWA)

The application uses service-worker caching to improve accessibility.

- Caches the application shell.
- Supports an app-like browsing experience.
- Keeps API requests network-first for fresh readings.
- Provides a responsive interface across different screen sizes.

---

## 🔐 Current Prototype Limitations

The following features are integration boundaries and are not fully implemented as production services:

- Physical sensor and hardware integration.
- Actual LoRa/MQTT communication.
- Push notification delivery.
- SMS and WhatsApp notifications.
- Machine-learning model training.
- Production-level automated climate-control hardware.

The current backend simulator demonstrates the intended system workflow. The existing API contract is designed to support future hardware and external-service integration without requiring major changes to the React interface.

---

## 🔮 Future Enhancements

- Integrate ESP32-based physical sensor nodes.
- Establish LoRa/MQTT communication between field devices and the gateway.
- Implement a trained machine-learning model for climate-risk prediction.
- Integrate physical heating and cooling devices.
- Add real-time weather API integration.
- Introduce multilingual voice alerts for farmers.
- Enable push notifications and SMS alerts.
- Expand crop-specific profiles and threshold management.
- Improve offline data synchronization.
- Support large-scale farms with multiple monitoring zones.

---

## 🌍 Project Impact

Croycore aims to support sustainable and climate-resilient agriculture through localized environmental monitoring and early risk identification.

- Reduces dependence on continuous manual monitoring.
- Supports early identification of climate-related crop risks.
- Encourages efficient and localized crop protection.
- Promotes technology-driven agricultural management.
- Supports sustainable farming practices.

---

## 👩‍💻 Project Information

| Detail | Description |
|---|---|
| Project Title | Adaptive Crop Defence System for Smart Agriculture |
| Project Name | Croycore |
| Category | Smart Agriculture, IoT, Climate Monitoring |
| Application Type | Farmer-Facing Progressive Web Application |
| Development Approach | Modular and Scalable Architecture |

---

## 📄 License

This project is developed for academic and prototype demonstration purposes. Add an appropriate open-source license if you intend to allow public reuse and distribution.

---

<p align="center">
  <b>🌱 Croycore – Smarter Monitoring, Safer Crops, Sustainable Agriculture.</b>
</p>
