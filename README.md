# SoilGenie: AI-Powered Agricultural Intelligence

![SoilGenie Professional Banner](https://github.com/Aliyuprof100/soilgenie-app/blob/main/static/images/logo.png) 
<!-- Optional: Create a banner image (1280x640px) with your logo and a farm background and host it online -->

**The operating system for the next generation of Nigerian agriculture. We translate satellite data into farmer prosperity.**

**Official Submission for the NigComSat Accelerator Program Hackathon.**

---

| **Quick Links** | |
|---|---|
| [**Watch Our 90-Second Video Demo**](https://your-video-link-goes-here.com) | [**View Our Pitch Deck**](https://your-pitch-deck-link-goes-here.com) |
|---|---|
| **Live Application Status:** `Deployment in Progress` | **Version:** `1.0.0 (MVP)` |

---

## 1. The Vision

**SoilGenie** is a dual-role, mobile-first platform designed to solve the critical information gap in Nigerian agriculture. Our mission is to democratize precision farming by making sophisticated soil analysis and hyperlocal weather forecasting accessible and affordable for every farmer. By leveraging **Earth Observation (EO)** and **Artificial Intelligence**, we empower farmers to increase yields, reduce input costs, and build more sustainable and profitable businesses.

## 2. The Problem: The High Cost of Uncertainty

The majority of Nigerian farmers operate with limited data, leading to systemic inefficiencies:
*   **Fertilizer Guesswork:** Sub-optimal application of fertilizers leads to wasted capital and potential environmental damage.
*   **Inaccessible Lab Testing:** Traditional soil analysis is too slow, expensive, and geographically sparse to be a viable option for most.
*   **Unpredictable Weather:** Regional weather forecasts are often too generic to inform critical, farm-level decisions.

This uncertainty is a primary barrier to achieving national food security and maximizing the potential of our agricultural sector. This is a problem that cannot be solved at scale on the ground; it requires a view from space.

## 3. Our Solution: A Platform for the Entire Ecosystem

SoilGenie addresses this challenge with a unique, two-pronged platform architecture:

| For the Independent Farmer | For the Agri-Entrepreneur (Agent) |
|---|---|
| A direct-to-farmer portal where tech-savvy farm managers can map their own land, receive instant analysis, track farm health over time, and view hyperlocal weather forecasts on a personal dashboard. | A "business-in-a-box" tool for local entrepreneurs. The agent dashboard allows them to manage a portfolio of farmer clients, perform analysis on their behalf, and deliver crucial insights via a universally accessible **SMS channel**. |

This model ensures that we can serve the top end of the market directly while building a trusted, scalable human network to reach rural and remote farming communities.

## 4. Key Features & Technology

This repository contains the full source code for our functional Minimum Viable Product.

#### Core Features:
*   ✅ **Dual-Role User System:** Secure registration and tailored dashboards for both **Farmers** and **Agents**.
*   ✅ **Interactive Geospatial Mapping:** A fully responsive Leaflet.js interface for precise farm boundary mapping using GNSS.
*   ✅ **Crop-Specific Analysis:** A feature to select the intended crop, allowing for more tailored (simulated AI) recommendations.
*   ✅ **Live Weather Integration:** Provides a 5-day hyperlocal weather forecast for a farm's location via the Open-Meteo API.
*   ✅ **SMS Delivery System:** Delivers the final analysis directly to any mobile phone using the Twilio API, bridging the digital divide.
*   ✅ **Professional UI/UX:** A stunning, fully responsive landing page and a clean, intuitive user portal built with Bootstrap 5.

#### Technology Stack:
*   **Backend:** Python 3.11+, Flask, Flask-SQLAlchemy, Flask-Login, Gunicorn
*   **Database:** PostgreSQL (Production), SQLite (Development)
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Leaflet.js
*   **Deployment:** Architected for cloud deployment on Render.
*   **Core APIs:** Twilio (SMS), Open-Meteo (Weather)
*   **Space Technology:** Leverages concepts from **Earth Observation (Sentinel-2)** and **GNSS**.

## 5. Getting Started: Running the Project Locally

The application is fully functional in a local environment.

**Prerequisites:**
*   Python 3.10+
*   Git

**Setup Instructions:**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Aliyuprof100/soilgenie-app.git
    cd soilgenie-app
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    # On Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # On Mac/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your environment variables:**
    *   Create a file named `.env` in the root directory.
    *   Copy the contents of `.env.example` (or add the required keys: `SECRET_KEY`, `TWILIO_ACCOUNT_SID`, etc.).
5.  **Initialize and upgrade the database:**
    ```bash
    # Set the Flask App (Mac/Linux)
    export FLASK_APP=run.py 
    # Or on Windows
    # set FLASK_APP=run.py
    
    flask db upgrade
    ```
6.  **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

## 6. Project Roadmap

Our MVP is the foundation. Our vision for the future includes:
*   **Q4 2025:** Full integration with live **Google Earth Engine** satellite data.
*   **Q1 2026:** Launch of our pilot program with 50 agents in a target agricultural zone.
*   **Q3 2026:** Integration of advanced data layers (soil type, topography) and development of predictive pest/disease models.
*   **2027:** Launch of our FinTech integration for input financing and marketplace linkages.

---
*Note: We are actively resolving a platform-specific import path issue on our cloud deployment. The fully functional codebase is provided here for technical review, and we are confident in making the live URL available shortly after the hackathon submission.*