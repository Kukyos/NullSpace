import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import SearchBar from './components/SearchBar';
import ExperimentCard from './components/ExperimentCard';
import KnowledgeGraph from './components/KnowledgeGraph';
import Header from './components/Header';
import ExperimentModal from './components/ExperimentModal';
import LoadingSpinner from './components/LoadingSpinner';
import Toast from './components/Toast';

function App() {
  const [allExperiments, setAllExperiments] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedExperiment, setSelectedExperiment] = useState(null);
  const [graphData, setGraphData] = useState(null);
  const [modalExperiment, setModalExperiment] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid');
  const [sortBy, setSortBy] = useState('relevance');
  const [filterBy, setFilterBy] = useState('all');
  const [isSearching, setIsSearching] = useState(false);
  const searchTimeoutRef = useRef(null);
  const [toasts, setToasts] = useState([]);
  const [dataSource, setDataSource] = useState('');
  const [isRealData, setIsRealData] = useState(true);

  // Define performSearch before it's used in useEffect
  const performSearch = useCallback(async (term) => {
    if (term.trim() === '') {
      setIsSearching(false);
      return;
    }
    
    try {
      const response = await fetch(`/api/search?query=${encodeURIComponent(term)}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      
      // Show data source notification for search results
      if (data.isRealData === false) {
        addToast(`Search results from ${data.dataSource}`, 'warning');
      }
      
      // Don't replace allExperiments, we'll filter in the memoized function
    } catch (error) {
      console.error('Error searching experiments:', error);
      addToast('Search failed - using local data', 'error');
    } finally {
      setIsSearching(false);
    }
  }, [addToast]);

  useEffect(() => {
    // Load initial data
    loadExperiments();
    loadGraphData();

    // Add event listener for related experiments search
    const handleRelatedExperimentsSearch = (event) => {
      const { query } = event.detail;
      setSearchTerm(query);
      addToast(`Searching for experiments related to: ${query}`, 'info');
    };

    window.addEventListener('searchRelatedExperiments', handleRelatedExperimentsSearch);

    return () => {
      window.removeEventListener('searchRelatedExperiments', handleRelatedExperimentsSearch);
    };
  }, [loadExperiments, loadGraphData, addToast]);

  // Debounced search effect
  useEffect(() => {
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }
    
    if (searchTerm.trim() === '') {
      setIsSearching(false);
      return;
    }

    setIsSearching(true);
    searchTimeoutRef.current = setTimeout(() => {
      performSearch(searchTerm);
    }, 300); // 300ms debounce

    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, [searchTerm, performSearch]);

  const loadExperiments = useCallback(async () => {
    try {
      setLoading(true);
      // Fetch experiments from our FastAPI backend
      const response = await fetch('/api/experiments');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setAllExperiments(data.experiments || []);
      setDataSource(data.dataSource || 'Unknown');
      setIsRealData(data.isRealData !== false);
      
      // Show toast message based on data source
      if (data.isRealData === false) {
        addToast(`⚠️ Using ${data.dataSource} - NASA API temporarily unavailable`, 'warning');
      } else if (data.dataSource === 'NASA OSDR') {
        addToast('✅ Connected to live NASA OSDR database', 'success');
      }
    } catch (error) {
      console.error('Error loading experiments:', error);
      setDataSource('Mock Data (Network Error)');
      setIsRealData(false);
      addToast('⚠️ Using Mock Data - Unable to connect to NASA API', 'error');
      // Fallback to mock data if API fails
      const mockExperiments = [
        {
          id: 'GLDS-21',
          title: 'Spaceflight Effects on Arabidopsis Gene Expression',
          summary: 'Investigation of how microgravity affects plant gene expression patterns in Arabidopsis thaliana.',
          organism: 'Arabidopsis thaliana',
          mission: 'STS-131',
          keywords: ['microgravity', 'gene expression', 'plants', 'spaceflight'],
          dataTypes: ['RNA-Seq', 'Microarray'],
          publicationCount: 12,
          duration: '14 days'
        },
        {
          id: 'GLDS-47',
          title: 'Muscle Atrophy in Microgravity',
          summary: 'Study of muscle protein degradation pathways in mouse models under simulated microgravity conditions.',
          organism: 'Mus musculus',
          mission: 'Rodent Research-1',
          keywords: ['muscle atrophy', 'microgravity', 'protein degradation', 'mice'],
          dataTypes: ['Proteomics', 'Histology'],
          publicationCount: 8,
          duration: '30 days'
        },
        {
          id: 'GLDS-104',
          title: 'Cardiac Function in Space',
          summary: 'Analysis of cardiovascular adaptations and cardiac muscle changes during long-duration spaceflight.',
          organism: 'Homo sapiens',
          mission: 'ISS Expedition 42',
          keywords: ['cardiac', 'cardiovascular', 'spaceflight', 'adaptation'],
          dataTypes: ['Echocardiography', 'Blood Analysis'],
          publicationCount: 15,
          duration: '180 days'
        },
        {
          id: 'GLDS-78',
          title: 'Bone Density Loss Studies',
          summary: 'Investigation of bone mineral density changes and osteoblast activity in microgravity environments.',
          organism: 'Rattus norvegicus',
          mission: 'SpaceX CRS-12',
          keywords: ['bone density', 'osteoblast', 'calcium', 'microgravity'],
          dataTypes: ['X-ray', 'Biochemistry'],
          publicationCount: 6,
          duration: '60 days'
        }
      ];
      setAllExperiments(mockExperiments);
    } finally {
      setLoading(false);
    }
  }, [addToast]);

  const loadGraphData = useCallback(async () => {
    try {
      // Fetch knowledge graph data from backend
      const response = await fetch('/api/knowledge-graph');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setGraphData(data);
    } catch (error) {
      console.error('Error loading graph data:', error);
      // Fallback to mock graph data
      const mockGraphData = {
        nodes: [
          { data: { id: 'microgravity', label: 'Microgravity', type: 'condition' } },
          { data: { id: 'gene-expression', label: 'Gene Expression', type: 'process' } },
          { data: { id: 'muscle-atrophy', label: 'Muscle Atrophy', type: 'outcome' } },
          { data: { id: 'arabidopsis', label: 'Arabidopsis', type: 'organism' } },
          { data: { id: 'mouse', label: 'Mouse', type: 'organism' } }
        ],
        edges: [
          { data: { source: 'microgravity', target: 'gene-expression', label: 'affects' } },
          { data: { source: 'microgravity', target: 'muscle-atrophy', label: 'causes' } },
          { data: { source: 'gene-expression', target: 'arabidopsis', label: 'studied in' } },
          { data: { source: 'muscle-atrophy', target: 'mouse', label: 'observed in' } }
        ]
      };
      setGraphData(mockGraphData);
    }
  }, []);

  const handleSearchChange = useCallback((term) => {
    setSearchTerm(term);
  }, []);

  const handleViewDetails = (experiment) => {
    setModalExperiment(experiment);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setModalExperiment(null);
  };

  // Toast management
  const addToast = useCallback((message, type = 'info') => {
    const id = Date.now() + Math.random();
    const newToast = { id, message, type };
    setToasts(prev => [...prev, newToast]);
  }, []);

  const removeToast = (id) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  };

  // Memoized filtering and sorting
  const filteredAndSortedExperiments = useMemo(() => {
    let filtered = allExperiments;

    // Apply search filter
    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(exp =>
        exp.title.toLowerCase().includes(term) ||
        exp.organism.toLowerCase().includes(term) ||
        exp.summary.toLowerCase().includes(term) ||
        exp.mission.toLowerCase().includes(term) ||
        exp.keywords.some(keyword => keyword.toLowerCase().includes(term))
      );
    }

    // Apply category filter
    if (filterBy !== 'all') {
      filtered = filtered.filter(exp => {
        switch (filterBy) {
          case 'plants':
            return exp.organism.toLowerCase().includes('arabidopsis') || 
                   exp.keywords.some(k => k.toLowerCase().includes('plant'));
          case 'animals':
            return exp.organism.toLowerCase().includes('mus') ||
                   exp.organism.toLowerCase().includes('rattus') ||
                   exp.organism.toLowerCase().includes('homo sapiens');
          case 'microgravity':
            return exp.keywords.some(k => k.toLowerCase().includes('microgravity'));
          case 'gene-expression':
            return exp.keywords.some(k => k.toLowerCase().includes('gene'));
          default:
            return true;
        }
      });
    }

    // Apply sorting
    const sorted = [...filtered].sort((a, b) => {
      switch (sortBy) {
        case 'title':
          return a.title.localeCompare(b.title);
        case 'organism':
          return a.organism.localeCompare(b.organism);
        case 'mission':
          return a.mission.localeCompare(b.mission);
        case 'publications':
          return (b.publicationCount || 0) - (a.publicationCount || 0);
        case 'relevance':
        default:
          return 0; // Keep original order for relevance
      }
    });

    return sorted;
  }, [allExperiments, searchTerm, filterBy, sortBy]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-space-dark via-slate-900 to-nasa-blue">
      <Header />
      
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Search and Controls Section */}
        <div className="mb-8 space-y-4">
          <SearchBar 
            searchTerm={searchTerm}
            onSearchChange={handleSearchChange}
            isSearching={isSearching}
          />
          
          {/* Data Source Indicator */}
          {dataSource && (
            <div className={`inline-flex items-center gap-2 px-3 py-2 rounded-full text-sm font-medium backdrop-blur-sm border ${
              isRealData 
                ? 'bg-green-500/10 border-green-500/30 text-green-400' 
                : 'bg-amber-500/10 border-amber-500/30 text-amber-400'
            }`}>
              <div className={`w-2 h-2 rounded-full ${
                isRealData ? 'bg-green-400' : 'bg-amber-400'
              } animate-pulse`}></div>
              <span>Data Source: {dataSource}</span>
              {!isRealData && (
                <span className="text-xs opacity-75">(Fallback Mode)</span>
              )}
            </div>
          )}
          
          {/* View Controls */}
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
            <div className="flex flex-wrap gap-3">
              {/* View Mode Toggle */}
              <div className="flex bg-slate-800/50 backdrop-blur-sm rounded-lg p-1">
                {['grid', 'list', 'graph'].map((mode) => (
                  <button
                    key={mode}
                    onClick={() => setViewMode(mode)}
                    className={`px-3 py-1.5 rounded-md text-sm font-medium transition-all duration-200 ${
                      viewMode === mode
                        ? 'bg-nasa-blue text-white shadow-lg'
                        : 'text-star-white/70 hover:text-star-white hover:bg-slate-700/50'
                    }`}
                  >
                    {mode.charAt(0).toUpperCase() + mode.slice(1)}
                  </button>
                ))}
              </div>

              {/* Filter Dropdown */}
              <select
                value={filterBy}
                onChange={(e) => setFilterBy(e.target.value)}
                className="bg-slate-800/50 backdrop-blur-sm border border-slate-600 rounded-lg px-3 py-1.5 text-star-white text-sm focus:outline-none focus:ring-2 focus:ring-nasa-blue"
              >
                <option value="all">All Categories</option>
                <option value="plants">Plant Studies</option>
                <option value="animals">Animal Studies</option>
                <option value="microgravity">Microgravity</option>
                <option value="gene-expression">Gene Expression</option>
              </select>

              {/* Sort Dropdown */}
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="bg-slate-800/50 backdrop-blur-sm border border-slate-600 rounded-lg px-3 py-1.5 text-star-white text-sm focus:outline-none focus:ring-2 focus:ring-nasa-blue"
              >
                <option value="relevance">Sort by Relevance</option>
                <option value="title">Sort by Title</option>
                <option value="organism">Sort by Organism</option>
                <option value="mission">Sort by Mission</option>
                <option value="publications">Sort by Publications</option>
              </select>
            </div>

            {/* Results Count */}
            <div className="text-star-white/70 text-sm">
              {isSearching ? (
                <div className="flex items-center gap-2">
                  <LoadingSpinner size="small" />
                  Searching...
                </div>
              ) : (
                `${filteredAndSortedExperiments.length} experiment${filteredAndSortedExperiments.length !== 1 ? 's' : ''} found`
              )}
            </div>
          </div>
        </div>

        {/* Main Content */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <LoadingSpinner size="large" />
              <p className="mt-4 text-star-white/70">Loading NASA bioscience data...</p>
            </div>
          </div>
        ) : viewMode === 'graph' ? (
          /* Full Screen Graph View */
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-star-white">
              Knowledge Graph
            </h2>
            <div className="h-screen max-h-[80vh]">
              <KnowledgeGraph 
                data={graphData}
                selectedExperiment={selectedExperiment}
                experiments={filteredAndSortedExperiments}
                onExperimentSelect={setSelectedExperiment}
              />
            </div>
          </div>
        ) : (
          /* Split Layout for Grid/List + Graph */
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            {/* Experiments Section */}
            <div className={`xl:col-span-2 space-y-4 ${viewMode === 'list' ? 'space-y-2' : ''}`}>
              <h2 className="text-2xl font-bold text-star-white flex items-center gap-3">
                NASA Bioscience Experiments
                {searchTerm && (
                  <span className="text-lg font-normal text-star-white/70">
                    for "{searchTerm}"
                  </span>
                )}
              </h2>
              
              {filteredAndSortedExperiments.length === 0 ? (
                <div className="text-center py-20">
                  <div className="text-6xl mb-4">🔍</div>
                  <h3 className="text-xl font-semibold text-star-white mb-2">No experiments found</h3>
                  <p className="text-star-white/70">Try adjusting your search terms or filters</p>
                </div>
              ) : (
                <div className={
                  viewMode === 'grid' 
                    ? 'grid grid-cols-1 lg:grid-cols-2 gap-4'
                    : 'space-y-3'
                }>
                  {filteredAndSortedExperiments.map((experiment, index) => (
                    <div
                      key={experiment.id}
                      className="animate-fadeInUp"
                      style={{ animationDelay: `${index * 100}ms` }}
                    >
                      <ExperimentCard
                        experiment={experiment}
                        onSelect={setSelectedExperiment}
                        isSelected={selectedExperiment?.id === experiment.id}
                        onViewDetails={handleViewDetails}
                        viewMode={viewMode}
                      />
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Knowledge Graph Sidebar */}
            <div className="xl:sticky xl:top-6 xl:self-start">
              <h2 className="text-xl font-bold text-star-white mb-4">
                Knowledge Graph
              </h2>
              <div className="h-96 xl:h-[70vh]">
                <KnowledgeGraph 
                  data={graphData}
                  selectedExperiment={selectedExperiment}
                  experiments={filteredAndSortedExperiments}
                  onExperimentSelect={setSelectedExperiment}
                />
              </div>
            </div>
          </div>
        )}
      </main>

      <ExperimentModal
        experiment={modalExperiment}
        isOpen={isModalOpen}
        onClose={closeModal}
        onToast={addToast}
      />

      {/* Toast Notifications */}
      {toasts.map((toast) => (
        <Toast
          key={toast.id}
          message={toast.message}
          type={toast.type}
          onClose={() => removeToast(toast.id)}
        />
      ))}
    </div>
  );
}

export default App;