# NULLspace Development Setup

## Prerequisites Installation

### Windows Setup

1. **Install Node.js** (version 16+)
   - Download from https://nodejs.org/
   - Verify: `node --version` and `npm --version`

2. **Install Python** (version 3.9+)
   - Download from https://python.org/
   - Verify: `python --version` and `pip --version`

## Quick Development Start

### Terminal 1 - Backend Setup
```powershell
cd backend
pip install -r requirements.txt
python main.py
```

### Terminal 2 - Frontend Setup  
```powershell
cd frontend
npm install
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development Notes

- The backend uses mock NASA data for demo purposes
- AI models load lazily to improve startup time
- TailwindCSS compile errors in IDE can be ignored - they work at runtime
- Knowledge graph uses placeholder SVG until Cytoscape is fully integrated

## Production Deployment

See README.md for full deployment instructions.