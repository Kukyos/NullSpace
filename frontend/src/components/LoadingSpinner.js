import React from 'react';

const LoadingSpinner = ({ size = 'medium', color = 'star-white' }) => {
  const sizeClasses = {
    small: 'w-4 h-4',
    medium: 'w-8 h-8',
    large: 'w-12 h-12'
  };

  return (
    <div className="flex items-center justify-center">
      <div className={`${sizeClasses[size]} animate-spin`}>
        <div className={`w-full h-full border-4 border-${color}/20 border-t-${color} rounded-full`}></div>
      </div>
    </div>
  );
};

export default LoadingSpinner;