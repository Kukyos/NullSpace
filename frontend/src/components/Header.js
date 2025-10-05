import React, { useState, useEffect } from 'react';

const Header = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      clearInterval(timer);
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', { 
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <header className="bg-black/20 backdrop-blur-lg border-b border-white/10 sticky top-0 z-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="relative">
              <div className="w-12 h-12 bg-gradient-to-r from-nasa-blue to-nasa-red rounded-lg flex items-center justify-center animate-float">
                <span className="text-white font-bold text-xl font-mono">🚀</span>
              </div>
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full animate-pulse flex items-center justify-center">
                <div className="w-2 h-2 bg-white rounded-full"></div>
              </div>
            </div>
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold text-star-white font-mono">
                NULL<span className="text-cosmic-purple">space</span>
              </h1>
              <p className="text-gray-300 text-xs sm:text-sm">
                NASA Bioscience Data Explorer • AI-Powered
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 sm:space-x-4">
            {/* Connection Status */}
            <div className="hidden sm:flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-green-500' : 'bg-red-500'} animate-pulse`}></div>
              <span className="text-xs text-gray-300">
                {isOnline ? 'ONLINE' : 'OFFLINE'}
              </span>
            </div>

            {/* Mission Time */}
            <div className="glass-morphism px-3 py-2 rounded-lg">
              <div className="text-cosmic-purple font-mono text-xs sm:text-sm">
                <div>MISSION TIME</div>
                <div className="text-star-white font-bold">
                  {formatTime(currentTime)}
                </div>
              </div>
            </div>

            {/* Version Badge */}
            <div className="glass-morphism px-3 py-2 rounded-lg">
              <span className="text-cosmic-purple font-mono text-xs sm:text-sm">
                v2.0.0-BETA
              </span>
            </div>

            {/* Mobile Menu Button */}
            <button className="sm:hidden glass-morphism p-2 rounded-lg text-star-white hover:text-cosmic-purple transition-colors">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mission Status Bar */}
        <div className="mt-3 flex items-center justify-between text-xs">
          <div className="flex items-center space-x-4 text-gray-400">
            <span className="flex items-center gap-1">
              <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></div>
              Data Stream Active
            </span>
            <span className="flex items-center gap-1">
              <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></div>
              AI Models Ready
            </span>
            <span className="flex items-center gap-1">
              <div className="w-1.5 h-1.5 bg-purple-500 rounded-full animate-pulse"></div>
              Knowledge Graph Online
            </span>
          </div>
          <div className="text-gray-500 font-mono">
            ISS Orbital Period: {Math.floor(currentTime.getSeconds() / 90 * 100)}% Complete
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;