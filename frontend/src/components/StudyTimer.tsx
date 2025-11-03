import React, { useState, useEffect } from 'react';
import { Clock, Play, Pause, RotateCcw } from 'lucide-react';

interface StudyTimerProps {
  theme: 'light' | 'dark';
}

const StudyTimer: React.FC<StudyTimerProps> = ({ theme }) => {
  const [time, setTime] = useState(1500); // 25 minutes in seconds
  const [isRunning, setIsRunning] = useState(false);
  const [isBreak, setIsBreak] = useState(false);

  useEffect(() => {
    let interval: number | null = null; // ✅ CHANGED FROM NodeJS.Timeout

    if (isRunning && time > 0) {
      interval = window.setInterval(() => { // ✅ ADDED window.
        setTime((prevTime) => prevTime - 1);
      }, 1000);
    } else if (time === 0) {
      // Auto-switch between work and break
      if (isBreak) {
        setTime(1500); // 25 min work
        setIsBreak(false);
      } else {
        setTime(300); // 5 min break
        setIsBreak(true);
      }
      setIsRunning(false);
      
      // Play notification sound (optional)
      const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBTGH0fPTgjMGHm7A7+OZRQ0PVare7rdmHAU2ldvzzn0vBSl+zPLZkEELElyx6+ulVBEMRJzi8bhhGwU0i9Xx14Y1Bh5qwO/mnEcODlOq3+6/aB8GM5LZ88l8MAUogMv02ZJDCxJatuntp1YWDEKU4PG9YhwFM4nU8tiIOAYebsDv5p5JDg5SqeHuwWkfBTCN2fPIfTAFJnvJ89iURA0RWq/p7qpXFw1DkN/yvmUdBTGG0vLWizkGHWq+7+ejSw8PUqfi7sJrIQU2jdXyzHwwBSJ5yPPYlkYOEFer6vCsWhkNQ47f8r5oHgU0hdLy1os4Bxpowu/mok0PDlKm4e/FbyMFNYvU8s9/MAUfecf02JhIDxBVqu3yuVweEUGM3vK/ax8FM4PQ8tiLNwgbaL/v56ZNEQ9Ppt/vxHAjBTSJ0/LPfjAFHXfG89mZSRAQVKjq8bpcHhJBit7yv2wfBTJ/z/PYjTcIHmW87+imURIPTqLe78ZxJAU0h9Hyz34wBht2xfPZm0oRD1Om6fK7XB8SQYje8r9tHwUygM/02I03CB5ju+7pplISEE2g3u/HcSQFM4XQ8s9+LwUbdMPz2ZxLEBBUpenyvFwfE0KG3fO/bR8FMX/N9NiNNwgdYbnv6aalUhIQTJ/e78hxJAUzg8/yzoAvBRtzwfLZnUsREVOj6fK8XSATQoTd871uIAUxfs302I03CB1bubvn5qJSEhFMnt3vyG8jBTKCzvLOgC8FG3G/8tmdSxERU6Lp8rxeIBRCgt3zvW4gBTF8zPTXjjYIHV+2u+aiUhIRTJ3d78hvIgUyg83yzoAvBRxvvvLZnUoQEVKh6PK9XiAUQoHc871uIAUwes302I43CB1etLrnoVIRDk2c3e7Hbx8FMoPM8s6AMAUccrzx2Z1KEhJRn+jyu14iFEJ/3PO9byAFMXjK9NiNNwkdXbK556FRDwxOms3ux24gBDKEy/HPgC8GHG+68dmeTBQTUJzn8r1gIxVDftr0vXEhBDJ4yPPYjTcJHV2y4+agURALT5jN7shuIAUzgsrxz38wBhxvuvHZnkwUE1Cc5/K9YCMVQnzZ9L1xIQQyd8f02I43Ch5dsN/mnVAMC1CWzO7HbiIFM4DI8c9/LwYabrnx2Z5MFBRSW+fyu2EkFkN72fS9cSEFM3XF9NiNNwoeTa/e5p1QCwtQlMzux24iBDR9xfLPfy8GHGu48dmeTRUSUlrm8rthJRZDd9n0vXEhBTN0w/TXjTYKH0ys3eaaUQoIUZPL7cduIgQ0fMTyz38wBx1rue/ZnU0WElJZ5vK7YiYWQ3XY9L1wIAUzdML014w2Ch9KqtzmmlAMCFGSyezGbSIENXzC8c9/MQgda7fv2Z1MFxNRV+Xyu2IlFkN12fS9cB8EM3PB9NWLNgofSajc5ppQCQhSkcnsxWwiBDV7wPHPfi8HG2m38dmeTBkTUFXk8rpiJRZDdNj0vm8fBDNywfTVizULH0il2+aaURILUo/I7MRpIQM1eb/xz34wBx1otO7Zn00aFFBU4/K5YSUWQnPX9L5uHwQzcr/01Ys1Ch9IpNvlmVESEVKOxuzDaSEDNXi+8c99LwcaaLPu2Z5MHBFQUuPyt2IlFUI== ');
      audio.play().catch(() => {}); // Silent fail if audio blocked
    }

    return () => {
      if (interval !== null) { // ✅ CHANGED CHECK
        window.clearInterval(interval); // ✅ ADDED window.
      }
    };
  }, [isRunning, time, isBreak]);

  const toggleTimer = () => {
    setIsRunning(!isRunning);
  };

  const resetTimer = () => {
    setIsRunning(false);
    setTime(1500);
    setIsBreak(false);
  };

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className={`px-5 py-4 rounded-lg ${
      isBreak 
        ? 'bg-green-500/20 border border-green-500/30' 
        : 'bg-indigo-500/20 border border-indigo-500/30'
    }`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center">
          <Clock className="w-5 h-5 mr-2 text-indigo-400" />
          <span className="text-sm font-medium text-gray-300">
            {isBreak ? 'Break Time' : 'Study Timer'}
          </span>
        </div>
      </div>
      
      <div className="text-3xl font-bold text-white mb-3 text-center font-mono">
        {formatTime(time)}
      </div>

      <div className="flex gap-2">
        <button
          onClick={toggleTimer}
          className="flex-1 flex items-center justify-center py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 transition-colors"
          title={isRunning ? 'Pause' : 'Start'}
        >
          {isRunning ? (
            <Pause className="w-4 h-4 text-white" />
          ) : (
            <Play className="w-4 h-4 text-white" />
          )}
        </button>
        
        <button
          onClick={resetTimer}
          className="flex-1 flex items-center justify-center py-2 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors"
          title="Reset"
        >
          <RotateCcw className="w-4 h-4 text-white" />
        </button>
      </div>

      <div className="mt-2 text-xs text-gray-400 text-center">
        {isBreak ? '5 min break' : '25 min focus'}
      </div>
    </div>
  );
};

export default StudyTimer;
