
---

# 🌾 DeepCrop AI 2.0 – Sugarcane Pest Detection System

**DeepCrop AI 2.0** is the official **Round 2 submission** for **AgriThon 2.0** by **Team DeepCrop**.
It’s a **full-stack, multimodal AI pipeline** for detecting two major sugarcane pests — **Dead Heart** and **Tiller** — using a fusion of **YOLOv8 image analysis** and **TabNet questionnaire classification**.

This project was developed for the hackathon conducted by the **School of Computer Science and Information Systems, VIT Vellore**, sponsored by the **Department of Biotechnology, Govt. of India**.

---

## 📸 Screenshots & Demos

<img width="2816" height="1536" alt="Gemini_Generated_Image_ip931sip931sip93 (1)" src="https://github.com/user-attachments/assets/aecfb77d-3e94-4bdf-b5cc-6141e3be4c0a" />

### **System Architecture**

<img width="3840" height="3824" alt="agrithon round 2" src="https://github.com/user-attachments/assets/9238e7d3-8909-4c87-befd-6859e3269996" />

### **Web Application – Dashboard View**

<img width="1919" height="1199" alt="image" src="https://github.com/user-attachments/assets/7aeeb5b6-f0e3-4271-93bf-b64e1dffa420" />


### **Prediction Flow GIF**

![DeepCrop2 0-MadewithClipchamp-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/d1d53601-b824-4360-8433-b40cfe7a5fb4)

---

## 🏛️ System Architecture & Pipeline

Our solution builds on the Round 1 foundation, but extends it into a **production-ready web platform**.

1. **Data Preparation & Annotation**

   * Dead Heart: Segmentation masks (YOLOv8-seg)
   * Tiller: Bounding boxes (YOLOv8)
   * Annotation handled in **Roboflow + CVAT (offline)**.
2. **Training Phase**

   * Dead Heart → YOLOv8 Segmentation Model
   * Tiller → YOLOv8 Detection Model
   * Questionnaire Models → Two separate **TabNet classifiers** trained on curated CSV symptom datasets (>500 samples each).
3. **Fusion Logic**

   * Weighted combination of image score (0.6) and questionnaire score (0.4).
4. **Web Application**

   * **Frontend:** React + Vite for responsive, multilingual UI.
   * **Backend:** FastAPI serving YOLOv8 and TabNet inference APIs, weather API integration.
5. **Deployment**

   * Dockerized backend and frontend, served via Nginx for production readiness.

---

## ✨ Key Features

* **🧠 Multimodal Fusion:** YOLOv8 + TabNet for accurate, explainable results.
* **🌿 Pest Segmentation & Detection:** Precise overlays for Dead Heart, bounding boxes for Tiller.
* **🌤 Weather Risk Engine:** Location-based pest risk assessment.
* **🌍 Multilingual UI:** English, Hindi, Tamil, Telugu.
* **⚡ Real-time Predictions:** API responses under 500ms on standard hardware.
* **📱 Field-friendly:** Lightweight APIs and offline-friendly questionnaire flow.

---

## 🛠️ Tech Stack

| Component               | Technology / Library                     |
| ----------------------- | ---------------------------------------- |
| **Backend**             | FastAPI, PyTorch, YOLOv8, TabNet, OpenCV |
| **Frontend**            | React 18, Vite, CSS3                     |
| **Image Augmentation**  | Albumentations, Roboflow                 |
| **Model Serving**       | Uvicorn + ASGI                           |
| **Weather Integration** | OpenWeather API                          |
| **Containerization**    | Docker, Docker Compose, Nginx            |
| **Data Processing**     | Pandas, NumPy, Scikit-learn              |

---

## 📊 Model Performance Summary

| Model                   | Task                 | Dataset Size | Metric                  | Inference Time |
| ----------------------- | -------------------- | ------------ | ----------------------- | -------------- |
| YOLOv8-seg (Dead Heart) | Segmentation         | 3,512 images | mAP\@0.5: **89.3%**     | \~240ms/image  |
| YOLOv8 (Tiller)         | Object Detection     | 3,512 images | mAP\@0.5: **88.7%**     | \~230ms/image  |
| TabNet (Dead Heart)     | Questionnaire Class. | 500+ samples | Accuracy: **92.4%**     | \~30ms/sample  |
| TabNet (Tiller)         | Questionnaire Class. | 500+ samples | Accuracy: **92.4%**     | \~30ms/sample  |
| Fusion Output           | Weighted 0.6/0.4     | Combined     | Final Accuracy: **94%** | \~300ms total  |

---

## 💻 How to Run

### Prerequisites

* Python ≥ 3.9
* Node.js ≥ 16
* Git
* Docker (optional for containerized deployment)

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

**Access:**

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

## 👥 Team DeepCrop

| Name               | Email                                    |
| ------------------ | -----------------------------------------|
| Hariharan S        | hariharan.s2022d@vitstudent.ac.in        |
| Naresh R           | naresh.r2022a@vitstudent.ac.in           |
| Mohammed Arfath    | mohammedarfath.r2022@vitstudent.ac.in    |
| Mohammad Yusuf K A | mohammadyusuf.ka2022@vitstudent.ac.in    |

---

## 📜 License

Licensed under the MIT License – see the `LICENSE` file.

---

## 📞 Support

Open an [issue on GitHub](https://github.com/Mohammed0Arfath/DeepCrop-AI-2.0/issues).

---

