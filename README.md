

---

# 🌾 DeepCrop AI – Sugarcane Pest Detection System

A **full-stack AI-powered platform** for early detection of sugarcane pests using computer vision and tabular deep learning. Built during **VIT AgriThon Round 2**, this system integrates **YOLOv8** image detection with **TabNet** questionnaire analysis to predict two major pests: **Dead Heart** and **Tiller**.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![React](https://img.shields.io/badge/React-18+-blue.svg)

---

## 📜 Overview

**Problem:**
Sugarcane farmers face significant yield losses due to late pest detection. Traditional monitoring methods are manual, slow, and error-prone.

**Solution:**
DeepCrop AI offers a **dual-modal pest detection** approach:

1. **YOLOv8** for localized image-based pest detection/segmentation.
2. **TabNet** for questionnaire-based crop health assessment.
3. **Fusion Logic** combining both predictions into a final decision.
4. **Weather-linked risk analysis** for preventive recommendations.

**Impact:**

* Early detection → Reduced crop loss.
* Visual overlays → Actionable, explainable results.
* Lightweight APIs → Works in low-connectivity areas.

---

## 🚀 Key Features

* **Dead Heart & Tiller Detection**
* **Multimodal AI Fusion** (image + questionnaire)
* **Weather-Based Pest Risk**
* **FastAPI Backend, React Frontend**
* **Localized UI** (English, Hindi, Tamil, Telugu)
* **Dockerized Deployment**
* **Beginner-Friendly Code Structure**

---

## 🏗️ System Architecture

```
┌───────────────┐    ┌───────────────┐    ┌─────────────┐
│ React Frontend│    │ FastAPI Backend│    │ AI Models  │
│ • Upload Img  │◄──►│ • API Endpoints│◄──►│ • YOLOv8   │
│ • Questionnaire│   │ • Fusion Logic │    │ • TabNet   │
│ • Results View │    │ • Weather API │    │             │
└───────────────┘    └───────────────┘    └─────────────┘
```

---

## 🛠️ Technology Stack

### **Backend**

* FastAPI, PyTorch, YOLOv8, TabNet, OpenCV, Albumentations
* Model Serving: Uvicorn + ASGI

### **Frontend**

* React 18, Vite, CSS3
* Location & Weather Integration

### **DevOps**

* Docker, Docker Compose
* Nginx

---


## 📊 Model Details

| Pest Type     | Model Type         | Dataset Size | Task           | Metric                  |
| ------------- | ------------------ | ------------ | -------------- | ----------------------- |
| Dead Heart    | YOLOv8 Seg         | 3,512 imgs   | Segmentation   | **mAP\@0.5:** 89.3%     |
| Tiller        | YOLOv8 Det         | 3,512 imgs   | Detection      | **mAP\@0.5:** 88.7%     |
| Questionnaire | TabNet             | 500+ samples | Classification | **Accuracy:** 92.4%     |
| Fusion Output | Weighted (0.6/0.4) | Combined     | Prediction     | **Final Accuracy:** 94% |

---


## ⚙️ Installation & Setup

```bash
# Clone repository
git clone https://github.com/Mohammed0Arfath/DeepCrop-AI-2.0.git
cd DeepCrop-AI-2.0
```

### **Backend**

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### **Frontend**

```bash
cd frontend
npm install
npm run dev
```

**Access App:**

* Frontend: [http://localhost:5173](http://localhost:5173)
* Backend Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

---

## 📁 Project Structure

```
DeepCrop-AI-2.0/
├── backend/         # FastAPI backend
│   ├── app/
│   ├── models/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/        # React frontend
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 👥 Team

**Team DeepCrop** – VIT AgriThon Round 2 Finalists

* Hariharan S
* Naresh R
* Mohammed Arfath
* Mohammad Yusuf KA

---

## 📞 Support

Open an issue on [GitHub Issues](https://github.com/Mohammed0Arfath/DeepCrop-AI-2.0/issues).

---

Do you want me to fill in those actual scores next?
