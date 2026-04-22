# 🔥 AI Pokedex — Pokémon Identifier

An AI-powered app that identifies Pokémon from images and generates structured information using LLMs.

---

## 🚀 Features

- 🧠 CNN-based image classification
- 📸 Upload Pokémon images
- 🔍 Confidence score display
- 🤖 LLM-powered Pokémon insights
- 🌐 FastAPI backend
- 🎨 Streamlit frontend

---

## 🏗️ Project Structure
Pokedex/
│
├── Frontend/ # Streamlit UI
├── Backend/ # FastAPI server
├── Work_dir/ # Model + Agent + Pipeline
├── model/ # Trained CNN model
├── predictions/ # Saved outputs
├── logs/ # Application logs
│
├── .env # API keys
├── requirements # Dependencies
└── README.md

---

## 🧠 Model Details

- Built with **PyTorch CNN**
- Input size: `64x64`
- Normalization: ImageNet stats
- Output:
  - Pokémon label
  - Confidence score

---

## ⚙️ How It Works

1. User uploads an image (Streamlit UI)
2. CNN model predicts Pokémon
3. Backend API fetches Pokémon details
4. LLM processes and formats response
5. Results displayed in UI

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key


---

## 🛠️ Installation

```bash
# Clone repository
git clone https://github.com/your-username/pokedex.git
cd pokedex

# Create virtual environment
python -m venv .venv

# Activate environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements
▶️ Run the Project
1️⃣ Start Backend
cd Backend
python back_server.py

Backend runs at:

http://127.0.0.1:8000
2️⃣ Start Frontend
cd Frontend
streamlit run front_server.py
🧪 Example Workflow
Upload Pokémon image
Model predicts → pikachu ⚡
Confidence → 98.7%
Backend fetches info
LLM formats output
⚠️ Known Issues
Evolutions field may return null (handled in schema)
Model path is currently hardcoded (should be relative for deployment)
Backend must be running before frontend
💡 Future Improvements
🌍 Deploy on cloud (AWS / Render / HuggingFace Spaces)
📱 Mobile-friendly UI
⚡ Real-time camera detection
🧠 Upgrade CNN → Vision Transformer
📊 Add Grad-CAM visualization
🧬 Pokémon comparison feature
🧑‍💻 Author

Anurag
AI Engineer (in progress 🚀)

⭐ Final Note

This project combines:

Deep Learning
Backend APIs
LLM Agents
Full-stack development

A solid step toward production-level AI systems.

⭐ If you like this project, consider giving it a star!