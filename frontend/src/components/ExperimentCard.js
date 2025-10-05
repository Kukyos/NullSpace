import React from 'react';

const ExperimentCard = ({ experiment, onSelect, isSelected, onViewDetails, viewMode = 'grid' }) => {
  const getOrganismIcon = (organism) => {
    if (organism.toLowerCase().includes('arabidopsis')) return '🌱';
    if (organism.toLowerCase().includes('mus') || organism.toLowerCase().includes('rattus')) return '🐭';
    if (organism.toLowerCase().includes('homo sapiens')) return '👨‍🚀';
    return '🧬';
  };

  const getMissionTypeColor = (mission) => {
    if (mission.includes('ISS')) return 'text-blue-400 bg-blue-400/20';
    if (mission.includes('STS')) return 'text-purple-400 bg-purple-400/20';
    if (mission.includes('SpaceX')) return 'text-green-400 bg-green-400/20';
    return 'text-cosmic-purple bg-cosmic-purple/20';
  };

  if (viewMode === 'list') {
    return (
      <div 
        className={`glass-morphism p-4 cursor-pointer transition-all duration-300 hover:scale-[1.02] flex items-center space-x-6 ${
          isSelected ? 'cyber-glow ring-2 ring-cosmic-purple' : 'hover:bg-white/10'
        }`}
        onClick={() => onSelect(experiment)}
      >
        <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-nasa-blue to-cosmic-purple rounded-full flex items-center justify-center text-2xl">
          {getOrganismIcon(experiment.organism)}
        </div>
        
        <div className="flex-grow min-w-0">
          <div className="flex items-center gap-3 mb-1">
            <h3 className="text-lg font-semibold text-star-white truncate">
              {experiment.title}
            </h3>
            <span className="bg-nasa-blue/20 text-nasa-blue px-2 py-1 rounded text-xs font-mono flex-shrink-0">
              {experiment.id}
            </span>
          </div>
          <p className="text-gray-300 text-sm line-clamp-2 mb-2">
            {experiment.summary}
          </p>
          <div className="flex items-center gap-4 text-xs">
            <span className="text-green-400 flex items-center gap-1">
              <span>{getOrganismIcon(experiment.organism)}</span>
              {experiment.organism}
            </span>
            <span className={`px-2 py-1 rounded ${getMissionTypeColor(experiment.mission)}`}>
              {experiment.mission}
            </span>
            {experiment.publicationCount && (
              <span className="text-star-white/70">
                📄 {experiment.publicationCount} publications
              </span>
            )}
          </div>
        </div>

        <div className="flex-shrink-0 flex items-center gap-3">
          {isSelected && (
            <div className="w-3 h-3 bg-cosmic-purple rounded-full animate-pulse"></div>
          )}
          <button 
            onClick={(e) => {
              e.stopPropagation();
              if (onViewDetails) onViewDetails(experiment);
            }}
            className="bg-cosmic-purple/20 hover:bg-cosmic-purple/40 text-cosmic-purple hover:text-white px-4 py-2 rounded-lg transition-all duration-200 text-sm font-medium"
          >
            Details →
          </button>
        </div>
      </div>
    );
  }

  // Grid view (default)
  return (
    <div 
      className={`glass-morphism p-6 cursor-pointer transition-all duration-300 hover:scale-105 hover:shadow-2xl group ${
        isSelected ? 'cyber-glow ring-2 ring-cosmic-purple' : 'hover:bg-white/10'
      }`}
      onClick={() => onSelect(experiment)}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex-grow">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-gradient-to-br from-nasa-blue to-cosmic-purple rounded-full flex items-center justify-center text-xl">
              {getOrganismIcon(experiment.organism)}
            </div>
            <div>
              <h3 className="text-xl font-semibold text-star-white group-hover:text-cosmic-purple transition-colors">
                {experiment.title}
              </h3>
              <div className="flex items-center space-x-3 text-sm text-gray-300 mt-1">
                <span className="bg-nasa-blue/20 text-nasa-blue px-2 py-1 rounded font-mono">
                  {experiment.id}
                </span>
                <span className={`px-2 py-1 rounded text-xs ${getMissionTypeColor(experiment.mission)}`}>
                  {experiment.mission}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        {isSelected && (
          <div className="w-3 h-3 bg-cosmic-purple rounded-full animate-pulse flex-shrink-0"></div>
        )}
      </div>
      
      <p className="text-gray-300 mb-4 leading-relaxed line-clamp-3">
        {experiment.summary}
      </p>
      
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <span className="text-green-400 font-medium italic text-sm">
            {experiment.organism}
          </span>
        </div>
        
        <div className="flex items-center gap-4 text-xs text-star-white/70">
          {experiment.duration && (
            <span className="flex items-center gap-1">
              ⏱️ {experiment.duration}
            </span>
          )}
          {experiment.publicationCount && (
            <span className="flex items-center gap-1">
              📄 {experiment.publicationCount}
            </span>
          )}
        </div>
      </div>

      <div className="flex flex-wrap gap-2 mb-4">
        {experiment.keywords.slice(0, 4).map((keyword, index) => (
          <span 
            key={index}
            className="bg-white/10 hover:bg-cosmic-purple/20 text-gray-300 hover:text-cosmic-purple px-2 py-1 rounded-md text-xs font-mono transition-colors cursor-pointer"
          >
            {keyword}
          </span>
        ))}
        {experiment.keywords.length > 4 && (
          <span className="text-star-white/50 text-xs px-2 py-1">
            +{experiment.keywords.length - 4} more
          </span>
        )}
      </div>

      <div className="flex items-center justify-between">
        {experiment.dataTypes && (
          <div className="flex gap-1">
            {experiment.dataTypes.slice(0, 2).map((type, index) => (
              <span key={index} className="text-xs bg-slate-800/50 text-star-white/80 px-2 py-1 rounded">
                {type}
              </span>
            ))}
          </div>
        )}
        
        <button 
          onClick={(e) => {
            e.stopPropagation();
            if (onViewDetails) onViewDetails(experiment);
          }}
          className="bg-cosmic-purple/20 hover:bg-cosmic-purple hover:text-white text-cosmic-purple px-4 py-2 rounded-lg transition-all duration-200 text-sm font-medium hover:scale-105"
        >
          View Details →
        </button>
      </div>
    </div>
  );
};

export default ExperimentCard;