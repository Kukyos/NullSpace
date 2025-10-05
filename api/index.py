from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import json
import sys
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NASA OSDR API Integration
async def fetch_nasa_experiments(limit: int = 15) -> List[Dict[str, Any]]:
    """Fetch experiments from NASA OSDR API"""
    try:
        search_url = "https://osdr.nasa.gov/osdr/data/search"
        
        async with aiohttp.ClientSession() as session:
            search_params = {
                'q': '*',  # Get all results, simpler and more reliable
                'size': limit,
                'from': 0
            }
            
            async with session.get(search_url, params=search_params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Handle OSDR API response format
                    hits_data = data.get('hits', {})
                    if isinstance(hits_data, dict):
                        total_hits = hits_data.get('total', {})
                        if isinstance(total_hits, dict):
                            total_count = total_hits.get('value', 0)
                        else:
                            total_count = total_hits
                        
                        study_hits = hits_data.get('hits', [])
                    else:
                        total_count = 0
                        study_hits = []
                    
                    if total_count == 0 or not study_hits:
                        logger.info("No studies found in OSDR API")
                        return []
                    
                    experiments = []
                    for hit in study_hits[:limit]:
                        experiment = format_nasa_experiment_osdr(hit)
                        if experiment:
                            experiments.append(experiment)
                    
                    logger.info(f"Successfully fetched {len(experiments)} experiments from NASA OSDR")
                    return experiments
                else:
                    logger.error(f"NASA API request failed with status: {response.status}")
                    return []
                    
    except Exception as e:
        logger.error(f"Error fetching NASA GeneLab data: {str(e)}")
        return []

def format_nasa_experiment_osdr(hit: Dict) -> Optional[Dict[str, Any]]:
    """Format NASA OSDR hit data for our application"""
    try:
        source = hit.get('_source', {})
        if not source:
            return None
        
        # Extract mission information
        mission_data = source.get('Mission', {})
        if isinstance(mission_data, dict):
            mission_name = mission_data.get('Name', 'Unknown Mission')
        else:
            mission_name = str(mission_data) if mission_data else 'Unknown Mission'
        
        # Extract keywords
        keywords = []
        factor_name = source.get('Study Factor Name', '')
        if factor_name:
            keywords.append(factor_name.lower())
        
        assay_type = source.get('Study Assay Technology Type', '')
        if assay_type:
            keywords.append(assay_type.lower())
        
        # Add space-related keywords based on content
        title = source.get('Study Title', '').lower()
        description = source.get('Study Description', '').lower()
        
        space_keywords = ['microgravity', 'spaceflight', 'space', 'ISS', 'bone', 
                         'muscle', 'cardiovascular', 'radiation', 'gene expression',
                         'inflammation', 'immune']
        
        for keyword in space_keywords:
            if keyword in title or keyword in description:
                keywords.append(keyword)
        
        # Extract data types
        data_types = []
        if assay_type:
            data_types.append(assay_type)
            
        assay_platform = source.get('Study Assay Technology Platform', '')
        if assay_platform:
            data_types.append(assay_platform)
            
        measurement_type = source.get('Study Assay Measurement Type', '')
        if measurement_type:
            data_types.append(measurement_type)
        
        # Truncate description
        description_text = source.get('Study Description', '')
        if len(description_text) > 400:
            description_text = description_text[:400] + '...'
        
        experiment = {
            'id': source.get('Accession', f"osdr-{hit.get('_id', 'unknown')}"),
            'title': source.get('Study Title', 'Unknown Study'),
            'summary': description_text,
            'organism': source.get('organism', 'Unknown organism'),
            'mission': mission_name,
            'keywords': list(set([k for k in keywords if k]))[:8],  # Remove empty and limit
            'dataTypes': list(set([dt for dt in data_types if dt]))[:5],  # Remove empty and limit
            'publicationCount': 0,  # Would need separate API call to get this
            'duration': 'Variable',
            'submissionDate': '',
            'releaseDate': source.get('Study Public Release Date', ''),
            'projectType': source.get('Project Type', ''),
            'flightProgram': source.get('Flight Program', ''),
            'spaceProgram': source.get('Space Program', ''),
            'managingCenter': source.get('Managing NASA Center', ''),
            'assayTechnology': assay_type
        }
        
        return experiment
        
    except Exception as e:
        logger.error(f"Error formatting OSDR experiment: {str(e)}")
        return None

def format_nasa_experiment(study: Dict) -> Optional[Dict[str, Any]]:
    """Format NASA study data for our application (legacy fallback)"""
    try:
        accession = study.get('accession', '')
        if not accession:
            return None
        
        # Extract organism
        organism = 'Unknown organism'
        if 'organisms' in study and study['organisms']:
            organism = study['organisms'][0].get('scientificName', organism)
        
        # Extract mission/project info
        mission = 'NASA Mission'
        if 'projectType' in study:
            mission = study['projectType']
        
        # Extract keywords from various fields
        keywords = []
        title_lower = study.get('title', '').lower()
        desc_lower = study.get('description', '').lower()
        
        space_keywords = ['microgravity', 'spaceflight', 'space', 'ISS', 'gene expression', 
                         'muscle atrophy', 'bone density', 'cardiovascular', 'radiation',
                         'plant growth', 'development', 'immune system']
        
        for keyword in space_keywords:
            if keyword in title_lower or keyword in desc_lower:
                keywords.append(keyword)
        
        # Extract data types
        data_types = []
        if 'assays' in study:
            for assay in study['assays']:
                if 'measurementType' in assay:
                    data_types.append(assay['measurementType'])
        
        experiment = {
            'id': accession,
            'title': study.get('title', 'Unknown Study'),
            'summary': (study.get('description', '').strip()[:400] + '...' 
                       if len(study.get('description', '')) > 400 
                       else study.get('description', '')),
            'organism': organism,
            'mission': mission,
            'keywords': keywords[:8],  # Limit keywords
            'dataTypes': list(set(data_types))[:5],  # Limit and dedupe data types
            'publicationCount': len(study.get('publications', [])),
            'duration': 'Variable',
            'submissionDate': study.get('submissionDate', ''),
            'releaseDate': study.get('releaseDate', ''),
            'projectType': study.get('projectType', ''),
            'studyType': study.get('studyType', '')
        }
        
        return experiment
        
    except Exception as e:
        logger.error(f"Error formatting experiment: {str(e)}")
        return None

async def search_nasa_experiments(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search NASA OSDR experiments by query"""
    try:
        search_url = "https://osdr.nasa.gov/osdr/data/search"
        
        async with aiohttp.ClientSession() as session:
            search_params = {
                'q': query,
                'size': limit,
                'from': 0
            }
            
            async with session.get(search_url, params=search_params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Handle OSDR API response format
                    hits_data = data.get('hits', {})
                    if isinstance(hits_data, dict):
                        total_hits = hits_data.get('total', {})
                        if isinstance(total_hits, dict):
                            total_count = total_hits.get('value', 0)
                        else:
                            total_count = total_hits
                        
                        study_hits = hits_data.get('hits', [])
                    else:
                        total_count = 0
                        study_hits = []
                    
                    if total_count == 0 or not study_hits:
                        return []
                    
                    experiments = []
                    for hit in study_hits:
                        experiment = format_nasa_experiment_osdr(hit)
                        if experiment:
                            experiments.append(experiment)
                    
                    return experiments
                else:
                    return []
                    
    except Exception as e:
        logger.error(f"Error searching NASA experiments: {str(e)}")
        return []

# Create FastAPI app for serverless deployment
app = FastAPI(
    title="NULLspace API",
    description="NASA Bioscience Data Explorer API",
    version="2.0.0"
)

# Configure CORS for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data for experiments (optimized for serverless)
mock_experiments = [
    {
        "id": "GLDS-21",
        "title": "Spaceflight Effects on Arabidopsis Gene Expression",
        "summary": "Investigation of how microgravity affects plant gene expression patterns in Arabidopsis thaliana during spaceflight missions.",
        "organism": "Arabidopsis thaliana",
        "mission": "STS-131",
        "keywords": ["microgravity", "gene expression", "plants", "spaceflight"],
        "dataTypes": ["RNA-Seq", "Microarray"],
        "publicationCount": 12,
        "duration": "14 days"
    },
    {
        "id": "GLDS-47",
        "title": "Muscle Atrophy in Microgravity",
        "summary": "Study of muscle protein degradation pathways in mouse models under simulated microgravity conditions.",
        "organism": "Mus musculus",
        "mission": "Rodent Research-1",
        "keywords": ["muscle atrophy", "microgravity", "protein degradation", "mice"],
        "dataTypes": ["Proteomics", "Histology"],
        "publicationCount": 8,
        "duration": "30 days"
    },
    {
        "id": "GLDS-104",
        "title": "Cardiac Function in Space",
        "summary": "Analysis of cardiovascular adaptations and cardiac muscle changes during long-duration spaceflight.",
        "organism": "Homo sapiens",
        "mission": "ISS Expedition 42",
        "keywords": ["cardiac", "cardiovascular", "spaceflight", "adaptation"],
        "dataTypes": ["Echocardiography", "Blood Analysis"],
        "publicationCount": 15,
        "duration": "180 days"
    },
    {
        "id": "GLDS-78",
        "title": "Bone Density Loss Studies",
        "summary": "Investigation of bone mineral density changes and osteoblast activity in microgravity environments.",
        "organism": "Rattus norvegicus",
        "mission": "SpaceX CRS-12",
        "keywords": ["bone density", "osteoblast", "calcium", "microgravity"],
        "dataTypes": ["X-ray", "Biochemistry"],
        "publicationCount": 6,
        "duration": "60 days"
    },
    {
        "id": "GLDS-173",
        "title": "Neural Development in Microgravity",
        "summary": "Study of neural stem cell differentiation and brain development under microgravity conditions.",
        "organism": "Homo sapiens",
        "mission": "ISS Expedition 56",
        "keywords": ["neural", "stem cells", "brain", "development"],
        "dataTypes": ["Single-cell RNA-Seq", "Imaging"],
        "publicationCount": 9,
        "duration": "21 days"
    }
]

# Mock knowledge graph data
mock_graph_data = {
    "nodes": [
        {"data": {"id": "microgravity", "label": "Microgravity", "type": "condition"}},
        {"data": {"id": "gene-expression", "label": "Gene Expression", "type": "process"}},
        {"data": {"id": "muscle-atrophy", "label": "Muscle Atrophy", "type": "outcome"}},
        {"data": {"id": "bone-loss", "label": "Bone Loss", "type": "outcome"}},
        {"data": {"id": "neural-changes", "label": "Neural Changes", "type": "outcome"}},
        {"data": {"id": "arabidopsis", "label": "Arabidopsis", "type": "organism"}},
        {"data": {"id": "mouse", "label": "Mouse", "type": "organism"}},
        {"data": {"id": "human", "label": "Human", "type": "organism"}},
        {"data": {"id": "spaceflight", "label": "Spaceflight", "type": "condition"}},
        {"data": {"id": "adaptation", "label": "Adaptation", "type": "process"}}
    ],
    "edges": [
        {"data": {"source": "microgravity", "target": "gene-expression", "label": "affects"}},
        {"data": {"source": "microgravity", "target": "muscle-atrophy", "label": "causes"}},
        {"data": {"source": "microgravity", "target": "bone-loss", "label": "induces"}},
        {"data": {"source": "spaceflight", "target": "adaptation", "label": "triggers"}},
        {"data": {"source": "gene-expression", "target": "arabidopsis", "label": "studied in"}},
        {"data": {"source": "muscle-atrophy", "target": "mouse", "label": "observed in"}},
        {"data": {"source": "bone-loss", "target": "human", "label": "measured in"}},
        {"data": {"source": "neural-changes", "target": "human", "label": "detected in"}}
    ]
}

@app.get("/")
async def root():
    return {"message": "NULLspace API v2.0 - NASA Bioscience Data Explorer"}

@app.get("/api/experiments")
async def get_experiments():
    """Get all NASA bioscience experiments from OSDR API"""
    try:
        experiments = await fetch_nasa_experiments()
        if experiments:
            return {"experiments": experiments, "dataSource": "NASA OSDR", "isRealData": True}
        else:
            # Fallback to mock data if NASA API returns no results
            return {"experiments": mock_experiments, "dataSource": "Mock Data", "isRealData": False}
    except Exception as e:
        # Fallback to mock data if NASA API fails
        logger.error(f"NASA API failed, using fallback data: {str(e)}")
        return {"experiments": mock_experiments, "dataSource": "Mock Data (API Error)", "isRealData": False}

@app.get("/api/knowledge-graph")
async def get_knowledge_graph():
    """Get knowledge graph data"""
    return mock_graph_data

@app.get("/api/search")
async def search_experiments(query: str = ""):
    """Search experiments by query"""
    if not query:
        try:
            experiments = await fetch_nasa_experiments()
            if experiments:
                return {"results": experiments, "dataSource": "NASA OSDR", "isRealData": True}
            else:
                return {"results": mock_experiments, "dataSource": "Mock Data", "isRealData": False}
        except Exception as e:
            logger.error(f"NASA API failed in search: {str(e)}")
            return {"results": mock_experiments, "dataSource": "Mock Data (API Error)", "isRealData": False}
    
    try:
        # Try NASA API search first
        nasa_results = await search_nasa_experiments(query)
        if nasa_results:
            return {"results": nasa_results, "query": query, "dataSource": "NASA OSDR", "isRealData": True}
    except Exception as e:
        logger.error(f"NASA search API failed: {str(e)}")
    
    # Fallback to mock data search
    query_lower = query.lower()
    filtered = []
    
    for exp in mock_experiments:
        # Search in title, organism, summary, and keywords
        if (query_lower in exp["title"].lower() or
            query_lower in exp["organism"].lower() or
            query_lower in exp["summary"].lower() or
            any(query_lower in keyword.lower() for keyword in exp["keywords"])):
            filtered.append(exp)
    
    return {"results": filtered, "query": query, "dataSource": "Mock Data", "isRealData": False}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

# For Vercel deployment
handler = app