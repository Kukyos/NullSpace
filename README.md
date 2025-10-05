# NULLspace - NASA Bioscience Data Explorer

🚀 **An AI-powered platform for exploring NASA bioscience experiments through interactive knowledge graphs and intelligent summarization.**

![NULLspace](https://img.shields.io/badge/NULLspace-v1.0.0-blue?style=for-the-badge&logo=nasa)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python)

## 🌌 Overview

NULLspace transforms how researchers explore NASA's bioscience data by providing:

- **AI-Powered Summaries**: Intelligent experiment summarization using BART and T5 models
- **Interactive Knowledge Graphs**: Visual exploration of experiment relationships via Cytoscape.js
- **Semantic Search**: Find relevant experiments using natural language queries
- **Real NASA Data**: Integration with NASA GeneLab and Space Biology databases

## 🛠️ Tech Stack

### Frontend
- **React 18** with modern hooks and functional components
- **TailwindCSS** for responsive, space-themed UI design
- **Cytoscape.js** for interactive network visualizations
- **Plotly.js** for scientific data charts and plots

### Backend
- **FastAPI** for high-performance async API endpoints
- **Python 3.9+** with type hints and modern async/await patterns

### AI/ML
- **HuggingFace Transformers** (BART, T5) for text summarization
- **KeyBERT** for intelligent keyword extraction
- **Sentence Transformers** for semantic similarity matching

### Data Sources
- **NASA GeneLab**: Omics data from spaceflight experiments
- **NASA Space Biology Database**: Experiment metadata and results
- **Cached JSON**: Optimized data storage for fast retrieval

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.9+ and pip
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/nullspace.git
cd nullspace
```

2. **Set up the backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Set up the frontend**
```bash
cd ../frontend
npm install
```

4. **Start the development servers**

Backend (terminal 1):
```bash
cd backend
python main.py
```

Frontend (terminal 2):
```bash
cd frontend
npm start
```

5. **Open your browser**
Navigate to `http://localhost:3000` to explore NULLspace!

## 🎯 Features

### 🔍 Intelligent Search
- Semantic search across NASA bioscience experiments
- Filter by organism, mission, or research keywords
- AI-powered relevance scoring

### 📊 Knowledge Graph Visualization
- Interactive network of experiment relationships
- Visual connections between organisms, missions, and findings
- Dynamic node sizing and color-coding
- Zoom, pan, and node selection interactions

### 🤖 AI Summarization
- Automatic experiment summary generation
- Key insight extraction from research papers
- Keyword and topic identification
- Cross-experiment similarity analysis

### 🌟 Modern UI/UX
- Space-themed dark interface with NASA color palette
- Glass morphism effects and cyber-glow animations
- Responsive design for desktop and mobile
- Smooth transitions and loading states

## 📁 Project Structure

```
nullspace/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Header.js
│   │   │   ├── SearchBar.js
│   │   │   ├── ExperimentCard.js
│   │   │   └── KnowledgeGraph.js
│   │   ├── App.js           # Main app component
│   │   └── index.css        # Global styles
│   ├── package.json
│   └── tailwind.config.js   # TailwindCSS configuration
├── backend/                 # FastAPI server
│   ├── main.py             # API routes and server
│   └── requirements.txt    # Python dependencies
├── ai/                     # AI/ML modules
│   ├── summarizer.py       # Text summarization
│   └── knowledge_graph.py  # Graph generation
├── data/                   # Data processing
│   └── nasa_client.py      # NASA API client
└── docs/                   # Documentation
```

## 🔮 API Endpoints

### Experiments
- `GET /api/experiments` - List all experiments with optional filtering
- `GET /api/experiments/{id}` - Get detailed experiment information
- `GET /api/search?query={term}` - Semantic search across experiments

### Knowledge Graph
- `GET /api/knowledge-graph` - Generate graph data for visualization
- `GET /api/knowledge-graph?experiment_ids=1,2,3` - Graph for specific experiments

### Platform
- `GET /api/stats` - Platform statistics and metrics

## 🎨 Design Philosophy

NULLspace embraces a **space-age aesthetic** with:

- **Dark cosmic backgrounds** with gradient overlays
- **NASA-inspired color palette** (NASA blue #0B3D91, NASA red #FC3D21)
- **Glassmorphism effects** for modern, floating UI elements
- **Cyber-glow accents** with cosmic purple highlights
- **Monospace fonts** for technical data display
- **Smooth animations** for professional polish

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Performance

- **Sub-second** search response times
- **Lightweight** React bundle (~500KB gzipped)
- **Efficient** AI model loading with lazy initialization
- **Cached** NASA data for improved performance
- **Responsive** UI with 60fps animations

## 🚀 Deployment

### Docker (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Manual Deployment
1. Build the React frontend: `npm run build`
2. Serve with nginx or similar
3. Deploy FastAPI backend with gunicorn
4. Set up reverse proxy for API routes

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NASA** for providing open access to bioscience data
- **HuggingFace** for state-of-the-art AI models
- **Cytoscape.js** for powerful network visualization
- **The space biology research community** for advancing our understanding of life in space

---

**Built with ❤️ for the future of space exploration**

*NULLspace - Where data meets the cosmos* 🌌