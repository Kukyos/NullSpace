"""
NASA data client for fetching bioscience experiments
"""
import asyncio
import aiohttp
import json
from typing import Dict, List, Optional
from pathlib import Path
import os

class NASADataClient:
    def __init__(self):
        self.genelab_base_url = "https://genelab-data.ndc.nasa.gov/genelab/data/study"
        self.session = None
        
        # Cache for demo data
        self.cache_dir = Path("data/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Mock data for demo purposes
        self.mock_experiments = self._load_mock_data()
    
    async def get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def get_experiments(
        self,
        search_term: Optional[str] = None,
        organism: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """Fetch NASA bioscience experiments"""
        try:
            # For MVP, use mock data with filtering
            experiments = self.mock_experiments.copy()
            
            # Apply filters
            if search_term:
                search_lower = search_term.lower()
                experiments = [
                    exp for exp in experiments
                    if (search_lower in exp.get('title', '').lower() or
                        search_lower in exp.get('description', '').lower() or
                        search_lower in exp.get('organism', '').lower() or
                        any(search_lower in kw.lower() for kw in exp.get('keywords', [])))
                ]
            
            if organism:
                organism_lower = organism.lower()
                experiments = [
                    exp for exp in experiments
                    if organism_lower in exp.get('organism', '').lower()
                ]
            
            return experiments[:limit]
            
        except Exception as e:
            print(f"Error fetching experiments: {e}")
            return self.mock_experiments[:limit]
    
    async def get_experiment_by_id(self, experiment_id: str) -> Optional[Dict]:
        """Get detailed experiment data by ID"""
        try:
            # Find in mock data
            for exp in self.mock_experiments:
                if exp['id'] == experiment_id:
                    return exp
            
            return None
            
        except Exception as e:
            print(f"Error fetching experiment {experiment_id}: {e}")
            return None
    
    async def get_related_experiments(self, experiment_id: str, limit: int = 5) -> List[Dict]:
        """Find experiments related to the given one"""
        try:
            base_exp = await self.get_experiment_by_id(experiment_id)
            if not base_exp:
                return []
            
            base_keywords = set(kw.lower() for kw in base_exp.get('keywords', []))
            base_organism = base_exp.get('organism', '').lower()
            
            related = []
            for exp in self.mock_experiments:
                if exp['id'] == experiment_id:
                    continue
                
                # Calculate similarity score
                exp_keywords = set(kw.lower() for kw in exp.get('keywords', []))
                keyword_overlap = len(base_keywords & exp_keywords)
                organism_match = 1 if base_organism == exp.get('organism', '').lower() else 0
                
                similarity_score = keyword_overlap + organism_match
                
                if similarity_score > 0:
                    exp_copy = exp.copy()
                    exp_copy['similarity_score'] = similarity_score
                    related.append(exp_copy)
            
            # Sort by similarity and return top results
            related.sort(key=lambda x: x['similarity_score'], reverse=True)
            return related[:limit]
            
        except Exception as e:
            print(f"Error finding related experiments: {e}")
            return []
    
    async def semantic_search(self, query: str, limit: int = 20) -> List[Dict]:
        """Perform semantic search across experiments"""
        # For MVP, use simple keyword matching
        # In production, use sentence transformers for semantic similarity
        
        query_terms = set(query.lower().split())
        results = []
        
        for exp in self.mock_experiments:
            # Create searchable text
            searchable_text = ' '.join([
                exp.get('title', ''),
                exp.get('description', ''),
                exp.get('organism', ''),
                ' '.join(exp.get('keywords', []))
            ]).lower()
            
            # Simple term matching
            matches = sum(1 for term in query_terms if term in searchable_text)
            if matches > 0:
                exp_copy = exp.copy()
                exp_copy['search_score'] = matches / len(query_terms)
                results.append(exp_copy)
        
        # Sort by relevance
        results.sort(key=lambda x: x['search_score'], reverse=True)
        return results[:limit]
    
    async def get_platform_stats(self) -> Dict:
        """Get platform statistics"""
        return {
            'total_experiments': len(self.mock_experiments),
            'organisms_studied': len(set(exp.get('organism', '') for exp in self.mock_experiments)),
            'missions_covered': len(set(exp.get('mission', '') for exp in self.mock_experiments)),
            'keywords_indexed': sum(len(exp.get('keywords', [])) for exp in self.mock_experiments),
            'last_updated': '2024-10-05T00:00:00Z'
        }
    
    def _load_mock_data(self) -> List[Dict]:
        """Load mock NASA experiment data for demo"""
        return [
            {
                'id': 'GLDS-21',
                'title': 'Spaceflight Effects on Arabidopsis Gene Expression',
                'description': 'This study examines how microgravity environment during spaceflight affects gene expression patterns in Arabidopsis thaliana plants. The research focuses on identifying genes that are differentially expressed under microgravity conditions compared to ground controls.',
                'organism': 'Arabidopsis thaliana',
                'mission': 'STS-131',
                'duration_days': 15,
                'keywords': ['microgravity', 'gene expression', 'plants', 'spaceflight', 'transcriptomics'],
                'factors': ['Microgravity', 'Spaceflight Environment'],
                'data_types': ['RNA-seq', 'Microarray'],
                'publication_count': 12,
                'dataset_size_gb': 2.3
            },
            {
                'id': 'GLDS-47',
                'title': 'Muscle Atrophy in Microgravity Environment',
                'description': 'Investigation of muscle protein degradation pathways in mouse models under simulated microgravity conditions. This study aims to understand the molecular mechanisms behind muscle atrophy observed in astronauts.',
                'organism': 'Mus musculus',
                'mission': 'Rodent Research-1',
                'duration_days': 30,
                'keywords': ['muscle atrophy', 'microgravity', 'protein degradation', 'mice', 'proteomics'],
                'factors': ['Simulated Microgravity', 'Muscle Unloading'],
                'data_types': ['Proteomics', 'Histology'],
                'publication_count': 8,
                'dataset_size_gb': 1.7
            },
            {
                'id': 'GLDS-173',
                'title': 'Microbial Communities in Space Environment',
                'description': 'Comprehensive analysis of how space environment affects microbial communities, particularly focusing on E. coli behavior and adaptation mechanisms in microgravity.',
                'organism': 'Escherichia coli',
                'mission': 'ISS Expedition-45',
                'duration_days': 45,
                'keywords': ['microbiome', 'bacteria', 'space adaptation', 'microgravity', 'genomics'],
                'factors': ['Microgravity', 'Radiation', 'Confined Environment'],
                'data_types': ['16S rRNA', 'Whole Genome Sequencing'],
                'publication_count': 6,
                'dataset_size_gb': 3.1
            },
            {
                'id': 'GLDS-242',
                'title': 'Bone Density Changes in Long-Duration Spaceflight',
                'description': 'Study of bone density changes and calcium metabolism in astronauts during long-duration missions to the International Space Station.',
                'organism': 'Homo sapiens',
                'mission': 'ISS Long Duration',
                'duration_days': 180,
                'keywords': ['bone density', 'calcium', 'osteoporosis', 'astronauts', 'metabolism'],
                'factors': ['Microgravity', 'Radiation', 'Confined Environment', 'Altered Nutrition'],
                'data_types': ['DEXA Scan', 'Blood Analysis', 'Urine Analysis'],
                'publication_count': 15,
                'dataset_size_gb': 0.8
            },
            {
                'id': 'GLDS-104',
                'title': 'Radiation Effects on Fruit Fly Development',
                'description': 'Examination of how space radiation affects fruit fly development and reproductive cycles during spaceflight missions.',
                'organism': 'Drosophila melanogaster',
                'mission': 'STS-121',
                'duration_days': 12,
                'keywords': ['radiation', 'development', 'fruit flies', 'reproduction', 'genetics'],
                'factors': ['Space Radiation', 'Microgravity'],
                'data_types': ['Developmental Biology', 'Genetics'],
                'publication_count': 9,
                'dataset_size_gb': 1.2
            },
            {
                'id': 'GLDS-189',
                'title': 'Plant Root Growth in Microgravity',
                'description': 'Investigation of how microgravity affects root growth patterns and gravitropism responses in various plant species.',
                'organism': 'Brassica rapa',
                'mission': 'ISS Expedition-52',
                'duration_days': 28,
                'keywords': ['root growth', 'gravitropism', 'plants', 'microgravity', 'development'],
                'factors': ['Microgravity', 'Altered Gravity Vector'],
                'data_types': ['Imaging', 'Morphological Analysis'],
                'publication_count': 7,
                'dataset_size_gb': 2.8
            },
            {
                'id': 'GLDS-321',
                'title': 'Cardiovascular Changes in Spaceflight',
                'description': 'Study of cardiovascular system adaptations in astronauts during and after spaceflight missions.',
                'organism': 'Homo sapiens',
                'mission': 'ISS Multiple Expeditions',
                'duration_days': 120,
                'keywords': ['cardiovascular', 'heart', 'blood pressure', 'astronauts', 'adaptation'],
                'factors': ['Microgravity', 'Fluid Shifts', 'Exercise Countermeasures'],
                'data_types': ['ECG', 'Ultrasound', 'Blood Analysis'],
                'publication_count': 18,
                'dataset_size_gb': 1.5
            },
            {
                'id': 'GLDS-418',
                'title': 'Yeast Stress Response in Space',
                'description': 'Analysis of stress response mechanisms in yeast cells exposed to spaceflight conditions.',
                'organism': 'Saccharomyces cerevisiae',
                'mission': 'ISS Expedition-58',
                'duration_days': 21,
                'keywords': ['yeast', 'stress response', 'microgravity', 'cell biology', 'genomics'],
                'factors': ['Microgravity', 'Temperature Variations'],
                'data_types': ['RNA-seq', 'Cell Culture'],
                'publication_count': 5,
                'dataset_size_gb': 1.9
            }
        ]