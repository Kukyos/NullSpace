import React, { useEffect } from 'react';

const ExperimentModal = ({ experiment, onClose, isOpen, onToast }) => {
  // Handle escape key press
  useEffect(() => {
    const handleEscapeKey = (event) => {
      if (event.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscapeKey);
      // Prevent body scroll when modal is open
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscapeKey);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen || !experiment) return null;

  return (
    <div 
      className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={(e) => {
        // Close modal when clicking backdrop
        if (e.target === e.currentTarget) {
          onClose();
        }
      }}
    >
      <div className="glass-morphism max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-black/20 backdrop-blur-lg p-6 border-b border-white/10">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-2xl font-bold text-star-white mb-2">
                {experiment.title}
              </h2>
              <div className="flex items-center space-x-4">
                <span className="bg-nasa-blue/20 text-nasa-blue px-3 py-1 rounded font-mono text-sm">
                  {experiment.id}
                </span>
                <span className="text-cosmic-purple font-medium">
                  {experiment.mission}
                </span>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors p-2"
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {/* Organism & Mission Info */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-morphism p-4">
              <h3 className="text-lg font-semibold text-star-white mb-3 flex items-center">
                <span className="w-3 h-3 bg-green-400 rounded-full mr-2"></span>
                Organism
              </h3>
              <p className="text-green-400 font-medium italic text-lg">
                {experiment.organism}
              </p>
            </div>
            
            <div className="glass-morphism p-4">
              <h3 className="text-lg font-semibold text-star-white mb-3 flex items-center">
                <span className="w-3 h-3 bg-cosmic-purple rounded-full mr-2"></span>
                Mission Details
              </h3>
              <div className="space-y-2">
                <p className="text-gray-300">
                  <span className="text-cosmic-purple">Mission:</span> {experiment.mission}
                </p>
                {experiment.duration_days && (
                  <p className="text-gray-300">
                    <span className="text-cosmic-purple">Duration:</span> {experiment.duration_days} days
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* AI Summary */}
          <div className="glass-morphism p-6">
            <h3 className="text-lg font-semibold text-star-white mb-4 flex items-center">
              <span className="w-3 h-3 bg-yellow-400 rounded-full mr-2"></span>
              AI-Generated Summary
            </h3>
            <p className="text-gray-300 leading-relaxed">
              {experiment.summary || experiment.description}
            </p>
          </div>

          {/* Detailed Description */}
          {experiment.description && experiment.description !== experiment.summary && (
            <div className="glass-morphism p-6">
              <h3 className="text-lg font-semibold text-star-white mb-4 flex items-center">
                <span className="w-3 h-3 bg-blue-400 rounded-full mr-2"></span>
                Full Description
              </h3>
              <p className="text-gray-300 leading-relaxed">
                {experiment.description}
              </p>
            </div>
          )}

          {/* Research Factors */}
          {experiment.factors && (
            <div className="glass-morphism p-6">
              <h3 className="text-lg font-semibold text-star-white mb-4 flex items-center">
                <span className="w-3 h-3 bg-orange-400 rounded-full mr-2"></span>
                Research Factors
              </h3>
              <div className="flex flex-wrap gap-2">
                {experiment.factors.map((factor, index) => (
                  <span 
                    key={index}
                    className="bg-orange-400/20 text-orange-400 px-3 py-1 rounded-md font-medium"
                  >
                    {factor}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Data Types */}
          {experiment.data_types && (
            <div className="glass-morphism p-6">
              <h3 className="text-lg font-semibold text-star-white mb-4 flex items-center">
                <span className="w-3 h-3 bg-purple-400 rounded-full mr-2"></span>
                Data Types Collected
              </h3>
              <div className="flex flex-wrap gap-2">
                {experiment.data_types.map((type, index) => (
                  <span 
                    key={index}
                    className="bg-purple-400/20 text-purple-400 px-3 py-1 rounded-md font-medium"
                  >
                    {type}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Keywords */}
          <div className="glass-morphism p-6">
            <h3 className="text-lg font-semibold text-star-white mb-4 flex items-center">
              <span className="w-3 h-3 bg-cyan-400 rounded-full mr-2"></span>
              Research Keywords
            </h3>
            <div className="flex flex-wrap gap-2">
              {experiment.keywords?.map((keyword, index) => (
                <span 
                  key={index}
                  className="bg-white/10 text-gray-300 px-3 py-1 rounded-md text-sm font-mono hover:bg-white/20 transition-colors cursor-pointer"
                >
                  #{keyword}
                </span>
              ))}
            </div>
          </div>

          {/* Stats */}
          {(experiment.publication_count || experiment.dataset_size_gb) && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {experiment.publication_count && (
                <div className="glass-morphism p-4 text-center">
                  <div className="text-2xl font-bold text-cosmic-purple mb-1">
                    {experiment.publication_count}
                  </div>
                  <div className="text-gray-400 text-sm font-mono">Publications</div>
                </div>
              )}
              {experiment.dataset_size_gb && (
                <div className="glass-morphism p-4 text-center">
                  <div className="text-2xl font-bold text-green-400 mb-1">
                    {experiment.dataset_size_gb}GB
                  </div>
                  <div className="text-gray-400 text-sm font-mono">Dataset Size</div>
                </div>
              )}
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row justify-center gap-4 pt-4">
            <button 
              onClick={() => {
                // Open NASA GeneLab page for this experiment
                const geneLabUrl = `https://genelab-data.ndc.nasa.gov/genelab/accession/${experiment.id}/`;
                window.open(geneLabUrl, '_blank', 'noopener,noreferrer');
                
                // Show success toast
                if (onToast) {
                  onToast(`Opening ${experiment.id} on NASA GeneLab`, 'success');
                }
              }}
              className="bg-nasa-blue hover:bg-nasa-blue/80 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 hover:scale-105 flex items-center justify-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
              View on NASA GeneLab
            </button>
            <button 
              onClick={() => {
                // Find related experiments based on keywords or organism
                const keywords = experiment.keywords || [];
                const organism = experiment.organism || '';
                
                // Create search query for related experiments
                const searchQuery = keywords.length > 0 
                  ? keywords[0] 
                  : organism.split(' ')[0]; // Use first part of organism name
                
                // Close current modal and trigger search
                onClose();
                
                // Use a timeout to allow modal to close, then trigger search
                setTimeout(() => {
                  // Dispatch a custom event to trigger search in parent component
                  const searchEvent = new CustomEvent('searchRelatedExperiments', {
                    detail: { query: searchQuery, excludeId: experiment.id }
                  });
                  window.dispatchEvent(searchEvent);
                }, 100);
              }}
              className="bg-cosmic-purple hover:bg-cosmic-purple/80 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200 hover:scale-105 flex items-center justify-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
              Related Experiments
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExperimentModal;