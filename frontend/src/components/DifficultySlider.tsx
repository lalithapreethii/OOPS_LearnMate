import React from 'react';

interface DifficultySliderProps {
  selectedDifficulty: 'EASY' | 'MEDIUM' | 'HARD';
  onDifficultyChange: (difficulty: 'EASY' | 'MEDIUM' | 'HARD') => void;
}

const DifficultySlider: React.FC<DifficultySliderProps> = ({ 
  selectedDifficulty, 
  onDifficultyChange 
}) => {
  const difficulties: ('EASY' | 'MEDIUM' | 'HARD')[] = ['EASY', 'MEDIUM', 'HARD'];
  const colors = {
    EASY: '#4CAF50',
    MEDIUM: '#FF9800',
    HARD: '#F44336'
  };

  const difficultyIndex = difficulties.indexOf(selectedDifficulty);

  const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value);
    onDifficultyChange(difficulties[value]);
  };

  return (
    <div className="difficulty-slider-container mb-8 p-6 bg-primary rounded-xl shadow-lg">
      <h3 className="text-xl font-bold text-primary mb-6 text-center">
        Select Difficulty Level
      </h3>
      
      <div className="slider-wrapper relative mb-6">
        <input
          type="range"
          min="0"
          max="2"
          value={difficultyIndex}
          onChange={handleSliderChange}
          className="w-full h-2 rounded-lg appearance-none cursor-pointer slider"
          style={{
            background: `linear-gradient(to right, 
              ${colors[selectedDifficulty]} 0%, 
              ${colors[selectedDifficulty]} ${(difficultyIndex / 2) * 100}%, 
              #e0e0e0 ${(difficultyIndex / 2) * 100}%, 
              #e0e0e0 100%)`
          }}
        />
        
        <div className="difficulty-labels flex justify-between mt-4 px-1">
          {difficulties.map((level) => (
            <button
              key={level}
              onClick={() => onDifficultyChange(level)}
              className={`
                text-sm font-medium transition-all duration-300 px-3 py-1 rounded-lg
                ${selectedDifficulty === level 
                  ? 'text-white font-bold transform scale-110 shadow-md' 
                  : 'text-muted hover:text-primary'
                }
              `}
              style={{
                backgroundColor: selectedDifficulty === level ? colors[level] : 'transparent'
              }}
            >
              {level.charAt(0) + level.slice(1).toLowerCase()}
            </button>
          ))}
        </div>
      </div>

      <div 
        className="difficulty-indicator mt-6 py-3 px-6 rounded-lg text-white text-center font-bold text-lg transition-all duration-300 shadow-lg transform hover:scale-105"
        style={{ backgroundColor: colors[selectedDifficulty] }}
      >
        <span className="mr-2">🎯</span>
        Current: {selectedDifficulty}
      </div>

      <style dangerouslySetInnerHTML={{__html: `
        .slider::-webkit-slider-thumb {
          appearance: none;
          width: 24px;
          height: 24px;
          border-radius: 50%;
          background: white;
          border: 3px solid ${colors[selectedDifficulty]};
          cursor: pointer;
          box-shadow: 0 2px 8px rgba(0,0,0,0.3);
          transition: all 0.3s ease;
        }

        .slider::-webkit-slider-thumb:hover {
          transform: scale(1.2);
          box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }

        .slider::-moz-range-thumb {
          width: 24px;
          height: 24px;
          border-radius: 50%;
          background: white;
          border: 3px solid ${colors[selectedDifficulty]};
          cursor: pointer;
          box-shadow: 0 2px 8px rgba(0,0,0,0.3);
          transition: all 0.3s ease;
        }

        .slider::-moz-range-thumb:hover {
          transform: scale(1.2);
          box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
      `}} />
    </div>
  );
};

export default DifficultySlider;
