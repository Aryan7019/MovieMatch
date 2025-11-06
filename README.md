# 🎬 Cinematch - Movie Recommendation System

A smart movie recommendation system built with **Streamlit** that suggests similar movies based on content-based filtering using machine learning.

## 🚀 Live Demo
**[Try it live on Streamlit Cloud!](https://cinematch-movie-recommendations.streamlit.app)**

## ✨ Features
- 🎭 **4,800+ Movies** from TMDB dataset
- 🤖 **AI-Powered Recommendations** using cosine similarity
- 🎨 **Beautiful Dark Mode UI** with movie posters
- ⚡ **Ultra-Fast Performance** with optimized data loading (27.6MB compressed data)
- 📱 **Fully Responsive Design** - Perfect on mobile, tablet, and desktop
- 🎯 **Real-time Poster Fetching** from TMDB API

## 🛠️ Technology Stack
- **Frontend:** Streamlit with responsive CSS
- **Backend:** Python
- **ML Algorithm:** TF-IDF + Cosine Similarity  
- **Data:** TMDB 5000 Movies Dataset (Ultra-compressed)
- **Libraries:** pandas, scikit-learn, requests

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/Aryan7019/Cinematch.git
cd Cinematch
pip install -r requirements.txt
```

### 2. Data Files Ready!
✅ **No download needed!** Ultra-compressed data (27.6MB) is included in the repository.

### 3. Run the App
```bash
streamlit run app.py
```

## 📱 Responsive Design
- **Mobile-First:** Touch-friendly interface with optimized layouts
- **Tablet-Friendly:** Perfect viewing on all tablet sizes  
- **Desktop-Enhanced:** Full-featured experience with hover effects
- **Dark Mode:** Professional appearance across all devices

## 🎯 How It Works

This recommendation system uses **cosine similarity** to find movies similar to your selection by analyzing:
- **Genres** (Action, Comedy, Drama, etc.)
- **Keywords** (space war, romance, etc.)  
- **Cast** (top 3 actors)
- **Directors**

The system processes movie features using TF-IDF vectorization and computes similarity scores to suggest the most relevant recommendations.

## 🚀 Deployment Ready
- **Ultra-compressed data** (84.6% size reduction)
- **GitHub compatible** (under 50MB limit)
- **Streamlit Cloud optimized**
- **Fast loading** with advanced caching

## 📊 Performance
- **Initial Load:** ~5-10 seconds (one-time data loading)
- **Recommendations:** ~1-2 seconds per request
- **Memory Usage:** ~200MB
- **File Size:** 27.6MB (ultra-compressed)

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## 📄 License
This project is licensed under the MIT License.
