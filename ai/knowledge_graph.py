"""
Knowledge graph generation for experiment relationships
"""
import asyncio
from typing import Dict, List, Set, Tuple
import json
from collections import defaultdict
import numpy as np

class KnowledgeGraphGenerator:
    def __init__(self):
        self.relationship_types = {
            'organism': 'studied_in',
            'mission': 'conducted_during',
            'factor': 'affected_by',
            'outcome': 'results_in',
            'keyword': 'related_to'
        }
    
    async def generate_graph(self, experiment_ids: List[str]) -> Dict:
        """Generate knowledge graph data for given experiments"""
        try:
            # For MVP, create mock graph data
            # In production, this would analyze actual experiment data
            
            nodes = []
            edges = []
            node_ids = set()
            
            # Mock experiments data for demo
            mock_experiments = self._get_mock_experiments(experiment_ids)
            
            # Generate nodes and relationships
            for exp in mock_experiments:
                exp_node_id = f"exp_{exp['id']}"
                
                # Add experiment node
                if exp_node_id not in node_ids:
                    nodes.append({
                        'data': {
                            'id': exp_node_id,
                            'label': exp['title'][:30] + "...",
                            'type': 'experiment',
                            'size': 25,
                            'color': '#0B3D91'
                        }
                    })
                    node_ids.add(exp_node_id)
                
                # Add organism nodes
                if exp.get('organism'):
                    org_id = f"org_{exp['organism'].replace(' ', '_').lower()}"
                    if org_id not in node_ids:
                        nodes.append({
                            'data': {
                                'id': org_id,
                                'label': exp['organism'],
                                'type': 'organism',
                                'size': 20,
                                'color': '#EF4444'
                            }
                        })
                        node_ids.add(org_id)
                    
                    edges.append({
                        'data': {
                            'id': f"{exp_node_id}_{org_id}",
                            'source': exp_node_id,
                            'target': org_id,
                            'label': 'studies',
                            'type': 'studies'
                        }
                    })
                
                # Add mission nodes
                if exp.get('mission'):
                    mission_id = f"mission_{exp['mission'].replace(' ', '_').replace('-', '_').lower()}"
                    if mission_id not in node_ids:
                        nodes.append({
                            'data': {
                                'id': mission_id,
                                'label': exp['mission'],
                                'type': 'mission',
                                'size': 18,
                                'color': '#6366F1'
                            }
                        })
                        node_ids.add(mission_id)
                    
                    edges.append({
                        'data': {
                            'id': f"{exp_node_id}_{mission_id}",
                            'source': exp_node_id,
                            'target': mission_id,
                            'label': 'conducted_in',
                            'type': 'conducted_in'
                        }
                    })
                
                # Add keyword/factor nodes
                for keyword in exp.get('keywords', [])[:3]:  # Limit to top 3
                    keyword_id = f"kw_{keyword.replace(' ', '_').lower()}"
                    if keyword_id not in node_ids:
                        nodes.append({
                            'data': {
                                'id': keyword_id,
                                'label': keyword,
                                'type': 'keyword',
                                'size': 15,
                                'color': '#10B981'
                            }
                        })
                        node_ids.add(keyword_id)
                    
                    edges.append({
                        'data': {
                            'id': f"{exp_node_id}_{keyword_id}",
                            'source': exp_node_id,
                            'target': keyword_id,
                            'label': 'involves',
                            'type': 'involves'
                        }
                    })
            
            # Add cross-experiment relationships
            self._add_cross_relationships(nodes, edges, node_ids)
            
            return {
                'nodes': nodes,
                'edges': edges,
                'layout': {
                    'name': 'cose',
                    'animate': True,
                    'animationDuration': 1000
                },
                'style': self._get_graph_style()
            }
            
        except Exception as e:
            print(f"Error generating knowledge graph: {e}")
            return self._get_fallback_graph()
    
    def _get_mock_experiments(self, experiment_ids: List[str]) -> List[Dict]:
        """Get mock experiment data for demo"""
        mock_data = [
            {
                'id': 'GLDS-21',
                'title': 'Spaceflight Effects on Arabidopsis Gene Expression',
                'organism': 'Arabidopsis thaliana',
                'mission': 'STS-131',
                'keywords': ['microgravity', 'gene expression', 'plants', 'spaceflight']
            },
            {
                'id': 'GLDS-47',
                'title': 'Muscle Atrophy in Microgravity',
                'organism': 'Mus musculus',
                'mission': 'Rodent Research-1',
                'keywords': ['muscle atrophy', 'microgravity', 'protein degradation']
            },
            {
                'id': 'GLDS-173',
                'title': 'Microbial Communities in Space',
                'organism': 'Escherichia coli',
                'mission': 'ISS Expedition-45',
                'keywords': ['microbiome', 'bacteria', 'space adaptation']
            },
            {
                'id': 'GLDS-242',
                'title': 'Bone Density Changes in Astronauts',
                'organism': 'Homo sapiens',
                'mission': 'ISS Long Duration',
                'keywords': ['bone density', 'calcium', 'osteoporosis']
            }
        ]
        
        # Filter by requested IDs or return all for demo
        if experiment_ids and experiment_ids != ['']:
            return [exp for exp in mock_data if exp['id'] in experiment_ids]
        
        return mock_data
    
    def _add_cross_relationships(self, nodes: List[Dict], edges: List[Dict], node_ids: Set[str]):
        """Add relationships between similar entities"""
        # Find organisms that share keywords
        organism_keywords = defaultdict(set)
        keyword_organisms = defaultdict(set)
        
        for node in nodes:
            if node['data']['type'] == 'organism':
                org_id = node['data']['id']
                # Find related keywords through edges
                for edge in edges:
                    if edge['data']['source'].startswith('exp_') and edge['data']['target'].startswith('kw_'):
                        # Find experiments with this organism
                        for exp_edge in edges:
                            if exp_edge['data']['target'] == org_id and exp_edge['data']['source'] == edge['data']['source']:
                                keyword_id = edge['data']['target']
                                organism_keywords[org_id].add(keyword_id)
                                keyword_organisms[keyword_id].add(org_id)
        
        # Add similarity edges between organisms with shared keywords
        organisms = list(organism_keywords.keys())
        for i, org1 in enumerate(organisms):
            for org2 in organisms[i+1:]:
                shared_keywords = organism_keywords[org1] & organism_keywords[org2]
                if len(shared_keywords) >= 1:  # At least 1 shared keyword
                    edges.append({
                        'data': {
                            'id': f"similar_{org1}_{org2}",
                            'source': org1,
                            'target': org2,
                            'label': 'similar_to',
                            'type': 'similarity',
                            'style': 'dashed'
                        }
                    })
    
    def _get_graph_style(self) -> List[Dict]:
        """Define Cytoscape styling for the graph"""
        return [
            {
                'selector': 'node',
                'style': {
                    'background-color': 'data(color)',
                    'label': 'data(label)',
                    'width': 'data(size)',
                    'height': 'data(size)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'color': '#ffffff',
                    'font-size': '10px',
                    'font-family': 'Inter, sans-serif'
                }
            },
            {
                'selector': 'node[type="experiment"]',
                'style': {
                    'shape': 'rectangle',
                    'border-width': 2,
                    'border-color': '#ffffff'
                }
            },
            {
                'selector': 'node[type="organism"]',
                'style': {
                    'shape': 'ellipse'
                }
            },
            {
                'selector': 'node[type="mission"]',
                'style': {
                    'shape': 'diamond'
                }
            },
            {
                'selector': 'node[type="keyword"]',
                'style': {
                    'shape': 'triangle'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'width': 2,
                    'line-color': '#6366F1',
                    'target-arrow-color': '#6366F1',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'opacity': 0.7
                }
            },
            {
                'selector': 'edge[type="similarity"]',
                'style': {
                    'line-style': 'dashed',
                    'line-color': '#10B981',
                    'target-arrow-color': '#10B981'
                }
            }
        ]
    
    def _get_fallback_graph(self) -> Dict:
        """Fallback graph when generation fails"""
        return {
            'nodes': [
                {
                    'data': {
                        'id': 'microgravity',
                        'label': 'Microgravity',
                        'type': 'condition',
                        'size': 20,
                        'color': '#6366F1'
                    }
                },
                {
                    'data': {
                        'id': 'gene_expression',
                        'label': 'Gene Expression',
                        'type': 'process',
                        'size': 18,
                        'color': '#10B981'
                    }
                },
                {
                    'data': {
                        'id': 'arabidopsis',
                        'label': 'Arabidopsis',
                        'type': 'organism',
                        'size': 16,
                        'color': '#EF4444'
                    }
                }
            ],
            'edges': [
                {
                    'data': {
                        'id': 'edge1',
                        'source': 'microgravity',
                        'target': 'gene_expression',
                        'label': 'affects'
                    }
                },
                {
                    'data': {
                        'id': 'edge2',
                        'source': 'gene_expression',
                        'target': 'arabidopsis',
                        'label': 'observed_in'
                    }
                }
            ],
            'layout': {'name': 'circle'},
            'style': self._get_graph_style()
        }