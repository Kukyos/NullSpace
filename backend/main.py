from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional
import os
import sys
import json
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import our AI modules
from ai.summarizer import ExperimentSummarizer
from ai.knowledge_graph import KnowledgeGraphGenerator
from data.nasa_client import NASADataClient

app = FastAPI(
    title="NULLspace API",
    description="NASA Bioscience Data Explorer Backend",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI components
summarizer = ExperimentSummarizer()
knowledge_graph = KnowledgeGraphGenerator()
nasa_client = NASADataClient()

@app.get("/")
async def root():
    return {
        "message": "Welcome to NULLspace API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/api/experiments")
async def get_experiments(
    search: Optional[str] = None,
    organism: Optional[str] = None,
    limit: int = 50
):
    """Get NASA bioscience experiments with optional filtering"""
    try:
        experiments = await nasa_client.get_experiments(
            search_term=search,
            organism=organism,
            limit=limit
        )
        
        # Add AI-generated summaries
        for experiment in experiments:
            if not experiment.get('summary'):
                experiment['summary'] = await summarizer.generate_summary(experiment)
                experiment['keywords'] = await summarizer.extract_keywords(experiment)
        
        return JSONResponse(content={"experiments": experiments})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/experiments/{experiment_id}")
async def get_experiment_detail(experiment_id: str):
    """Get detailed information about a specific experiment"""
    try:
        experiment = await nasa_client.get_experiment_by_id(experiment_id)
        
        if not experiment:
            raise HTTPException(status_code=404, detail="Experiment not found")
        
        # Generate enhanced details
        experiment['summary'] = await summarizer.generate_summary(experiment)
        experiment['keywords'] = await summarizer.extract_keywords(experiment)
        experiment['related_experiments'] = await nasa_client.get_related_experiments(experiment_id)
        
        return JSONResponse(content=experiment)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/knowledge-graph")
async def get_knowledge_graph(experiment_ids: Optional[str] = None):
    """Generate knowledge graph data for visualization"""
    try:
        if experiment_ids:
            exp_ids = experiment_ids.split(',')
        else:
            # Get top experiments for general graph
            experiments = await nasa_client.get_experiments(limit=10)
            exp_ids = [exp['id'] for exp in experiments]
        
        graph_data = await knowledge_graph.generate_graph(exp_ids)
        
        return JSONResponse(content=graph_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search_experiments(
    query: str,
    limit: int = 20
):
    """Intelligent search across experiments using AI similarity"""
    try:
        # Use semantic search for better results
        results = await nasa_client.semantic_search(query, limit=limit)
        
        # Enhance with AI summaries
        for result in results:
            result['summary'] = await summarizer.generate_summary(result)
            result['relevance_score'] = await summarizer.calculate_relevance(query, result)
        
        # Sort by relevance
        results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return JSONResponse(content={"results": results, "query": query})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_platform_stats():
    """Get platform statistics and metrics"""
    try:
        stats = await nasa_client.get_platform_stats()
        
        return JSONResponse(content=stats)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)