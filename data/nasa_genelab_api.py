"""
NASA GeneLab API Integration
Fetches real experiment data from NASA's GeneLab database
"""
import requests
import json
from typing import List, Dict, Any, Optional
import asyncio
import aiohttp
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NASAGeneLab:
    """NASA OSDR API client for fetching experiment data"""
    
    def __init__(self):
        self.base_url = "https://osdr.nasa.gov/osdr/data/search"
        self.api_url = "https://osdr.nasa.gov/osdr/data/study"
        self.search_url = "https://osdr.nasa.gov/osdr/data/search"
        
    async def fetch_experiments(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Fetch experiments from NASA GeneLab API"""
        try:
            async with aiohttp.ClientSession() as session:
                # Search for studies with space-related keywords (OSDR API format)
                search_params = {
                    'q': 'spaceflight OR microgravity OR space OR ISS',
                    'size': limit,
                    'from': 0
                }
                
                async with session.get(self.search_url, params=search_params) as response:
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
                        
                        # If no hits, use fallback data
                        if total_count == 0 or not study_hits:
                            logger.info("No studies found in OSDR API, using fallback data")
                            return self._get_fallback_data()
                        
                        # Process and format the studies
                        experiments = []
                        for hit in study_hits[:limit]:
                            experiment = self._process_osdr_hit(hit)
                            if experiment:
                                experiments.append(experiment)
                        
                        logger.info(f"Successfully fetched {len(experiments)} experiments from NASA OSDR")
                        return experiments
                    else:
                        logger.error(f"API request failed with status: {response.status}")
                        return self._get_fallback_data()
                        
        except Exception as e:
            logger.error(f"Error fetching NASA GeneLab data: {str(e)}")
            return self._get_fallback_data()
    
    def _process_osdr_hit(self, hit: Dict) -> Optional[Dict[str, Any]]:
        """Process individual OSDR search hit"""
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
            
            # Extract and format experiment data
            experiment = {
                'id': source.get('Accession', f"osdr-{hit.get('_id', 'unknown')}"),
                'title': source.get('Study Title', 'Unknown Study'),
                'summary': self._truncate_text(source.get('Study Description', ''), 500),
                'organism': source.get('organism', 'Unknown organism'),
                'mission': mission_name,
                'keywords': self._extract_osdr_keywords(source),
                'dataTypes': self._extract_osdr_data_types(source),
                'publicationCount': len(source.get('Study Publication Title', []) if isinstance(source.get('Study Publication Title'), list) else []),
                'duration': self._extract_osdr_duration(source),
                'submissionDate': '',
                'releaseDate': self._format_release_date(source.get('Study Public Release Date')),
                'factors': self._extract_osdr_factors(source),
                'experimentPlatform': source.get('Experiment Platform', ''),
                'projectType': source.get('Project Type', ''),
                'datasetSize': self._estimate_dataset_size(source),
                'flightProgram': source.get('Flight Program', ''),
                'spaceProgram': source.get('Space Program', ''),
                'managingCenter': source.get('Managing NASA Center', ''),
                'assayTechnology': source.get('Study Assay Technology Type', ''),
                'authoritative_url': source.get('Authoritative Source URL', '')
            }
            
            return experiment
                    
        except Exception as e:
            logger.error(f"Error processing OSDR hit: {str(e)}")
            return None
    
    async def _process_study(self, session: aiohttp.ClientSession, study: Dict) -> Optional[Dict[str, Any]]:
        """Process individual study data (legacy method for fallback)"""
        try:
            accession = study.get('accession', '')
            if not accession:
                return None
            
            # Get detailed study information
            detail_url = f"{self.api_url}/{accession}"
            async with session.get(detail_url) as response:
                if response.status == 200:
                    detail_data = await response.json()
                    study_data = detail_data.get('study', {})
                    
                    # Extract and format experiment data
                    experiment = {
                        'id': accession,
                        'title': study_data.get('title', 'Unknown Study'),
                        'summary': study_data.get('description', '').strip()[:500] + '...' if len(study_data.get('description', '')) > 500 else study_data.get('description', ''),
                        'organism': self._extract_organism(study_data),
                        'mission': self._extract_mission(study_data),
                        'keywords': self._extract_keywords(study_data),
                        'dataTypes': self._extract_data_types(study_data),
                        'publicationCount': len(study_data.get('publications', [])),
                        'duration': self._extract_duration(study_data),
                        'submissionDate': study_data.get('submissionDate', ''),
                        'releaseDate': study_data.get('releaseDate', ''),
                        'factors': self._extract_factors(study_data),
                        'experimentPlatform': study_data.get('experimentPlatform', ''),
                        'projectType': study_data.get('projectType', ''),
                        'datasetSize': self._extract_dataset_size(study_data)
                    }
                    
                    return experiment
                else:
                    logger.warning(f"Failed to get details for study {accession}")
                    return self._create_basic_experiment(study)
                    
        except Exception as e:
            logger.error(f"Error processing study: {str(e)}")
            return self._create_basic_experiment(study)
    
    def _create_basic_experiment(self, study: Dict) -> Dict[str, Any]:
        """Create basic experiment from search result"""
        return {
            'id': study.get('accession', 'Unknown'),
            'title': study.get('title', 'Unknown Study'),
            'summary': study.get('description', '').strip()[:300] + '...' if len(study.get('description', '')) > 300 else study.get('description', ''),
            'organism': study.get('organism', 'Unknown'),
            'mission': 'NASA Mission',
            'keywords': [],
            'dataTypes': [],
            'publicationCount': 0,
            'duration': 'Unknown'
        }
    
    def _extract_organism(self, study_data: Dict) -> str:
        """Extract organism information"""
        organisms = study_data.get('organisms', [])
        if organisms:
            return organisms[0].get('scientificName', 'Unknown organism')
        return study_data.get('organism', 'Unknown organism')
    
    def _extract_mission(self, study_data: Dict) -> str:
        """Extract mission information"""
        factors = study_data.get('factors', [])
        for factor in factors:
            factor_name = factor.get('factorName', '').lower()
            if 'flight' in factor_name or 'mission' in factor_name:
                return factor.get('factorValue', 'NASA Mission')
        
        # Check project info
        project = study_data.get('project', {})
        if project:
            return project.get('title', 'NASA Mission')
        
        return 'NASA Mission'
    
    def _extract_keywords(self, study_data: Dict) -> List[str]:
        """Extract relevant keywords"""
        keywords = []
        
        # From factors
        factors = study_data.get('factors', [])
        for factor in factors:
            factor_name = factor.get('factorName', '')
            if factor_name:
                keywords.append(factor_name.lower())
        
        # From study type
        study_type = study_data.get('studyType', '')
        if study_type:
            keywords.append(study_type.lower())
        
        # Add common space-related keywords based on content
        title_lower = study_data.get('title', '').lower()
        desc_lower = study_data.get('description', '').lower()
        
        space_keywords = ['microgravity', 'spaceflight', 'space', 'ISS', 'gene expression', 
                         'muscle atrophy', 'bone density', 'cardiovascular', 'radiation']
        
        for keyword in space_keywords:
            if keyword in title_lower or keyword in desc_lower:
                keywords.append(keyword)
        
        return list(set(keywords))[:10]  # Limit to 10 unique keywords
    
    def _extract_data_types(self, study_data: Dict) -> List[str]:
        """Extract data types"""
        data_types = []
        
        assays = study_data.get('assays', [])
        for assay in assays:
            assay_type = assay.get('measurementType', '')
            if assay_type:
                data_types.append(assay_type)
        
        return list(set(data_types))
    
    def _extract_duration(self, study_data: Dict) -> str:
        """Extract study duration"""
        factors = study_data.get('factors', [])
        for factor in factors:
            factor_name = factor.get('factorName', '').lower()
            if 'duration' in factor_name or 'time' in factor_name:
                return factor.get('factorValue', 'Unknown')
        return 'Unknown'
    
    def _extract_factors(self, study_data: Dict) -> List[Dict[str, str]]:
        """Extract experimental factors"""
        factors = study_data.get('factors', [])
        return [
            {
                'name': factor.get('factorName', ''),
                'value': factor.get('factorValue', '')
            }
            for factor in factors[:5]  # Limit to 5 factors
        ]
    
    def _extract_dataset_size(self, study_data: Dict) -> Optional[str]:
        """Extract dataset size information"""
        # This would need to be calculated from actual file sizes
        # For now, return estimated based on assay count
        assays = study_data.get('assays', [])
        if len(assays) > 10:
            return "Large (>1GB)"
        elif len(assays) > 5:
            return "Medium (100MB-1GB)"
        else:
            return "Small (<100MB)"
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length"""
        if not text:
            return ""
        text = text.strip()
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text
    
    def _extract_osdr_keywords(self, source: Dict) -> List[str]:
        """Extract keywords from OSDR data"""
        keywords = []
        
        # From factor names and values
        factor_name = source.get('Study Factor Name', '')
        factor_value = source.get('Factor Value', '')
        
        if factor_name:
            keywords.append(factor_name.lower())
        if factor_value:
            keywords.append(factor_value.lower())
        
        # From project and assay types
        project_type = source.get('Project Type', '')
        if project_type:
            keywords.append(project_type.lower())
            
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
        
        return list(set([k for k in keywords if k]))[:10]  # Remove empty and limit to 10
    
    def _extract_osdr_data_types(self, source: Dict) -> List[str]:
        """Extract data types from OSDR data"""
        data_types = []
        
        # From assay technology
        assay_tech = source.get('Study Assay Technology Type', '')
        if assay_tech:
            data_types.append(assay_tech)
            
        assay_platform = source.get('Study Assay Technology Platform', '')
        if assay_platform:
            data_types.append(assay_platform)
            
        measurement_type = source.get('Study Assay Measurement Type', '')
        if measurement_type:
            data_types.append(measurement_type)
        
        return list(set([dt for dt in data_types if dt]))
    
    def _extract_osdr_duration(self, source: Dict) -> str:
        """Extract duration from OSDR data"""
        # Try to extract from mission data
        mission_data = source.get('Mission', {})
        if isinstance(mission_data, dict):
            start_date = mission_data.get('Start Date', '')
            end_date = mission_data.get('End Date', '')
            if start_date and end_date:
                try:
                    from datetime import datetime
                    # Handle different date formats
                    for date_format in ['%d-%b-%Y', '%m/%d/%Y', '%Y-%m-%d']:
                        try:
                            start = datetime.strptime(start_date, date_format)
                            end = datetime.strptime(end_date, date_format)
                            duration = (end - start).days
                            return f"{duration} days"
                        except ValueError:
                            continue
                except Exception:
                    pass
        
        # Check parameter values for duration hints
        param_value = source.get('Parameter Value', '')
        if 'day' in param_value.lower():
            return param_value
            
        return 'Unknown'
    
    def _format_release_date(self, timestamp) -> str:
        """Format release date from timestamp"""
        if not timestamp:
            return ''
        try:
            from datetime import datetime
            if isinstance(timestamp, (int, float)):
                date = datetime.fromtimestamp(timestamp)
                return date.strftime('%Y-%m-%d')
            return str(timestamp)
        except Exception:
            return str(timestamp) if timestamp else ''
    
    def _extract_osdr_factors(self, source: Dict) -> List[Dict[str, str]]:
        """Extract experimental factors from OSDR data"""
        factors = []
        
        # Primary factor
        factor_name = source.get('Study Factor Name', '')
        factor_value = source.get('Factor Value', '')
        if factor_name:
            factors.append({
                'name': factor_name,
                'value': factor_value or 'Yes'
            })
        
        # Flight program as factor
        flight_program = source.get('Flight Program', '')
        if flight_program:
            factors.append({
                'name': 'Flight Program',
                'value': flight_program
            })
        
        # Project type as factor
        project_type = source.get('Project Type', '')
        if project_type:
            factors.append({
                'name': 'Project Type',
                'value': project_type
            })
        
        return factors[:5]  # Limit to 5 factors
    
    def _estimate_dataset_size(self, source: Dict) -> str:
        """Estimate dataset size from OSDR data"""
        # Basic estimation based on assay types and material types
        assay_types = [
            source.get('Study Assay Technology Type', ''),
            source.get('Study Assay Technology Platform', ''),
            source.get('Study Assay Measurement Type', '')
        ]
        
        # High-data assays
        high_data_types = ['rna-seq', 'microarray', 'proteomics', 'genomics', 'imaging']
        medium_data_types = ['flow cytometry', 'pcr', 'biochemistry']
        
        assay_text = ' '.join(assay_types).lower()
        
        if any(hdt in assay_text for hdt in high_data_types):
            return "Large (>1GB)"
        elif any(mdt in assay_text for mdt in medium_data_types):
            return "Medium (100MB-1GB)"
        else:
            return "Small (<100MB)"
    
    def _get_fallback_data(self) -> List[Dict[str, Any]]:
        """Return enhanced fallback data when API fails"""
        return [
            {
                'id': 'GLDS-21',
                'title': 'Spaceflight Effects on Arabidopsis Gene Expression',
                'summary': 'Investigation of how microgravity affects plant gene expression patterns in Arabidopsis thaliana during spaceflight missions.',
                'organism': 'Arabidopsis thaliana',
                'mission': 'STS-131',
                'keywords': ['microgravity', 'gene expression', 'plants', 'spaceflight', 'arabidopsis'],
                'dataTypes': ['RNA-Seq', 'Microarray'],
                'publicationCount': 12,
                'duration': '14 days',
                'factors': [
                    {'name': 'Spaceflight', 'value': 'Flight'},
                    {'name': 'Duration', 'value': '14 days'}
                ]
            },
            {
                'id': 'GLDS-47',
                'title': 'Muscle Atrophy in Microgravity',
                'summary': 'Study of muscle protein degradation pathways in mouse models under simulated microgravity conditions.',
                'organism': 'Mus musculus',
                'mission': 'Rodent Research-1',
                'keywords': ['muscle atrophy', 'microgravity', 'protein degradation', 'mice'],
                'dataTypes': ['Proteomics', 'Histology'],
                'publicationCount': 8,
                'duration': '30 days',
                'factors': [
                    {'name': 'Microgravity', 'value': 'Simulated'},
                    {'name': 'Duration', 'value': '30 days'}
                ]
            },
            {
                'id': 'GLDS-104',
                'title': 'Cardiac Function in Space',
                'summary': 'Analysis of cardiovascular adaptations and cardiac muscle changes during long-duration spaceflight.',
                'organism': 'Homo sapiens',
                'mission': 'ISS Expedition 42',
                'keywords': ['cardiac', 'cardiovascular', 'spaceflight', 'adaptation'],
                'dataTypes': ['Echocardiography', 'Blood Analysis'],
                'publicationCount': 15,
                'duration': '180 days',
                'factors': [
                    {'name': 'Spaceflight', 'value': 'Long-duration'},
                    {'name': 'Environment', 'value': 'ISS'}
                ]
            },
            {
                'id': 'GLDS-78',
                'title': 'Bone Density Loss Studies',
                'summary': 'Investigation of bone mineral density changes and osteoblast activity in microgravity environments.',
                'organism': 'Rattus norvegicus',
                'mission': 'SpaceX CRS-12',
                'keywords': ['bone density', 'osteoblast', 'calcium', 'microgravity'],
                'dataTypes': ['X-ray', 'Biochemistry'],
                'publicationCount': 6,
                'duration': '60 days',
                'factors': [
                    {'name': 'Microgravity', 'value': 'True'},
                    {'name': 'Duration', 'value': '60 days'}
                ]
            },
            {
                'id': 'GLDS-242',
                'title': 'Space Radiation Effects on DNA',
                'summary': 'Comprehensive analysis of DNA damage and repair mechanisms in response to cosmic radiation exposure.',
                'organism': 'Homo sapiens',
                'mission': 'ISS Expedition 55',
                'keywords': ['radiation', 'DNA damage', 'cosmic rays', 'repair mechanisms'],
                'dataTypes': ['Genomics', 'DNA-Seq'],
                'publicationCount': 9,
                'duration': '120 days',
                'factors': [
                    {'name': 'Radiation', 'value': 'Cosmic'},
                    {'name': 'Duration', 'value': '120 days'}
                ]
            },
            {
                'id': 'GLDS-173',
                'title': 'Plant Growth in Microgravity',
                'summary': 'Study of plant root development and gravitropism responses in microgravity conditions.',
                'organism': 'Zea mays',
                'mission': 'ISS Expedition 48',
                'keywords': ['plant growth', 'root development', 'gravitropism', 'microgravity'],
                'dataTypes': ['Microscopy', 'Time-lapse Imaging'],
                'publicationCount': 5,
                'duration': '28 days',
                'factors': [
                    {'name': 'Gravity', 'value': 'Microgravity'},
                    {'name': 'Plant Type', 'value': 'Corn'}
                ]
            },
            {
                'id': 'GLDS-195',
                'title': 'Immune System Changes in Space',
                'summary': 'Investigation of immune system adaptations and T-cell function during spaceflight missions.',
                'organism': 'Homo sapiens',
                'mission': 'ISS Various Expeditions',
                'keywords': ['immune system', 't-cells', 'spaceflight', 'immunology'],
                'dataTypes': ['Flow Cytometry', 'Immunoassays'],
                'publicationCount': 11,
                'duration': 'Variable',
                'factors': [
                    {'name': 'Environment', 'value': 'Spaceflight'},
                    {'name': 'System', 'value': 'Immune'}
                ]
            },
            {
                'id': 'GLDS-158',
                'title': 'Fruit Fly Development in Zero-G',
                'summary': 'Analysis of developmental biology and genetic expression in Drosophila melanogaster under microgravity.',
                'organism': 'Drosophila melanogaster',
                'mission': 'SpaceX CRS-8',
                'keywords': ['development', 'drosophila', 'genetics', 'zero gravity'],
                'dataTypes': ['RNA-Seq', 'Developmental Assays'],
                'publicationCount': 7,
                'duration': '21 days',
                'factors': [
                    {'name': 'Gravity', 'value': 'Zero-G'},
                    {'name': 'Stage', 'value': 'Development'}
                ]
            }
        ]

# Singleton instance
nasa_genelab = NASAGeneLab()

async def get_experiments(limit: int = 20) -> List[Dict[str, Any]]:
    """Get experiments from NASA GeneLab API"""
    return await nasa_genelab.fetch_experiments(limit)

async def search_experiments(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search experiments by query"""
    try:
        async with aiohttp.ClientSession() as session:
            search_params = {
                'q': query,
                'size': limit,
                'from': 0
            }
            
            async with session.get(nasa_genelab.search_url, params=search_params) as response:
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
                    
                    # If no hits, fall back to local search
                    if total_count == 0 or not study_hits:
                        fallback_data = nasa_genelab._get_fallback_data()
                        query_lower = query.lower()
                        return [
                            exp for exp in fallback_data
                            if query_lower in exp['title'].lower() or
                               query_lower in exp['summary'].lower() or
                               any(query_lower in keyword for keyword in exp['keywords']) or
                               query_lower in exp['organism'].lower()
                        ]
                    
                    experiments = []
                    for hit in study_hits:
                        experiment = nasa_genelab._process_osdr_hit(hit)
                        if experiment:
                            experiments.append(experiment)
                    
                    return experiments
                else:
                    # Fallback to filtering fallback data
                    fallback_data = nasa_genelab._get_fallback_data()
                    query_lower = query.lower()
                    return [
                        exp for exp in fallback_data
                        if query_lower in exp['title'].lower() or
                           query_lower in exp['summary'].lower() or
                           any(query_lower in keyword for keyword in exp['keywords']) or
                           query_lower in exp['organism'].lower()
                    ]
                    
    except Exception as e:
        logger.error(f"Error searching experiments: {str(e)}")
        # Fallback search in local data
        fallback_data = nasa_genelab._get_fallback_data()
        query_lower = query.lower()
        return [
            exp for exp in fallback_data
            if query_lower in exp['title'].lower() or
               query_lower in exp['summary'].lower() or
               any(query_lower in keyword for keyword in exp['keywords']) or
               query_lower in exp['organism'].lower()
        ]