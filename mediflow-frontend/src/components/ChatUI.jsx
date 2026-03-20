import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Loader } from 'lucide-react';
import { chatWithAgent } from '../api/client';

export default function ChatUI({ patientId, sessionId }) {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I am MediFlow AI. I can help you find doctors, check their availability, and book appointments. How can I help you today?", isUser: false }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { id: Date.now(), text: userMessage, isUser: true }]);
    
    setIsLoading(true);
    try {
      const response = await chatWithAgent(sessionId, userMessage, patientId);
      setMessages(prev => [...prev, { id: Date.now() + 1, text: response.message, isUser: false }]);
    } catch (error) {
      setMessages(prev => [...prev, { id: Date.now() + 1, text: "Sorry, I encountered an error connecting to the server.", isUser: false }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] max-h-screen bg-gray-50 rounded-xl overflow-hidden shadow-lg border border-gray-200">
      <div className="bg-blue-600 text-white p-4 shadow-md flex items-center justify-between z-10">
        <div>
          <h2 className="text-xl font-bold font-sans">MediFlow Assistant</h2>
          <p className="text-blue-100 text-sm">AI Patient Coordinator</p>
        </div>
        <Bot size={28} className="text-blue-100" />
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-[#e5ddd5] opacity-95">
        {messages.map(msg => (
          <div key={msg.id} className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl p-3 shadow-sm ${msg.isUser ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-white text-gray-800 rounded-tl-none font-medium'}`}>
              <div className="flex items-center space-x-2 mb-1">
                 {msg.isUser ? <User size={14} className="opacity-70" /> : <Bot size={14} className="text-blue-500" />}
                 <span className="text-xs opacity-70 font-semibold">{msg.isUser ? 'You' : 'MediFlow AI'}</span>
              </div>
              <div className="whitespace-pre-wrap leading-relaxed">
                {msg.text}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white rounded-2xl rounded-tl-none p-4 shadow-sm">
              <Loader className="animate-spin text-blue-500" size={20} />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="p-3 bg-white border-t border-gray-200">
        <form onSubmit={handleSend} className="flex items-center space-x-2">
          <input 
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message here..."
            className="flex-1 p-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50 transition-all font-sans"
            disabled={isLoading}
          />
          <button 
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 text-white p-3 rounded-full hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
          >
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
}
