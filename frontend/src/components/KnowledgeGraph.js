import React, { useEffect, useRef, useState } from 'react';

const KnowledgeGraph = ({ data, selectedExperiment, experiments = [], onExperimentSelect }) => {
  const cyRef = useRef(null);
  const cyInstance = useRef(null);
  const cleanupRef = useRef(null);
  const [isLoading, setIsLoading] = useState(true);

  // Cleanup function to properly remove DOM elements
  const cleanup = () => {
    if (cyInstance.current) {
      try {
        cyInstance.current.destroy();
      } catch (e) {
        console.log('Cytoscape cleanup:', e);
      }
      cyInstance.current = null;
    }
    
    if (cyRef.current && cleanupRef.current) {
      try {
        // Only remove elements we actually added
        const elementsToRemove = cyRef.current.querySelectorAll('svg, style');
        elementsToRemove.forEach(el => {
          if (el.parentNode === cyRef.current) {
            cyRef.current.removeChild(el);
          }
        });
      } catch (e) {
        // Fallback to innerHTML clear if selective removal fails
        if (cyRef.current) {
          cyRef.current.innerHTML = '';
        }
      }
      cleanupRef.current = null;
    }
  };

  useEffect(() => {
    let isMounted = true;
    
    const initializeGraph = async () => {
      if (!isMounted || !cyRef.current) return;
      
      setIsLoading(true);
      
      // Small delay to ensure DOM is ready
      await new Promise(resolve => setTimeout(resolve, 100));
      
      if (!isMounted) return;
      
      // Cleanup previous render
      cleanup();
      
      if (cyRef.current) {
        if (data && data.nodes && data.nodes.length > 0) {
          // Initialize Cytoscape when data is available
          await initializeCytoscape();
        } else {
          // Show placeholder when no data
          initializePlaceholderGraph();
        }
      }
      
      if (isMounted) {
        setIsLoading(false);
      }
    };

    initializeGraph();

    // Cleanup on unmount or data change
    return () => {
      isMounted = false;
      cleanup();
    };
  }, [data]); // eslint-disable-line react-hooks/exhaustive-deps

  const initializeCytoscape = async () => {
    if (!cyRef.current) return;
    
    try {
      // Dynamically import Cytoscape to avoid SSR issues
      const cytoscape = (await import('cytoscape')).default;
      
      if (cyRef.current && !cyInstance.current) {
        cyInstance.current = cytoscape({
          container: cyRef.current,
          elements: [
            ...data.nodes,
            ...data.edges
          ],
          style: [
            {
              selector: 'node',
              style: {
                'background-color': '#ffffff',
                'border-color': '#ffffff',
                'border-width': 2,
                'label': 'data(label)',
                'width': '40px',
                'height': '40px',
                'text-valign': 'bottom',
                'text-halign': 'center',
                'text-margin-y': 10,
                'color': '#ffffff',
                'font-size': '11px',
                'font-family': 'Inter, sans-serif',
                'font-weight': '500',
                'text-outline-width': 2,
                'text-outline-color': '#000000',
                'opacity': 0.9
              }
            },
            {
              selector: 'node[type="condition"]',
              style: {
                'background-color': '#ffffff',
                'width': '50px',
                'height': '50px'
              }
            },
            {
              selector: 'node[type="process"]',
              style: {
                'background-color': 'none',
                'border-width': 3
              }
            },
            {
              selector: 'node[type="outcome"]',
              style: {
                'background-color': 'none',
                'border-width': 2,
                'border-style': 'dashed'
              }
            },
            {
              selector: 'node[type="organism"]',
              style: {
                'background-color': 'none',
                'border-width': 1,
                'width': '35px',
                'height': '35px'
              }
            },
            {
              selector: 'edge',
              style: {
                'width': 2,
                'line-color': '#ffffff',
                'target-arrow-color': '#ffffff',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
                'opacity': 0.6,
                'arrow-scale': 1.2
              }
            },
            {
              selector: 'node:hover',
              style: {
                'opacity': 1,
                'border-width': 4
              }
            }
          ],
          layout: {
            name: 'cose',
            animate: true,
            animationDuration: 1500,
            nodeRepulsion: 8000,
            nodeOverlap: 20,
            idealEdgeLength: 100,
            padding: 30
          }
        });
        
        cleanupRef.current = true; // Mark that we have content to cleanup
      }
    } catch (error) {
      console.log('Cytoscape not available, using placeholder');
      initializePlaceholderGraph();
    }
  };

  const initializePlaceholderGraph = () => {
    if (!cyRef.current) return;
    
    // Create sleek black & white glowing SVG graph
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.setAttribute("viewBox", "0 0 500 400");
    svg.style.background = "radial-gradient(circle at center, rgba(30, 30, 30, 0.9), rgba(0, 0, 0, 0.95))";
    
    // Define glowing effects
    const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
    
    // Node glow filter
    const nodeGlow = document.createElementNS("http://www.w3.org/2000/svg", "filter");
    nodeGlow.setAttribute("id", "nodeGlow");
    const feGaussianBlur1 = document.createElementNS("http://www.w3.org/2000/svg", "feGaussianBlur");
    feGaussianBlur1.setAttribute("stdDeviation", "8");
    feGaussianBlur1.setAttribute("result", "coloredBlur");
    const feMerge1 = document.createElementNS("http://www.w3.org/2000/svg", "feMerge");
    const feMergeNode1 = document.createElementNS("http://www.w3.org/2000/svg", "feMergeNode");
    feMergeNode1.setAttribute("in", "coloredBlur");
    const feMergeNode2 = document.createElementNS("http://www.w3.org/2000/svg", "feMergeNode");
    feMergeNode2.setAttribute("in", "SourceGraphic");
    feMerge1.appendChild(feMergeNode1);
    feMerge1.appendChild(feMergeNode2);
    nodeGlow.appendChild(feGaussianBlur1);
    nodeGlow.appendChild(feMerge1);
    
    // Line glow filter
    const lineGlow = document.createElementNS("http://www.w3.org/2000/svg", "filter");
    lineGlow.setAttribute("id", "lineGlow");
    const feGaussianBlur2 = document.createElementNS("http://www.w3.org/2000/svg", "feGaussianBlur");
    feGaussianBlur2.setAttribute("stdDeviation", "4");
    feGaussianBlur2.setAttribute("result", "coloredBlur");
    const feMerge2 = document.createElementNS("http://www.w3.org/2000/svg", "feMerge");
    const feMergeNode3 = document.createElementNS("http://www.w3.org/2000/svg", "feMergeNode");
    feMergeNode3.setAttribute("in", "coloredBlur");
    const feMergeNode4 = document.createElementNS("http://www.w3.org/2000/svg", "feMergeNode");
    feMergeNode4.setAttribute("in", "SourceGraphic");
    feMerge2.appendChild(feMergeNode3);
    feMerge2.appendChild(feMergeNode4);
    lineGlow.appendChild(feGaussianBlur2);
    lineGlow.appendChild(feMerge2);
    
    defs.appendChild(nodeGlow);
    defs.appendChild(lineGlow);
    svg.appendChild(defs);
    
    // Sleek node layout with better spacing
    const nodes = [
      {id: 'microgravity', x: 250, y: 80, label: 'Microgravity', type: 'condition', size: 28},
      {id: 'gene-expr', x: 150, y: 200, label: 'Gene Expression', type: 'process', size: 24},
      {id: 'muscle-atr', x: 350, y: 200, label: 'Muscle Atrophy', type: 'outcome', size: 24},
      {id: 'arabidopsis', x: 100, y: 320, label: 'Arabidopsis', type: 'organism', size: 20},
      {id: 'mouse', x: 400, y: 320, label: 'Mouse', type: 'organism', size: 20}
    ];
    
    // Connections with smooth curves
    const connections = [
      {from: 'microgravity', to: 'gene-expr', curve: 'M250,80 Q200,140 150,200'},
      {from: 'microgravity', to: 'muscle-atr', curve: 'M250,80 Q300,140 350,200'},
      {from: 'gene-expr', to: 'arabidopsis', curve: 'M150,200 Q125,260 100,320'},
      {from: 'muscle-atr', to: 'mouse', curve: 'M350,200 Q375,260 400,320'}
    ];
    
    // Draw glowing connections
    connections.forEach(conn => {
      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", conn.curve);
      path.setAttribute("stroke", "#ffffff");
      path.setAttribute("stroke-width", "2");
      path.setAttribute("fill", "none");
      path.setAttribute("opacity", "0.6");
      path.setAttribute("filter", "url(#lineGlow)");
      path.style.animation = "pulse 3s ease-in-out infinite alternate";
      svg.appendChild(path);
    });
    
    // Draw glowing nodes
    nodes.forEach(node => {
      // Outer glow circle
      const outerCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      outerCircle.setAttribute("cx", node.x);
      outerCircle.setAttribute("cy", node.y);
      outerCircle.setAttribute("r", node.size + 4);
      outerCircle.setAttribute("fill", "none");
      outerCircle.setAttribute("stroke", "#ffffff");
      outerCircle.setAttribute("stroke-width", "1");
      outerCircle.setAttribute("opacity", "0.3");
      outerCircle.setAttribute("filter", "url(#nodeGlow)");
      svg.appendChild(outerCircle);
      
      // Main node circle
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", node.x);
      circle.setAttribute("cy", node.y);
      circle.setAttribute("r", node.size);
      circle.setAttribute("fill", node.type === 'condition' ? "#ffffff" : "none");
      circle.setAttribute("stroke", "#ffffff");
      circle.setAttribute("stroke-width", "2");
      circle.setAttribute("opacity", "0.9");
      circle.setAttribute("filter", "url(#nodeGlow)");
      circle.style.cursor = "pointer";
      circle.style.animation = "float 6s ease-in-out infinite";
      circle.style.animationDelay = `${Math.random() * 2}s`;
      svg.appendChild(circle);
      
      // Node label with glow
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", node.x);
      text.setAttribute("y", node.y + node.size + 20);
      text.setAttribute("text-anchor", "middle");
      text.setAttribute("fill", "#ffffff");
      text.setAttribute("font-size", "11");
      text.setAttribute("font-family", "Inter, sans-serif");
      text.setAttribute("font-weight", "500");
      text.setAttribute("opacity", "0.9");
      text.setAttribute("filter", "url(#nodeGlow)");
      text.textContent = node.label;
      svg.appendChild(text);
    });
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
      @keyframes pulse {
        0% { opacity: 0.4; stroke-width: 1; }
        100% { opacity: 0.8; stroke-width: 3; }
      }
      @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-3px); }
      }
    `;
    document.head.appendChild(style);
    
    // Safely append to DOM
    if (cyRef.current) {
      cyRef.current.appendChild(svg);
      cleanupRef.current = true; // Mark that we have content to cleanup
    }
  };

  return (
    <div className="glass-morphism p-6 h-[500px]">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-star-white">
          Experiment Relationships
        </h3>
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-white rounded-full opacity-80"></div>
            <span className="text-xs text-gray-300 font-mono">NEURAL NETWORK</span>
          </div>
        </div>
      </div>
      
      <div 
        ref={cyRef}
        className="w-full h-[400px] bg-gradient-to-br from-black/40 via-gray-900/30 to-black/50 rounded-lg border border-white/20 overflow-hidden relative"
        style={{
          boxShadow: 'inset 0 0 50px rgba(255, 255, 255, 0.05), 0 0 20px rgba(255, 255, 255, 0.1)'
        }}
      >
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center z-10">
            <div className="text-center">
              <div className="animate-spin w-8 h-8 border-2 border-white/30 border-t-white rounded-full mx-auto mb-4"></div>
              <p className="text-gray-300 font-mono text-sm">Initializing neural network...</p>
            </div>
          </div>
        )}
      </div>
      
      <div className="mt-4 space-y-2">
        {/* Legend */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs text-gray-400 font-mono">
          <span className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-nasa-blue rounded-full animate-pulse"></div>
            <span>CONDITIONS</span>
          </span>
          <span className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-cosmic-purple rounded-full animate-pulse"></div>
            <span>PROCESSES</span>
          </span>
          <span className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span>OUTCOMES</span>
          </span>
          <span className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></div>
            <span>ORGANISMS</span>
          </span>
        </div>
        
        {/* Stats */}
        <div className="flex justify-between items-center text-xs text-gray-500 font-mono">
          <span>Nodes: {data?.nodes?.length || 0}</span>
          <span>Relations: {data?.edges?.length || 0}</span>
          <span className="flex items-center gap-1">
            <div className="w-1 h-1 bg-cosmic-purple rounded-full animate-pulse"></div>
            Live Data
          </span>
        </div>
      </div>
    </div>
  );
};

export default KnowledgeGraph;