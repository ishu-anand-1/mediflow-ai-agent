import React, { useState } from 'react';
import { setAvailability, setStatus } from '../api/client';
import { Calendar, Clock, Activity, Settings } from 'lucide-react';

export default function DoctorDashboard({ doctorId }) {
  const [date, setDate] = useState('');
  const [slots, setSlots] = useState('');
  const [status, setStatusMessage] = useState(null);
  const [isActive, setIsActive] = useState(true);

  const handleToggleStatus = async () => {
    try {
      const newStatus = !isActive;
      await setStatus(doctorId, newStatus);
      setIsActive(newStatus);
      setStatusMessage({ type: 'success', msg: `Doctor is now visible to Patients: ${newStatus ? 'ON' : 'OFF'}` });
    } catch (e) {
      setStatusMessage({ type: 'error', msg: 'Failed to update visibility.' });
    }
  };

  const handleUpdateAvailability = async (e) => {
    e.preventDefault();
    try {
      const slotsList = slots.split(',').map(s => s.trim());
      await setAvailability({
        doctor_id: doctorId,
        date: date,
        slots: slotsList
      });
      setStatusMessage({ type: 'success', msg: 'Availability updated successfully!' });
      setSlots('');
      setDate('');
    } catch (error) {
      setStatusMessage({ type: 'error', msg: 'Failed to update availability.' });
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
      <div className="bg-indigo-600 text-white p-6">
        <div className="flex items-center space-x-3">
          <Activity size={28} />
          <h2 className="text-2xl font-bold font-sans">Provider Dashboard</h2>
        </div>
        <p className="text-indigo-100 mt-1">Manage your schedule and view AI reports</p>
        
        <div className="flex items-center mt-5 space-x-3">
          <button 
            type="button"
            onClick={handleToggleStatus}
            className={`px-5 py-2 font-bold rounded-full transition-colors ${isActive ? 'bg-green-400 hover:bg-green-500 text-gray-900 border-2 border-green-300' : 'bg-red-400 hover:bg-red-500 text-white border-2 border-red-300'}`}
          >
            {isActive ? '● Today ON' : '○ Today OFF'}
          </button>
          <span className="text-sm text-indigo-100 font-medium">
            {isActive ? 'You are visible in patient queries.' : 'You are currently hidden from LLM searches.'}
          </span>
        </div>
      </div>
      
      <div className="p-6">
        <h3 className="text-lg font-bold text-gray-800 flex items-center mb-4 font-sans">
          <Calendar className="mr-2 text-indigo-500" size={20} />
          Set Daily Availability
        </h3>
        
        <form onSubmit={handleUpdateAvailability} className="space-y-5">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">Date</label>
            <input 
              type="date" 
              required
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-shadow"
            />
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-1">Time Slots (comma separated, e.g. 09:00, 10:00)</label>
            <div className="relative">
              <Clock className="absolute left-3 top-3 text-gray-400" size={18} />
              <input 
                type="text" 
                required
                value={slots}
                onChange={(e) => setSlots(e.target.value)}
                placeholder="10:00, 11:30, 14:00"
                className="w-full p-2.5 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-shadow"
              />
            </div>
          </div>
          
          <button 
            type="submit"
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2 shadow-sm"
          >
            <Settings size={18} />
            <span>Update Schedule</span>
          </button>
        </form>
        
        {status && (
          <div className={`mt-4 p-3 rounded-lg text-sm font-medium ${status.type === 'success' ? 'bg-green-100 text-green-800 border border-green-200' : 'bg-red-100 text-red-800 border border-red-200'}`}>
            {status.msg}
          </div>
        )}

        <div className="mt-8 pt-6 border-t border-gray-100">
           <p className="text-sm text-gray-500 leading-relaxed">
             AI reporting can be queried via the patient interface by entering "Get doctor stats for doctor ID {doctorId} on YYYY-MM-DD". The agent will call the <code className="bg-gray-100 px-1 rounded text-red-500">get_doctor_stats</code> tool and summarize your performance.
           </p>
        </div>
      </div>
    </div>
  );
}
