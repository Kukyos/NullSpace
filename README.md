# 🚀 NULLspace - NASA Bioscience Data Explorer

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Kukyos/NullSpace)

An AI-powered web application that explores and visualizes NASA bioscience experiments through intelligent summarization and interactive knowledge graphs.

## ✨ Features

- **🤖 AI-Powered Summarization**: Uses HuggingFace BART models to generate intelligent summaries of NASA experiments
- **🕸️ Interactive Knowledge Graphs**: Dynamic visualization of relationships between experiments, organisms, and findings  
- **🔍 Smart Search**: Real-time search with debouncing, suggestions, and semantic filtering
- **📱 Responsive Design**: Modern, space-themed UI that works across all devices
- **⚡ Real-time Data**: Integration with NASA GeneLab and Space Biology databases
- **🎨 Dynamic UI**: Multiple view modes (Grid/List/Graph), advanced filtering, and smooth animations

## 🛠️ Tech Stack

### Frontend
- **React 18** with modern hooks and context
- **TailwindCSS** for responsive, utility-first styling  
- **Cytoscape.js** for interactive knowledge graph visualization
- **Custom animations** and glass morphism design

### Backend  
- **FastAPI** for high-performance Python API
- **HuggingFace Transformers** for AI summarization (BART model)
- **KeyBERT** for intelligent keyword extraction
- **Sentence Transformers** for semantic relationship mapping

### Deployment
- **Vercel** for serverless deployment
- **GitHub** for version control and CI/CD

## 🚀 Live Demo

**Deploy your own instance instantly:**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Kukyos/NullSpace)

## 📁 Project Structure

```
NULLspace/
├── frontend/              # React application
│   ├── src/
│   │   ├── components/   # UI components
│   │   │   ├── Header.js
│   │   │   ├── SearchBar.js
│   │   │   ├── ExperimentCard.js
│   │   │   ├── ExperimentModal.js
│   │   │   ├── KnowledgeGraph.js
│   │   │   └── Toast.js
│   │   ├── App.js        # Main application
│   │   └── index.css     # Styles with animations
│   └── public/
├── api/                   # Serverless API for Vercel
│   ├── index.py          # FastAPI serverless handler
│   └── requirements.txt
├── backend/              # Local development server
│   ├── main.py
│   └── requirements.txt
├── ai/                   # AI models and processing
├── data/                 # Data collection scripts
├── vercel.json           # Vercel deployment config
└── README.md
```

## 🏃‍♂️ Quick Start

### Option 1: Deploy to Vercel (Recommended)

1. Click the "Deploy with Vercel" button above
2. Connect your GitHub account  
3. Deploy automatically - done! 🎉

### Option 2: Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kukyos/NullSpace.git
   cd NullSpace
   ```

2. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Setup Backend** (in a new terminal)
   ```bash
   cd backend  
   pip install -r requirements.txt
   python main.py
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🎯 Key Features Showcase

### Dynamic Search & Filtering
- ⚡ **Real-time search** with 300ms debouncing
- 💡 **Smart suggestions** for quick searches
- 🏷️ **Category filters** (Plants, Animals, Microgravity, etc.)
- 📊 **Multiple sort options** (Relevance, Title, Publications, etc.)

### Interactive Experiment Cards
- 🎨 **Multiple view modes**: Grid, List, and Graph views
- 🖱️ **Hover animations** and smooth transitions
- 🔗 **Direct NASA GeneLab links** for each experiment
- 📱 **Fully responsive** design

### Advanced Modal System
- ⌨️ **Keyboard navigation** (Escape to close)
- 🖱️ **Click-outside-to-close** functionality
- 🔔 **Toast notifications** for user feedback
- 🚀 **Related experiments** discovery

### Knowledge Graph Visualization
- 🕸️ **Interactive network** of experiment relationships
- 🎯 **Click to focus** on specific experiments
- 📊 **Real-time statistics** (nodes, edges, connections)
- 🌈 **Color-coded** node types

## 🌐 API Endpoints

- `GET /api/experiments` - Get all NASA bioscience experiments
- `GET /api/search?query={term}` - Search experiments by keyword
- `GET /api/knowledge-graph` - Get knowledge graph data
- `GET /health` - API health check

## 🎨 UI/UX Highlights

- **🌌 Space-themed design** with NASA-inspired color palette
- **✨ Glass morphism effects** and subtle animations
- **📱 Mobile-first responsive** design
- **⚡ Performance optimized** with React.memo and useMemo
- **🎭 Smooth transitions** and loading states
- **🔔 User feedback** with toast notifications

## 🚀 Deployment on Vercel

The project is optimized for Vercel deployment with:

- **📦 Serverless API** in `/api/index.py`
- **⚡ Static frontend** build optimization
- **🔧 Automatic builds** on git push
- **🌍 Global CDN** distribution

### Manual Vercel Deployment

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel --prod`
3. Follow the prompts

## 🧪 Development Features

- **🔄 Hot reload** for both frontend and backend
- **🧪 Mock data** for offline development
- **📊 Comprehensive logging** and error handling
- **🎯 TypeScript-ready** component structure

## 📈 Performance Features

- **⚡ Debounced search** (300ms delay)
- **🎯 Memoized filtering** and sorting
- **📦 Code splitting** and lazy loading
- **🗜️ Optimized bundle size** with tree shaking

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **🚀 NASA GeneLab** for providing bioscience experiment data
- **🤗 HuggingFace** for pre-trained AI models  
- **⚡ Vercel** for amazing deployment platform
- **💎 Open source community** for incredible tools and libraries

## 📞 Contact & Links

- **📂 Repository**: [github.com/Kukyos/NullSpace](https://github.com/Kukyos/NullSpace)
- **🚀 Deploy**: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Kukyos/NullSpace)

---

**Built with ❤️ for NASA bioscience exploration** 🧬🚀