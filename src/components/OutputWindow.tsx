'use client';

import { useState, useRef, useEffect } from 'react';

interface OutputWindowProps {
  messages: string[];
  onClear: () => void;
}

export default function OutputWindow({ messages, onClear }: OutputWindowProps) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [filter, setFilter] = useState<'all' | 'errors' | 'info'>('all');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const filteredMessages = messages.filter(msg => {
    if (filter === 'errors') return msg.toLowerCase().includes('error') || msg.toLowerCase().includes('failed');
    if (filter === 'info') return msg.toLowerCase().includes('result') || msg.toLowerCase().includes('converged');
    return true;
  });

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className={`bg-gray-900 text-gray-300 border-t border-gray-300 transition-all ${isExpanded ? 'h-48' : 'h-8'}`}>
      {/* Header */}
      <div 
        className="flex items-center justify-between px-3 py-1 bg-gray-800 cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center gap-4">
          <span className="text-sm font-medium text-white">Output</span>
          {isExpanded && (
            <div className="flex gap-2">
              <button
                onClick={(e) => { e.stopPropagation(); setFilter('all'); }}
                className={`px-2 py-0.5 text-xs rounded ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-400'}`}
              >
                All
              </button>
              <button
                onClick={(e) => { e.stopPropagation(); setFilter('errors'); }}
                className={`px-2 py-0.5 text-xs rounded ${filter === 'errors' ? 'bg-red-600 text-white' : 'bg-gray-700 text-gray-400'}`}
              >
                Errors
              </button>
              <button
                onClick={(e) => { e.stopPropagation(); setFilter('info'); }}
                className={`px-2 py-0.5 text-xs rounded ${filter === 'info' ? 'bg-green-600 text-white' : 'bg-gray-700 text-gray-400'}`}
              >
                Info
              </button>
            </div>
          )}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500">{filteredMessages.length} messages</span>
          <button
            onClick={(e) => { e.stopPropagation(); onClear(); }}
            className="px-2 py-0.5 text-xs bg-gray-700 rounded hover:bg-gray-600"
          >
            Clear
          </button>
          <span className="text-gray-400">{isExpanded ? '▼' : '▲'}</span>
        </div>
      </div>

      {/* Messages */}
      {isExpanded && (
        <div className="h-36 overflow-y-auto p-2 font-mono text-xs">
          {filteredMessages.length === 0 ? (
            <div className="text-gray-500">No messages to display</div>
          ) : (
            filteredMessages.map((msg, idx) => {
              const isError = msg.toLowerCase().includes('error');
              const isSuccess = msg.toLowerCase().includes('converged') || msg.toLowerCase().includes('✓');
              
              return (
                <div 
                  key={idx} 
                  className={`py-0.5 ${
                    isError ? 'text-red-400' : 
                    isSuccess ? 'text-green-400' : 
                    'text-gray-300'
                  }`}
                >
                  {msg}
                </div>
              );
            })
          )}
          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
}