🌏 Digital Divide Predictor: AI-Powered Policy Intelligence
Bridging the gap between digital infrastructure and human inclusion.

The Digital Divide Predictor is an AI-driven Decision Support System (DSS) designed to transform raw Aadhaar enrolment and update data into actionable governance insights. It moves beyond static dashboards to provide predictive risk scores, helping policymakers identify digitally excluded districts before they fall behind.

🚨 The Problem
India possesses world-class digital infrastructure, yet millions remain digitally excluded. The core issue is not the absence of technology, but the absence of intelligence in decision-making.

Policymakers currently lack:

A unified view of where the digital divide is most severe.

Predictive insights to act proactively rather than reactively.

Data-backed guidance on specific interventions and budget allocation.

This results in welfare exclusion, delayed services, and inefficient resource allocation.

💡 The Solution
We have built a Policy Intelligence Engine that converts massive datasets into interpretable governance metrics.

Key Capabilities:
🔮 Predictive Risk Modeling: Classifies districts into Thriving, Struggling, or Critical using an Ensemble ML model.

📊 Digital Literacy Index (DLI): A proprietary metric derived from biometric/demographic update ratios and enrolment efficiency.

📝 Actionable Recommendations: Generates specific, budget-aware policy interventions (e.g., "Maintain Infrastructure" vs. "Target Remaining Gaps") based on district risk profiles.

📍 Regional Performance Matrix: Comparative analysis of states and districts to spot structural inequalities.

⚙️ How It Works (Methodology)
1. Data Foundation (Trust & Scale)
We utilize official UIDAI Aadhaar data (sourced from data.gov.in), ensuring national coverage and policy-grade reliability.

Inputs: Enrolments, Demographic Updates, Biometric Updates.

Scope: 1M+ Records analyzed across 1000+ Districts.

2. Feature Intelligence Layer
Raw data is transformed into decision-ready indicators:

Digital Literacy Index (DLI): Measures the intensity of digital engagement.

Infrastructure Readiness: Assesses the physical reach of centers.

Update Ratios: Analyzes the balance between demographic and biometric updates to gauge user sophistication.

3. AI-Driven Prediction (Ensemble Engine)
We employ a robust Ensemble Learning approach combining the strengths of three powerful algorithms:

Random Forest: Handles complex, non-linear data patterns.

Gradient Boosting: Sequential learning to reduce error.

AdaBoost: Focuses on hard-to-classify edge cases.

Result: High-accuracy risk prediction with explainable feature importance (top predictor: DLI).

📸 Dashboard Preview
1. Executive Dashboard
A high-level view of the nation's digital health, highlighting critical districts and total records analyzed. (Place screenshot image_6a6261.jpg here)

2. Regional Performance Matrix
State-wise performance distribution to identify regional clusters of excellence or concern. (Place screenshot image_6a65e2.jpg here)

3. ML Model Transparency
Full visibility into ROC Curves, Confusion Matrices, and Feature Importance to ensure trust in AI decisions. (Place screenshot image_6a6646.jpg here)

4. District Risk Predictor & Recommendations
Granular analysis of specific districts with tailored, budget-estimated recommendations. (Place screenshot image_6a6568.jpg here)

🛠️ Technology Stack
Language: Python

Frontend/Dashboard: Streamlit

Data Processing: Pandas, NumPy

Machine Learning: Scikit-Learn (RandomForest, AdaBoost, GradientBoosting)

Visualization: Plotly, Matplotlib, Seaborn


🚀 Installation & Usage
To run this application locally, follow these steps:

1. Clone the repository

Bash
git clone https://github.com/yourusername/digital-divide-predictor.git
cd digital-divide-predictor
2. Create a virtual environment (Optional but recommended)

Bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3. Install dependencies

Bash
pip install -r requirements.txt
4. Run the application

Bash
streamlit run app.py
The app will open in your browser at http://localhost:8501.


🚀 Installation & Usage
To run this application locally, follow these steps:

1. Clone the repository

Bash
git clone https://github.com/yourusername/digital-divide-predictor.git
cd digital-divide-predictor
2. Create a virtual environment (Optional but recommended)

Bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3. Install dependencies

Bash
pip install -r requirements.txt
4. Run the application

Bash
streamlit run app.py
The app will open in your browser at http://localhost:8501.

### Contributors 
Deep Khatke , Swayam , Yug , Murli , vikas 


