#📊 Enterprise Cloud-Integrated E-Commerce Analytics & ML Engine
A high-performance Business Intelligence (BI) web application that processes e-commerce transactional data, manages cloud-ready data pipelines, and runs predictive machine learning models to forecast company revenue.
🔗 Live Application Link:
🚀 Key Architectural Highlights
Production-Ready Data Cleaning: Automated pipeline handling duplicate removal, systematic missing-value imputation (demographic median matching), and feature engineering.

Hybrid Cloud Architecture: Integration with AWS S3 via Boto3 API for live remote data fetching, equipped with an automated local failover mechanism to ensure 100% application uptime.

Interactive Presentation Layer: Fully responsive analytical UI built using Streamlit and optimized with memory-caching mechanisms (@st.cache_data) for lightning-fast loads.

Predictive Growth Engine: Integrated supervised Machine Learning (Linear Regression) model providing real-time forecasting based on budget simulation sliders.

🛠️ Technology Stack & Tools
Core Backend: Python 3.x

Data Processing & Analytics: Pandas, NumPy

Machine Learning Framework: Scikit-Learn (Linear Regression)

Cloud Infrastructure: AWS S3, Boto3 SDK

Data Visualization: Plotly Express, Matplotlib

Deployment & Hosting: Streamlit Community Cloud

📁 Repository Structure

├── app.py                  # Main Streamlit Web Application & ML Core
├── data_cleaning.py        # Baseline Backend Data Processing Pipeline Script
├── requirements.txt        # Production dependency log file
└── README.md               # Comprehensive project documentation
⚙️ How the Pipeline Works
1. Data Ingestion & Transformation
The pipeline reads multi-dimensional transactional records containing anomalies (missing metrics & duplicate indexes). It performs multi-step operations:

Drops structural duplicates to preserve registry authenticity.

Uses a vectorized pandas approach to handle missing age demographics.

Performs binning logic to segment data into targeted cohorts (Youth, Working Class, Senior).

2. Cloud Data Storage & Failover Routing
The storage layer attempts a cloud session connection using credentials to pull raw csv strings. If remote communication fails or credentials are restricted, a simulation array immediately fires up to guarantee structural continuity.

3. Predictive Modeling Engine
Using historical marketing performance metrics, the system trains a Linear Regression model. The dashboard presents an intuitive slider interface allowing end-users to simulate marketing spend projections, mapping the trends instantly on a Plotly curve graph.
