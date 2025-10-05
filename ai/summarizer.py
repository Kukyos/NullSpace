"""
AI-powered experiment summarization using HuggingFace transformers
"""
import asyncio
from typing import Dict, List, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from keybert import KeyBERT
import torch

class ExperimentSummarizer:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize BART for summarization
        self.summarizer = None
        self.keyword_extractor = KeyBERT()
        
        # Load models lazily
        self._models_loaded = False
    
    async def _load_models(self):
        """Lazy load AI models to improve startup time"""
        if not self._models_loaded:
            try:
                # Use a smaller, faster model for demo purposes
                self.summarizer = pipeline(
                    "summarization",
                    model="facebook/bart-large-cnn",
                    device=0 if self.device == "cuda" else -1,
                    max_length=150,
                    min_length=50,
                    do_sample=False
                )
                self._models_loaded = True
                print("✅ AI models loaded successfully")
            except Exception as e:
                print(f"⚠️ Error loading models: {e}")
                # Fallback to mock summaries for demo
                self._models_loaded = "mock"
    
    async def generate_summary(self, experiment: Dict) -> str:
        """Generate AI summary for an experiment"""
        await self._load_models()
        
        try:
            # Combine experiment metadata for summarization
            text_to_summarize = self._prepare_text_for_summary(experiment)
            
            if self._models_loaded == "mock":
                return self._generate_mock_summary(experiment)
            
            # Generate summary using BART
            summary = self.summarizer(
                text_to_summarize,
                max_length=130,
                min_length=30,
                do_sample=False
            )[0]['summary_text']
            
            return summary
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._generate_mock_summary(experiment)
    
    async def extract_keywords(self, experiment: Dict) -> List[str]:
        """Extract key terms from experiment using KeyBERT"""
        await self._load_models()
        
        try:
            text = self._prepare_text_for_keywords(experiment)
            
            # Extract keywords
            keywords = self.keyword_extractor.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),
                stop_words='english'
            )[:8]  # Take top 8 keywords
            
            return [kw[0] for kw in keywords]
            
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return self._generate_mock_keywords(experiment)
    
    async def calculate_relevance(self, query: str, experiment: Dict) -> float:
        """Calculate relevance score between query and experiment"""
        # Simple relevance scoring for demo
        # In production, use sentence transformers for semantic similarity
        
        text = self._prepare_text_for_keywords(experiment).lower()
        query_terms = query.lower().split()
        
        matches = sum(1 for term in query_terms if term in text)
        score = matches / len(query_terms) if query_terms else 0
        
        return min(score, 1.0)
    
    def _prepare_text_for_summary(self, experiment: Dict) -> str:
        """Prepare experiment text for summarization"""
        parts = []
        
        if experiment.get('title'):
            parts.append(f"Study: {experiment['title']}")
        
        if experiment.get('description'):
            parts.append(experiment['description'])
        
        if experiment.get('organism'):
            parts.append(f"Organism studied: {experiment['organism']}")
        
        if experiment.get('mission'):
            parts.append(f"Mission: {experiment['mission']}")
        
        if experiment.get('factors'):
            parts.append(f"Factors: {', '.join(experiment['factors'])}")
        
        text = ". ".join(parts)
        
        # Truncate if too long for model
        return text[:1024] if len(text) > 1024 else text
    
    def _prepare_text_for_keywords(self, experiment: Dict) -> str:
        """Prepare experiment text for keyword extraction"""
        parts = []
        
        for field in ['title', 'description', 'organism', 'mission']:
            if experiment.get(field):
                parts.append(str(experiment[field]))
        
        return " ".join(parts)
    
    def _generate_mock_summary(self, experiment: Dict) -> str:
        """Generate mock summary when AI models fail"""
        organism = experiment.get('organism', 'biological samples')
        mission = experiment.get('mission', 'space mission')
        
        summaries = [
            f"This study investigates the effects of spaceflight conditions on {organism} during the {mission}.",
            f"Research examining how microgravity environment affects {organism} biological processes.",
            f"Comprehensive analysis of {organism} responses to space environment conditions during {mission}.",
            f"Investigation of molecular and cellular changes in {organism} under spaceflight conditions."
        ]
        
        # Simple hash-based selection for consistency
        hash_val = hash(experiment.get('id', 'default')) % len(summaries)
        return summaries[hash_val]
    
    def _generate_mock_keywords(self, experiment: Dict) -> List[str]:
        """Generate mock keywords when AI models fail"""
        base_keywords = ['spaceflight', 'microgravity', 'gene expression', 'space biology']
        
        if experiment.get('organism'):
            base_keywords.append(experiment['organism'].lower())
        
        if experiment.get('mission'):
            base_keywords.append(experiment['mission'])
        
        return base_keywords[:6]