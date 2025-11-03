import React, { useState, useEffect, useRef } from 'react';
import DifficultySlider from './components/DifficultySlider';
import { quizApi } from './services/quizApi';
import Login from './components/Login';
import axios from 'axios';
import {
  LayoutDashboard,
  Brain,
  BookOpen,
  Bot,
  User,
  Send,
  BarChart,
  Target,
  Loader2,
  BookMarked,
  Flame,
  TrendingUp,
  CheckCircle,
  Atom,
  FlaskConical,
  Server,
  X,
  Cpu,
  Calculator,
  Dna,
  Terminal,
  Sun,
  Moon,
  LogOut,
  // Added for Timer
  Clock,
  Play,
  Pause,
  RotateCcw,
  StickyNote,
  Plus,
  Edit,
  Trash2,
  Save,
} from 'lucide-react';

// ✅ CHANGE 4: Updated Page Type
type Page = 'dashboard' | 'quizzes' | 'resources' | 'chatbot' | 'profile' | 'notes' | 'timer';
type Theme = 'light' | 'dark';

interface Question {
  id: string;
  text: string;
  topic: string;
  options: { id: string; text: string }[];
  correctOptionId: string;
}

interface Topic {
  id: number;
  name: string;
  description: string;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
}

interface Resource {
  id: string;
  title: string;
  type: 'video' | 'article' | 'quiz';
  link: string; // renamed from `url` to `link` to avoid editor/TS conflicts
  estimatedTime: string;
  topic: string;
}

interface ChatMessage {
  role: 'user' | 'bot';
  content: string;
}

interface WeakTopic {
  topic: string;
  currentScore: number;
  goalScore?: number;
}

interface UserData {
  userId: number;
  name: string;
  email: string;
}

interface Note {
  id: string;
  title: string;
  content: string;
  subject: string;
  createdAt: Date;
  updatedAt: Date;
}

interface QuizAccuracy {
  name: string;
  accuracy: number;
}

const API_BASE_URL = 'http://localhost:8082/api';

const MOCK_USER_DATA: UserData = {
  userId: 1,
  name: 'Student',
  email: 'student@example.com'
};

const MOCK_WEAK_TOPICS: WeakTopic[] = [
  { topic: 'Data Structures', currentScore: 45, goalScore: 80 },
  { topic: 'Algorithms', currentScore: 60, goalScore: 80 },
  { topic: 'Machine Learning Concepts', currentScore: 30, goalScore: 75 },
  { topic: 'Polymorphism', currentScore: 70, goalScore: 90 },
];

const INITIAL_QUIZ_ACCURACY: QuizAccuracy[] = [
  { name: 'Quiz 1', accuracy: 60 },
  { name: 'Quiz 2', accuracy: 80 },
  { name: 'Quiz 3', accuracy: 50 },
  { name: 'Quiz 4', accuracy: 90 },
  { name: 'Quiz 5', accuracy: 75 },
];

const INITIAL_WEEKLY_STREAK = 4;

const MOCK_TOPICS: Topic[] = [
  { id: 1, name: 'Object-Oriented Programming', description: 'Test your knowledge of classes, objects, and inheritance.', difficulty: 'MEDIUM' },
  { id: 2, name: 'Data Structures', description: 'Explore arrays, linked lists, stacks, and queues.', difficulty: 'EASY' },
  { id: 3, name: 'Algorithms', description: 'Challenge yourself with sorting and searching algorithms.', difficulty: 'HARD' },
  { id: 4, name: 'Physics', description: 'From kinematics to quantum mechanics, test your physics knowledge.', difficulty: 'MEDIUM' },
  { id: 5, name: 'Chemistry', description: 'Explore atoms, molecules, and chemical reactions.', difficulty: 'MEDIUM' },
  { 
    id: 6, name: 'Operating Systems', description: 'Understand processes, memory, and file systems.', difficulty: 'HARD' },
  { id: 7, name: 'Math', description: 'Calculus, Algebra, and more. Test your math skills.', difficulty: 'MEDIUM' },
  { id: 8, name: 'Biology', description: 'Explore cells, genetics, and evolution.', difficulty: 'EASY' },
  { id: 9, name: 'AIML Basics', description: 'Understand the fundamentals of AI and Machine Learning.', difficulty: 'HARD' },
];

const MOCK_QUIZ: Question[] = [
  // Small, well-formed sample quiz set used by the app. Keep concise and valid.
  { id: 'oops1', topic: 'Object-Oriented Programming', text: 'Which concept allows using the same function name with different arguments?', options: [ { id: 'o1', text: 'Encapsulation' }, { id: 'o2', text: 'Inheritance' }, { id: 'o3', text: 'Polymorphism' }, { id: 'o4', text: 'Abstraction' } ], correctOptionId: 'o3' },
  { id: 'ds1', topic: 'Data Structures', text: 'What is the time complexity of adding an element to a hash set on average?', options: [ { id: 'o1', text: 'O(1)' }, { id: 'o2', text: 'O(n)' }, { id: 'o3', text: 'O(log n)' }, { id: 'o4', text: 'O(n^2)' } ], correctOptionId: 'o1' },
  { id: 'algo1', topic: 'Algorithms', text: 'Which algorithm finds the shortest path in an unweighted graph?', options: [ { id: 'o1', text: 'Dijkstra' }, { id: 'o2', text: 'Bellman-Ford' }, { id: 'o3', text: 'Breadth-First Search' }, { id: 'o4', text: 'Depth-First Search' } ], correctOptionId: 'o3' },
  { id: 'phy1', topic: 'Physics', text: "What is Newton's second law of motion?", options: [ { id: 'o1', text: 'F = ma (Force = mass * acceleration)' }, { id: 'o2', text: 'E = mc^2' }, { id: 'o3', text: 'P = IV' }, { id: 'o4', text: 'V = IR' } ], correctOptionId: 'o1' },
  { id: 'chem1', topic: 'Chemistry', text: 'What is the chemical symbol for Gold?', options: [ { id: 'o1', text: 'Go' }, { id: 'o2', text: 'Gd' }, { id: 'o3', text: 'Ag' }, { id: 'o4', text: 'Au' } ], correctOptionId: 'o4' },
  { id: 'math1', topic: 'Math', text: 'What is the derivative of x^2?', options: [ { id: 'o1', text: '2x' }, { id: 'o2', text: 'x' }, { id: 'o3', text: 'x^3 / 3' }, { id: 'o4', text: '2' } ], correctOptionId: 'o1' },
  { id: 'bio1', topic: 'Biology', text: 'What is the powerhouse of the cell?', options: [ { id: 'o1', text: 'Nucleus' }, { id: 'o2', text: 'Mitochondria' }, { id: 'o3', text: 'Ribosome' }, { id: 'o4', text: 'Chloroplast' } ], correctOptionId: 'o2' },
  { id: 'aiml1', topic: 'AIML Basics', text: 'What does NLP stand for?', options: [ { id: 'o1', text: 'Natural Language Processing' }, { id: 'o2', text: 'Neural Link Protocol' }, { id: 'o3', text: 'Network Logic Programming' }, { id: 'o4', text: 'New Logic Paradigm' } ], correctOptionId: 'o1' },
  { id: 'os1', topic: 'Operating Systems', text: 'What is a process in an operating system?', options: [ { id: 'o1', text: 'A file stored on disk' }, { id: 'o2', text: 'A program in execution' }, { id: 'o3', text: 'A hardware device' }, { id: 'o4', text: 'A system call' } ], correctOptionId: 'o2' }
];

const MOCK_RESOURCES: Resource[] = [
  { id: 'r1', title: 'Data Structures & Algorithms', type: 'article' as const, link: 'https://www.geeksforgeeks.org/data-structures-and-algorithms-interview-questions/', estimatedTime: '45 min', topic: 'DSA' },
  { id: 'r2', title: 'OOPS Concepts', type: 'article' as const, link: 'https://www.interviewbit.com/oops-interview-questions/', estimatedTime: '30 min', topic: 'OOPS' },
  { id: 'r3', title: 'Operating Systems Playlist', type: 'video' as const, link: 'https://www.youtube.com/playlist?list=PLBlnK6fEyqRj00w9DqnX8M0dBHogY42_P', estimatedTime: '1-2 hours', topic: 'Operating Systems' },
  { id: 'r4', title: 'Khan Academy Physics', type: 'video' as const, link: 'https://www.khanacademy.org/science/physics', estimatedTime: 'Variable', topic: 'Physics' },
  { id: 'r5', title: 'Chemguide UK', type: 'article' as const, link: 'https://chemguide.co.uk/', estimatedTime: 'Variable', topic: 'Chemistry' },
  { 
id: 'r6', title: 'Khan Academy Biology', type: 'video' as const, link: 'https://www.khanacademy.org/science/biology', estimatedTime: 'Variable', topic: 'Biology' },
  { id: 'r7', title: 'Crash Course: AI', type: 'video' as const, link: 'https://www.youtube.com/playlist?list=PL8dPuuaLjXtO_S-gopL2FkF-GjA5a2-3q', estimatedTime: '2-3 hours', topic: 'AIML Basics' },
  { id: 'r8', title: 'Maths is Fun', type: 'article' as const, link: 'https://www.mathsisfun.com/', estimatedTime: 'Variable', topic: 'Math' },
  { id: 'r9', title: 'Quick Sort Explained', type: 'article' as const, link: 'https://www.baeldung.com/java-quicksort', estimatedTime: '15 min', topic: 'Algorithms' },
  { id: 'r10', title: 'Intro to Linked Lists', type: 'video' as const, link: 'https://www.youtube.com/watch?v=njTh_1TjPbs', estimatedTime: '10 min', topic: 'Data Structures' },
];

// --- Mock API ---

const mockApi = <T,>(data: T, delay: number): Promise<T> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(data);
    }, delay);
  });
};

const fetchWithBackoff = async (
  url: string,
  options: RequestInit,
  retries = 3,
  delay = 500
): Promise<Response> => {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response;
  } catch (error) {
    if (retries > 0) {
      console.warn(`API call failed, retrying in ${delay}ms... (${retries} retries left)`);
      await new Promise(res => setTimeout(res, delay));
      return fetchWithBackoff(url, options, retries - 1, delay * 2);
    }
    throw error;
  }
};

// --- CSS Definitions ---

const cssVariables = `
:root {
  --bg-primary: 255 255 255;
  --bg-secondary: 247 248 252;
  --bg-accent: 232 234 246;
  --text-primary: 18 20 34;
  --text-secondary: 70 73 97;
  --text-muted: 130 134 163;
  --border-primary: 228 230 244;
}
.dark {
  --bg-primary: 31 33 58;
  --bg-secondary: 23 25 45;
  --bg-accent: 46 49 80;
  --text-primary: 255 255 255;
  --text-secondary: 198 201 230;
  --text-muted: 104 109 158;
  --border-primary: 46 49 80;
}
`;

const globalStyles = `
body {
  background-color: rgb(var(--bg-secondary));
  color: rgb(var(--text-secondary));
  font-family: "Inter", sans-serif;
  transition: background-color 0.3s ease, color 0.3s ease;
}
.bg-primary { background-color: rgb(var(--bg-primary)); }
.bg-secondary { background-color: rgb(var(--bg-secondary)); }
.bg-accent { background-color: rgb(var(--bg-accent)); }
.text-primary { color: rgb(var(--text-primary)); }
.text-secondary { color: rgb(var(--text-secondary)); }
.text-muted { color: rgb(var(--text-muted)); }
.border-primary { border-color: rgb(var(--border-primary)); }

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 10px;
}
::-webkit-scrollbar-track {
  background: rgb(var(--bg-secondary));
}
::-webkit-scrollbar-thumb {
  background-color: rgb(var(--bg-accent));
  border-radius: 6px;
  border: 3px solid rgb(var(--bg-secondary));
}
::-webkit-scrollbar-thumb:hover {
  background-color: #555;
}

/* Animations */
@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fade-in-up 0.5s ease-out forwards;
}
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
.animate-fade-in {
  animation: fade-in 0.3s ease-out forwards;
}
@keyframes progress-bar-fill {
  from { width: 0%; }
}
.animate-progress-bar {
  animation: progress-bar-fill 1s ease-in-out forwards;
}
@keyframes bar-grow {
  from { transform: scaleY(0); }
  to { transform: scaleY(1); }
}
.animate-bar-grow {
  animation: bar-grow 0.7s ease-out forwards;
  transform-origin: bottom;
}
@keyframes doughnut-spin {
  from { transform: rotate(-90deg); }
  to { transform: rotate(0deg); }
}
.animate-doughnut-spin {
  animation: doughnut-spin 1s ease-out forwards;
}
@keyframes skilli-jump {
  0%, 100% { transform: translateY(0) scale(1); }
  25% { transform: translateY(-30px) translateX(-15px) rotate(-15deg) scale(1.1); }
  50% { transform: translateY(0) scale(1); }
  75% { transform: translateY(-30px) translateX(15px) rotate(15deg) scale(1.1); }
}
.animate-skilli-jump {
  animation: skilli-jump 3s ease-in-out infinite 1s;
}
@keyframes gradient-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
.animate-gradient-shift {
  background-size: 200% 200%;
  animation: gradient-shift 6s ease-in-out infinite;
}
`;

// Setup axios to include JWT token in all requests
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('jwt_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// --- Components ---

const GlobalStyles = () => (
  <style dangerouslySetInnerHTML={{ __html: cssVariables + globalStyles }} />
);

// ✅ CHANGE 1: Replaced old StudyTimer with TimerButton + TimerPage

// ✅ NEW: Simple Hexagonal Timer Button
const TimerButton: React.FC<{ onClick: () => void }> = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="w-full px-5 py-4 rounded-lg transition-colors duration-200 text-lg text-gray-400 hover:bg-gray-700 hover:text-white flex items-center"
      title="Study Timer"
    >
      <div className="w-10 h-10 flex items-center justify-center bg-violet-600 rounded" style={{
        clipPath: 'polygon(30% 0%, 70% 0%, 100% 50%, 70% 100%, 30% 100%, 0% 50%)'
      }}>
        <Clock className="w-6 h-6 text-white" />
      </div>
      <span className="font-medium ml-3">Study Timer</span>
    </button>
  );
};

// ✅ NEW: Full Timer Page Component
const TimerPage: React.FC<{ onClose: () => void }> = ({ onClose }) => {
  const [duration, setDuration] = useState(25); // Default 25 minutes
  const [time, setTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [isActive, setIsActive] = useState(false);

  useEffect(() => {
    let interval: number | null = null;

    if (isRunning && time > 0) {
      interval = window.setInterval(() => {
        setTime((prevTime) => prevTime - 1);
      }, 1000);
    } else if (time === 0 && isActive) {
      setIsRunning(false);
      setIsActive(false);
      
      // Save study session to backend
      saveStudySession();
      
      alert('Timer completed! Time for a break! 🎉');
    }

    return () => {
      if (interval !== null) {
        window.clearInterval(interval);
      }
    };
  }, [isRunning, time, isActive]);

  const saveStudySession = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/study-sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: 1,
          durationMinutes: duration,
          topic: 'General Study',
          sessionDate: new Date().toISOString().split('T')[0]
        })
      });
      
      if (response.ok) {
        console.log('Study session saved successfully');
      }
    } catch (error) {
      console.error('Failed to save study session:', error);
    }
  };

  const startTimer = () => {
    setTime(duration * 60);
    setIsRunning(true);
    setIsActive(true);
  };

  const toggleTimer = () => {
    setIsRunning(!isRunning);
  };

  const resetTimer = () => {
    setIsRunning(false);
    setTime(duration * 60);
  };

  const stopTimer = () => {
    setIsRunning(false);
    setIsActive(false);
    setTime(0);
  };

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-primary rounded-2xl shadow-2xl max-w-md w-full p-8 border border-primary">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-3xl font-bold text-primary flex items-center">
            <Clock className="w-8 h-8 mr-3 text-violet-600" />
            Study Timer
          </h2>
          <button
            onClick={onClose}
            className="text-muted hover:text-primary transition-colors"
            title="Close"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {!isActive ? (
          // Timer Setup Screen
          <div className="space-y-6">
            <div>
              <label className="block text-secondary font-medium mb-3 text-lg">
                How many minutes do you want to study?
              </label>
              <div className="flex items-center gap-4">
                <input
                  type="range"
                  min="1"
                  max="120"
                  value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))}
                  className="flex-1 h-2 bg-accent rounded-lg appearance-none cursor-pointer"
                  style={{
                    background: `linear-gradient(to right, #8b5cf6 0%, #8b5cf6 ${(duration / 120) * 100}%, rgb(var(--bg-accent)) ${(duration / 120) * 100}%, rgb(var(--bg-accent)) 100%)`
                  }}
                />
                <span className="text-4xl font-bold text-violet-600 w-20 text-right">
                  {duration}
                </span>
              </div>
              <div className="flex justify-between text-sm text-muted mt-2">
                <span>1 min</span>
                <span>120 min</span>
              </div>
            </div>

            <div className="grid grid-cols-4 gap-2">
              {[5, 10, 15, 25, 30, 45, 60, 90].map((preset) => (
                <button
                  key={preset}
                  onClick={() => setDuration(preset)}
                  className={`py-2 px-3 rounded-lg font-medium transition-colors ${
                    duration === preset
                      ? 'bg-violet-600 text-white'
                      : 'bg-secondary text-secondary hover:bg-accent'
                  }`}
                >
                  {preset}m
                </button>
              ))}
            </div>

            <button
              onClick={startTimer}
              className="w-full py-4 bg-violet-600 hover:bg-violet-700 text-white font-bold text-xl rounded-lg transition-colors flex items-center justify-center gap-2"
            >
              <Play className="w-6 h-6" />
              Start Timer
            </button>
          </div>
        ) : (
          // Timer Running Screen
          <div className="space-y-6">
            <div className="text-center">
              <div className="text-7xl font-bold text-violet-600 font-mono mb-4">
                {formatTime(time)}
              </div>
              <p className="text-xl text-secondary">
                {isRunning ? '🔥 Focus Time!' : '⏸️ Paused'}
              </p>
            </div>

            <div className="flex gap-3">
              <button
                onClick={toggleTimer}
                className="flex-1 py-3 bg-violet-600 hover:bg-violet-700 text-white font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
              >
                {isRunning ? (
                  <>
                    <Pause className="w-5 h-5" />
                    Pause
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    Resume
                  </>
                )}
              </button>
              
              <button
                onClick={resetTimer}
                className="flex-1 py-3 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
              >
                <RotateCcw className="w-5 h-5" />
                Reset
              </button>
            </div>

            <button
              onClick={stopTimer}
              className="w-full py-3 bg-red-500 hover:bg-red-600 text-white font-medium rounded-lg transition-colors"
            >
              Stop & Close
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

// ✅ NEW: Notes Button
const NotesButton: React.FC<{ onClick: () => void }> = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="w-full px-5 py-4 rounded-lg transition-colors duration-200 text-lg text-gray-400 hover:bg-gray-700 hover:text-white flex items-center"
      title="My Notes"
    >
      <div className="w-10 h-10 flex items-center justify-center bg-amber-600 rounded rotate-45">
        <StickyNote className="w-6 h-6 text-white -rotate-45" />
      </div>
      <span className="font-medium ml-3">My Notes</span>
    </button>
  );
};

// ✅ NEW: Notes Page Component
const NotesPage: React.FC = () => {
  const [notes, setNotes] = useState<Note[]>([]);
  const [isCreating, setIsCreating] = useState(false);
  const [editingNote, setEditingNote] = useState<Note | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    subject: 'General'
  });

  // Load notes from backend on mount
  useEffect(() => {
    const fetchNotes = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/notes/user/1`); // userId = 1
        if (response.ok) {
          const data = await response.json();
          setNotes(data.map((note: any) => ({
            ...note,
            createdAt: new Date(note.createdAt),
            updatedAt: new Date(note.updatedAt)
          })));
        }
      } catch (error) {
        console.error('Failed to fetch notes:', error);
        // Fallback to localStorage
        const savedNotes = localStorage.getItem('studyNotes');
        if (savedNotes) {
          const parsed = JSON.parse(savedNotes);
          setNotes(parsed.map((note: any) => ({
            ...note,
            createdAt: new Date(note.createdAt),
            updatedAt: new Date(note.updatedAt)
          })));
        }
      }
    };
    fetchNotes();
  }, []);

  const subjects = ['General', 'Math', 'Physics', 'Chemistry', 'Biology', 'DSA', 'OOPS', 'OS', 'AIML'];

  const handleCreateNote = async () => {
    if (!formData.title.trim() || !formData.content.trim()) {
      alert('Please fill in both title and content!');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/notes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: 1,
          title: formData.title,
          content: formData.content,
          subject: formData.subject
        })
      });

      if (response.ok) {
        const newNote = await response.json();
        setNotes([{
          ...newNote,
          createdAt: new Date(newNote.createdAt),
          updatedAt: new Date(newNote.updatedAt)
        }, ...notes]);
        setFormData({ title: '', content: '', subject: 'General' });
        setIsCreating(false);
      } else {
        throw new Error('Failed to create note');
      }
    } catch (error) {
      console.error('Failed to create note:', error);
      // Fallback to localStorage
      const newNote: Note = {
        id: Date.now().toString(),
        title: formData.title,
        content: formData.content,
        subject: formData.subject,
        createdAt: new Date(),
        updatedAt: new Date()
      };
      setNotes([newNote, ...notes]);
      localStorage.setItem('studyNotes', JSON.stringify([newNote, ...notes]));
      setFormData({ title: '', content: '', subject: 'General' });
      setIsCreating(false);
      alert('Backend unavailable. Note saved locally.');
    }
  };

  const handleUpdateNote = async () => {
    if (!editingNote || !formData.title.trim() || !formData.content.trim()) {
      alert('Please fill in both title and content!');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/notes/${editingNote.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: formData.title,
          content: formData.content,
          subject: formData.subject
        })
      });

      if (response.ok) {
        const updated = await response.json();
        setNotes(notes.map(note => 
          note.id === editingNote.id 
            ? { ...updated, createdAt: new Date(updated.createdAt), updatedAt: new Date(updated.updatedAt) }
            : note
        ));
        setFormData({ title: '', content: '', subject: 'General' });
        setEditingNote(null);
        setIsCreating(false);
      } else {
        throw new Error('Failed to update note');
      }
    } catch (error) {
      console.error('Failed to update note:', error);
      // Fallback to local update
      setNotes(notes.map(note => 
        note.id === editingNote.id 
          ? { ...note, ...formData, updatedAt: new Date() }
          : note
      ));
      localStorage.setItem('studyNotes', JSON.stringify(notes));
      setFormData({ title: '', content: '', subject: 'General' });
      setEditingNote(null);
      setIsCreating(false);
      alert('Backend unavailable. Note updated locally.');
    }
  };

  const handleDeleteNote = async (id: string) => {
    if (confirm('Are you sure you want to delete this note?')) {
      try {
        const response = await fetch(`${API_BASE_URL}/notes/${id}`, {
          method: 'DELETE'
        });

        if (response.ok) {
          setNotes(notes.filter(note => note.id !== id));
        } else {
          throw new Error('Failed to delete note');
        }
      } catch (error) {
        console.error('Failed to delete note:', error);
        // Fallback to local delete
        const updatedNotes = notes.filter(note => note.id !== id);
        setNotes(updatedNotes);
        localStorage.setItem('studyNotes', JSON.stringify(updatedNotes));
        alert('Backend unavailable. Note deleted locally.');
      }
    }
  };

  const startEdit = (note: Note) => {
    setEditingNote(note);
    setFormData({
      title: note.title,
      content: note.content,
      subject: note.subject
    });
    setIsCreating(true);
  };

  const cancelEdit = () => {
    setIsCreating(false);
    setEditingNote(null);
    setFormData({ title: '', content: '', subject: 'General' });
  };

  const formatDate = (date: Date) => {
    return new Date(date).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const subjectColors: Record<string, string> = {
    'General': 'bg-gray-500',
    'Math': 'bg-blue-500',
    'Physics': 'bg-purple-500',
    'Chemistry': 'bg-green-500',
    'Biology': 'bg-emerald-500',
    'DSA': 'bg-red-500',
    'OOPS': 'bg-orange-500',
    'OS': 'bg-yellow-600',
    'AIML': 'bg-pink-500'
  };

  return (
    <div className="p-10 bg-secondary min-h-full">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-5xl font-bold text-primary mb-2">My Study Notes</h1>
          <p className="text-2xl text-secondary">Keep track of important concepts and ideas</p>
        </div>
        <button
          onClick={() => setIsCreating(true)}
          className="flex items-center gap-2 px-6 py-3 bg-amber-600 hover:bg-amber-700 text-white font-semibold rounded-lg transition-colors"
        >
          <Plus className="w-5 h-5" />
          New Note
        </button>
      </div>

      {/* Note Editor Modal */}
      {isCreating && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-primary rounded-2xl shadow-2xl max-w-2xl w-full p-8 border border-primary">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-3xl font-bold text-primary flex items-center">
                <StickyNote className="w-8 h-8 mr-3 text-amber-600" />
                {editingNote ? 'Edit Note' : 'Create New Note'}
              </h2>
              <button
                onClick={cancelEdit}
                className="text-muted hover:text-primary transition-colors"
                title="Close"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-secondary font-medium mb-2">Subject</label>
                <select
                  value={formData.subject}
                  onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                  className="w-full px-4 py-3 bg-secondary border border-primary rounded-lg text-primary focus:outline-none focus:ring-2 focus:ring-amber-500"
                >
                  {subjects.map(subject => (
                    <option key={subject} value={subject}>{subject}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-secondary font-medium mb-2">Title</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="Enter note title..."
                  className="w-full px-4 py-3 bg-secondary border border-primary rounded-lg text-primary placeholder-muted focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>

              <div>
                <label className="block text-secondary font-medium mb-2">Content</label>
                <textarea
                  value={formData.content}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  placeholder="Write your notes here..."
                  rows={10}
                  className="w-full px-4 py-3 bg-secondary border border-primary rounded-lg text-primary placeholder-muted focus:outline-none focus:ring-2 focus:ring-amber-500 resize-none"
                />
              </div>

              <div className="flex gap-3">
                <button
                  onClick={editingNote ? handleUpdateNote : handleCreateNote}
                  className="flex-1 py-3 bg-amber-600 hover:bg-amber-700 text-white font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                  <Save className="w-5 h-5" />
                  {editingNote ? 'Update Note' : 'Save Note'}
                </button>
                <button
                  onClick={cancelEdit}
                  className="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-lg transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Notes Grid */}
      {notes.length === 0 ? (
        <div className="text-center py-20">
          <StickyNote className="w-24 h-24 mx-auto text-muted mb-4" />
          <p className="text-2xl text-secondary mb-2">No notes yet</p>
          <p className="text-muted">Click "New Note" to create your first study note!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {notes.map((note) => (
            <div
              key={note.id}
              className="bg-primary p-6 rounded-xl shadow-lg border border-primary hover:shadow-xl transition-shadow"
            >
              <div className="flex justify-between items-start mb-3">
                <span className={`px-3 py-1 ${subjectColors[note.subject]} text-white text-sm font-medium rounded-full`}>
                  {note.subject}
                </span>
                <div className="flex gap-2">
                  <button
                    onClick={() => startEdit(note)}
                    className="text-blue-500 hover:text-blue-700 transition-colors"
                    title="Edit"
                  >
                    <Edit className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => handleDeleteNote(note.id)}
                    className="text-red-500 hover:text-red-700 transition-colors"
                    title="Delete"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>

              <h3 className="text-xl font-bold text-primary mb-2 line-clamp-2">{note.title}</h3>
              <p className="text-secondary mb-4 line-clamp-4 whitespace-pre-wrap">{note.content}</p>
              
              <div className="text-xs text-muted pt-4 border-t border-primary">
                <div>Created: {formatDate(note.createdAt)}</div>
                {note.updatedAt.getTime() !== note.createdAt.getTime() && (
                  <div>Updated: {formatDate(note.updatedAt)}</div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};


const Sidebar: React.FC<{ 
  currentPage: Page; 
  setCurrentPage: (page: Page) => void; 
  theme: Theme;
  setTheme: (theme: Theme) => void;
  onLogout: () => void;
}> = ({ currentPage, setCurrentPage, theme, setTheme, onLogout }) => {
  const navItems = [
    { name: 'Dashboard', icon: LayoutDashboard, page: 'dashboard' },
    { name: 'Quizzes', icon: Brain, page: 'quizzes' },
    { name: 'Resources', icon: BookOpen, page: 'resources' },
    { name: 'Skilli (Bot)', icon: Bot, page: 'chatbot' },
  ] as const;

  return (
    <div className="flex flex-col w-72 h-screen p-5 bg-gray-900 text-white fixed shadow-2xl z-20">
      <div className="flex items-center mb-10 px-2 pt-4">
        <BookMarked className="w-10 h-10 mr-2 text-indigo-400" />
        <span className="text-2xl font-semibold">KnowWhereYouLack</span>
      </div>
      <nav className="flex-1 space-y-3">
        {navItems.map((item) => (
          <button
            key={item.name}
            onClick={() => setCurrentPage(item.page)}
            className={`flex items-center w-full px-5 py-4 rounded-lg transition-colors duration-200 text-lg ${
              currentPage === item.page
                ? 'bg-indigo-500 text-white shadow-lg'
                : 'text-gray-400 hover:bg-gray-700 hover:text-white'
            }`}
          >
            <item.icon className="w-6 h-6 mr-3" />
            <span className="font-medium">{item.name}</span>
          </button>
        ))}
      </nav>

      {/* ✅ CHANGE 2: Updated Sidebar bottom section */}
      <div className="mt-auto border-t border-gray-700 pt-4 space-y-3">
        {/* ✅ NOTES BUTTON - ABOVE TIMER */}
        <NotesButton onClick={() => setCurrentPage('notes')} />

        {/* ✅ TIMER BUTTON */}
        <TimerButton onClick={() => setCurrentPage('timer')} />

        {/* ✅ THEME TOGGLE */}
        <ThemeToggle theme={theme} setTheme={setTheme} />

        <button
          onClick={() => setCurrentPage('profile')}
          className={`flex items-center w-full px-5 py-4 rounded-lg transition-colors duration-200 text-lg ${
            currentPage === 'profile'
              ? 'bg-indigo-500 text-white shadow-lg'
              : 'text-gray-400 hover:bg-gray-700 hover:text-white'
          }`}
        >
          <User className="w-6 h-6 mr-3" />
          <span className="font-medium">Profile</span>
        </button>

        <button
          onClick={onLogout}
          className="flex items-center w-full px-5 py-4 rounded-lg transition-colors duration-200 text-lg text-gray-400 hover:bg-gray-700 hover:text-white"
        >
          <LogOut className="w-6 h-6 mr-3" />
          <span className="font-medium">Log Out</span>
        </button>
      </div>
    </div>
  );
};

const ThemeToggle: React.FC<{ theme: Theme; setTheme: (theme: Theme) => void; }> = ({ theme, setTheme }) => {
  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
  };

  return (
    <button
      onClick={toggleTheme}
      className="w-full px-5 py-4 rounded-lg transition-colors duration-200 text-lg text-gray-400 hover:bg-gray-700 hover:text-white flex items-center"
      title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
    >
      {theme === 'light' ? (
        <Moon className="w-6 h-6 mr-3" />
      ) : (
        <Sun className="w-6 h-6 mr-3" />
      )}
      <span className="font-medium">{theme === 'light' ? 'Dark' : 'Light'} Mode</span>
    </button>
  );
};


const DashboardView: React.FC<{ 
  userData: UserData;
  quizAccuracy: QuizAccuracy[];
  weeklyStreak: number;
}> = ({ userData, quizAccuracy: initialQuizAccuracy, weeklyStreak: initialWeeklyStreak }) => {
  const [weakTopics, setWeakTopics] = useState<WeakTopic[]>(MOCK_WEAK_TOPICS);
  const [quizAccuracy, setQuizAccuracy] = useState<QuizAccuracy[]>(initialQuizAccuracy);
  const [weeklyStreak, setWeeklyStreak] = useState(initialWeeklyStreak);
  const [totalQuizzes, setTotalQuizzes] = useState(0);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Fetch dashboard stats from backend
        const response = await fetch(`${API_BASE_URL}/analytics/dashboard/1`);
        if (response.ok) {
          const data = await response.json();
          setWeakTopics(data.weakTopics || MOCK_WEAK_TOPICS);
          setQuizAccuracy(data.recentAccuracy || initialQuizAccuracy);
          setWeeklyStreak(data.weeklyStreak || initialWeeklyStreak);
          setTotalQuizzes(data.totalQuizzes || 0);
          console.log('Dashboard data loaded from backend:', data);
        } else {
          console.log('Backend unavailable, using mock data');
        }
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
        // Fallback to initial/mock data
        setWeakTopics(MOCK_WEAK_TOPICS);
        setQuizAccuracy(initialQuizAccuracy);
        setWeeklyStreak(initialWeeklyStreak);
      }
    };

    fetchDashboardData();
  }, []);

  const overallProgress = quizAccuracy.length > 0 
    ? Math.round(quizAccuracy.reduce((acc, q) => acc + q.accuracy, 0) / quizAccuracy.length)
    : 0;
  
  const getWeakTopicColor = (score: number) => {
    if (score < 40) return 'bg-red-500';
    if (score < 70) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  return (
    <div className="p-10 grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-3 mb-5">
        <h1 className="text-5xl font-bold text-primary animate-fade-in-up">
          Welcome back, {userData.name}!
        </h1>
        <p className="text-2xl text-secondary mt-3 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
          Let's continue your learning journey.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:col-span-3 gap-8 mb-4">
        <div className="bg-primary p-8 rounded-xl shadow-lg border border-primary flex items-center animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
          <Flame className="w-16 h-16 text-red-500 mr-6" />
          <div>
            <div className="text-5xl font-bold text-primary">{weeklyStreak}</div>
            <div className="text-xl text-secondary font-medium mt-1">Day Streak</div>
          </div>
        </div>
        <div className="bg-primary p-8 rounded-xl shadow-lg border border-primary flex items-center animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
          <CheckCircle className="w-16 h-16 text-green-500 mr-6" />
          <div>
            <div className="text-5xl font-bold text-primary">{totalQuizzes > 0 ? totalQuizzes : quizAccuracy.length}</div>
            <div className="text-xl text-secondary font-medium mt-1">Quizzes Taken</div>
          </div>
        </div>
      </div>

      <div className="lg:col-span-2 bg-primary p-8 rounded-xl shadow-lg border border-primary animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
        <div className="flex items-center mb-5">
          <Target className="w-8 h-8 mr-3 text-red-500" />
          <h2 className="text-3xl font-semibold text-primary">Your Weakest Topics</h2>
        </div>
        <div className="space-y-5">
          {weakTopics.slice(0, 4).map((topic, index) => {
            const color = getWeakTopicColor(topic.currentScore);
            return (
              <div key={topic.topic} className="animate-fade-in-up" style={{ animationDelay: `${index * 0.05 + 0.1}s` }}>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-xl font-medium text-secondary">{topic.topic}</span>
                  <span className="text-xl font-bold text-muted">{topic.currentScore}%</span>
                </div>
                <div className="w-full bg-accent rounded-full h-4 overflow-hidden">
                  <div className={`h-4 rounded-full animate-progress-bar ${color}`} style={{ width: `${topic.currentScore}%`, animationDelay: `${index * 0.1}s` }}></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="bg-primary p-8 rounded-xl shadow-lg border border-primary flex flex-col items-center justify-center animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
        <div className="flex items-center mb-4 self-start">
          <TrendingUp className="w-8 h-8 mr-3 text-indigo-500" />
          <h2 className="text-3xl font-semibold text-primary">Overall Progress</h2>
        </div>
        <div className="relative flex items-center justify-center w-48 h-48 my-4">
          <div className="absolute inset-0 rounded-full animate-doughnut-spin" style={{
            background: `conic-gradient(from 0deg, #6366f1 0%, #6366f1 ${overallProgress}%, rgb(var(--bg-accent)) ${overallProgress}%, rgb(var(--bg-accent)) 100%)`,
          }}></div>
          <div className="absolute w-40 h-40 bg-primary rounded-full"></div>
          <span className="relative text-5xl font-bold text-indigo-700">
            {overallProgress}%
          </span>
        </div>
        <p className="mt-4 text-secondary font-medium text-center text-xl">
          You're doing great! Keep pushing forward.
        </p>
      </div>

      <div className="lg:col-span-3 bg-primary p-8 rounded-xl shadow-lg border border-primary animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
        <div className="flex items-center mb-5">
          <BarChart className="w-8 h-8 mr-3 text-green-500" />
          <h2 className="text-3xl font-semibold text-primary">Recent Quiz Accuracy</h2>
        </div>
        <div className="flex justify-around items-end h-64">
          {quizAccuracy.slice(-6).map((quiz, index) => (
            <div key={quiz.name} className="flex flex-col items-center w-16">
              <div 
                className="w-12 bg-green-500 rounded-t-lg animate-bar-grow" 
                style={{ 
                  height: `${quiz.accuracy}%`, 
                  animationDelay: `${index * 0.1}s` 
                }}
                title={`Accuracy: ${quiz.accuracy}%`}
              ></div>
              <span className="mt-3 text-sm font-medium text-muted">{quiz.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const QuizView: React.FC<{ 
  onQuizComplete: (score: number, total: number) => void;
}> = ({ onQuizComplete }) => {
  const [topics] = useState<Topic[]>(MOCK_TOPICS);
  const [selectedTopic, setSelectedTopic] = useState<Topic | null>(null);
  const [selectedDifficulty, setSelectedDifficulty] = useState<'EASY' | 'MEDIUM' | 'HARD'>('MEDIUM');
  const [quiz, setQuiz] = useState<Question[] | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<{ [key: string]: string }>({});
  const [isFinished, setIsFinished] = useState(false);
  const [finalScore, setFinalScore] = useState(0);
  const [loading, setLoading] = useState(false);
  const [topicToStart, setTopicToStart] = useState<{ topic: Topic, count: number } | null>(null);

  // Fetch topics from backend on mount
  useEffect(() => {
    fetchTopicsFromBackend();
  }, []);

  const fetchTopicsFromBackend = async () => {
    try {
      const backendTopics = await quizApi.getAllTopics();
      console.log('✅ Fetched topics from backend:', backendTopics);
    } catch (error) {
      console.error('❌ Failed to fetch topics from backend:', error);
      console.log('📝 Using mock topics as fallback');
    }
  };

  const startQuiz = async (topicId: number) => {
    const topic = topics.find(t => t.id === topicId);
    if (!topic) return;
    
    setTopicToStart(null);
    setLoading(true);
    setSelectedTopic(topic);
    
    try {
      // ✅ Use quizApi service to fetch questions
      console.log(`🚀 Fetching ${selectedDifficulty} questions for topic ${topicId}...`);
      const quizData = await quizApi.getQuestionsByDifficulty(topicId, selectedDifficulty);
      
      // Transform backend questions to frontend format
      const transformedQuestions: Question[] = quizData.questions?.map((q) => ({
        id: q.questionId?.toString(),
        text: q.questionText,
        topic: topic.name,
        options: [
          { id: 'A', text: 'Option A' },
          { id: 'B', text: 'Option B' },
          { id: 'C', text: 'Option C' },
          { id: 'D', text: 'Option D' }
        ],
        correctOptionId: q.correctAnswer || 'A'
      })) || [];
      
      if (transformedQuestions.length > 0) {
        setQuiz(transformedQuestions);
        console.log(`✅ Loaded ${transformedQuestions.length} questions from backend`);
      } else {
        console.warn('⚠️ No questions returned from backend, using mock data');
        const mockQuestions = MOCK_QUIZ.filter(q => q.topic === topic.name).slice(0, 10);
        setQuiz(mockQuestions);
      }
    } catch (error) {
      console.error('❌ Failed to fetch questions from backend:', error);
      // Fallback to mock data
      const mockQuestions = MOCK_QUIZ.filter(q => q.topic === topic.name).sort(() => 0.5 - Math.random());
      setQuiz(mockQuestions.slice(0, 10));
      console.log('📝 Using mock data as fallback');
    }
    
    setCurrentQuestionIndex(0);
    setAnswers({});
    setIsFinished(false);
    setFinalScore(0);
    setLoading(false);
  };

  // Handle difficulty change - reload quiz if already started
  const handleDifficultyChange = async (newDifficulty: 'EASY' | 'MEDIUM' | 'HARD') => {
    setSelectedDifficulty(newDifficulty);
    
    // If a quiz is already started, reload questions with new difficulty
    if (selectedTopic && !isFinished) {
      console.log(`🔄 Reloading quiz with ${newDifficulty} difficulty...`);
      await startQuiz(selectedTopic.id);
    }
  };

  const handleAnswer = (questionId: string, optionId: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: optionId }));
  };

  const handleNext = () => {
    if (quiz && currentQuestionIndex < quiz.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      handleSubmit();
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    await mockApi({}, 500);
    let score = 0;
    quiz?.forEach((q) => {
      if (answers[q.id] === q.correctOptionId) {
        score++;
      }
    });
    
    // Save quiz result to backend
    const total = quiz?.length || 0;
    try {
      await fetch(`${API_BASE_URL}/analytics/quiz-result`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: 1,
          topic: selectedTopic,
          score: score,
          totalQuestions: total
        })
      });
      console.log('Quiz result saved to backend');
    } catch (error) {
      console.error('Failed to save quiz result:', error);
    }
    
    setFinalScore(score);
    setIsFinished(true);
    setLoading(false);
  };

  if (loading && !quiz) {
    return (
      <div className="flex items-center justify-center h-full bg-secondary">
        <Loader2 className="w-12 h-12 animate-spin text-indigo-600" />
      </div>
    );
  }

  if (isFinished) {
    return (
      <div className="p-10 max-w-2xl mx-auto text-center bg-secondary min-h-full">
        <CheckCircle className="w-24 h-24 text-green-600 mx-auto mb-6" />
        <h1 className="text-4xl font-bold text-primary mb-4">Quiz Complete!</h1>
        <p className="text-2xl text-secondary mb-8">
          You scored {finalScore} out of {quiz?.length || 0}
        </p>
        <button
          onClick={() => {
            onQuizComplete(finalScore, quiz?.length || 0);
          }}
          className="px-8 py-4 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition-colors text-xl"
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  if (quiz) {
    if (quiz.length === 0) {
      return (
        <div className="p-10 text-center bg-secondary min-h-full">
          <h2 className="text-2xl font-bold text-primary mb-6">No questions available for this topic yet.</h2>
          <button
            onClick={() => {
              setQuiz(null);
              setSelectedTopic(null);
            }}
            className="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition-colors text-lg"
          >
            Back to Topics
          </button>
        </div>
      );
    }

    const currentQuestion = quiz[currentQuestionIndex];
    return (
      <div className="p-10 max-w-4xl mx-auto bg-secondary min-h-full">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-4xl font-bold text-primary">{selectedTopic?.name} Quiz</h1>
          <span className="text-xl font-medium text-muted">
            Question {currentQuestionIndex + 1} / {quiz.length}
          </span>
        </div>
        <div className="bg-primary p-8 rounded-xl shadow-lg border border-primary animate-fade-in">
          <p className="text-3xl font-semibold text-primary mb-8">
            {currentQuestion.text}
          </p>
          <div className="space-y-4">
            {currentQuestion.options.map((option) => (
              <button
                key={option.id}
                onClick={() => handleAnswer(currentQuestion.id, option.id)}
                className={`block w-full text-left p-5 rounded-lg border-2 transition-all text-xl font-medium ${
                  answers[currentQuestion.id] === option.id
                    ? 'bg-indigo-600 border-indigo-600 text-white'
                    : 'bg-accent border-accent text-secondary hover:border-indigo-400 hover:bg-indigo-50'
                }`}
              >
                {option.text}
              </button>
            ))}
          </div>
          <div className="flex justify-end mt-10">
            <button
              onClick={handleNext}
              disabled={!answers[currentQuestion.id]}
              className="px-10 py-4 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition-colors text-xl disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {currentQuestionIndex === quiz.length - 1 ? 'Submit' : 'Next'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  const TopicCircle: React.FC<{ topic: Topic; onClick: () => void }> = ({ topic, onClick }) => {
    const iconMap: { [key: string]: React.ReactNode } = {
      'Object-Oriented Programming': <Brain size={48} />,
      'Data Structures': <Terminal size={48} />,
      'Algorithms': <Target size={48} />,
      'Physics': <Atom size={48} />,
      'Chemistry': <FlaskConical size={48} />,
      'Operating Systems': <Server size={48} />,
      'Math': <Calculator size={48} />,
      'Biology': <Dna size={48} />,
      'AIML Basics': <Cpu size={48} />,
    };

    const colorMap: { [key: string]: string } = {
      'Object-Oriented Programming': 'from-blue-400 to-indigo-500',
      'Data Structures': 'from-green-400 to-emerald-500',
      'Algorithms': 'from-red-400 to-rose-500',
      'Physics': 'from-purple-400 to-violet-500',
      'Chemistry': 'from-yellow-400 to-amber-500',
      'Operating Systems': 'from-gray-400 to-gray-500',
      'Math': 'from-orange-400 to-red-500',
      'Biology': 'from-lime-400 to-green-500',
      'AIML Basics': 'from-cyan-400 to-sky-500',
    };

    const Icon = iconMap[topic.name] || <Brain size={48} />;
    const color = colorMap[topic.name] || 'from-indigo-400 to-blue-500';

    return (
      <button
        onClick={onClick}
        className={`flex flex-col items-center justify-center p-6 bg-gradient-to-br ${color} text-white rounded-full w-52 h-52 shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-all transform ease-in-out duration-300 cursor-pointer`}
      >
        <div className="mb-3">{Icon}</div>
        <span className="text-xl font-semibold text-center">{topic.name}</span>
      </button>
    );
  };
  
  const QuizStartModal: React.FC<{
    topicInfo: { topic: Topic, count: number };
    onStart: () => void;
    onCancel: () => void;
  }> = ({ topicInfo, onStart, onCancel }) => {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div className="bg-primary rounded-2xl shadow-2xl max-w-lg w-full p-10 border border-primary animate-fade-in-up">
          <button onClick={onCancel} className="absolute top-4 right-4 text-muted hover:text-primary">
            <X size={24} />
          </button>
          <h2 className="text-3xl font-bold text-primary mb-4">{topicInfo.topic.name}</h2>
          <p className="text-lg text-secondary mb-2">{topicInfo.topic.description}</p>
          <div className="flex items-center space-x-6 my-6">
            <span className="text-lg text-secondary">
              Difficulty: <span className="font-bold text-primary">{topicInfo.topic.difficulty}</span>
            </span>
            <span className="text-lg text-secondary">
              Questions: <span className="font-bold text-primary">{topicInfo.count > 10 ? '10' : topicInfo.count}</span>
            </span>
          </div>
          <button
            onClick={onStart}
            disabled={topicInfo.count === 0}
            className="w-full py-4 bg-indigo-600 text-white font-bold text-xl rounded-lg shadow-md hover:bg-indigo-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {topicInfo.count === 0 ? 'No Questions Yet' : 'Start Quiz'}
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="p-10 bg-secondary min-h-full">
      <h1 className="text-5xl font-bold text-primary mb-6">Choose a Topic</h1>
      
      {/* Difficulty Slider Component */}
      <DifficultySlider 
        selectedDifficulty={selectedDifficulty}
        onDifficultyChange={handleDifficultyChange}
      />

      <div className="flex flex-wrap gap-10 justify-center">
        {topics.map(topic => (
          <TopicCircle
            key={topic.id}
            topic={topic}
            onClick={() => {
              const qCount = MOCK_QUIZ.filter(q => q.topic === topic.name).length;
              setTopicToStart({ topic: topic, count: qCount });
            }}
          />
        ))}
      </div>
      {topicToStart && (
        <QuizStartModal
          topicInfo={topicToStart}
          onStart={() => startQuiz(topicToStart.topic.id)}
          onCancel={() => setTopicToStart(null)}
        />
      )}
    </div>
  );
};

const ResourcesView: React.FC = () => {
  const [resources] = useState<Resource[]>(MOCK_RESOURCES);
  return (
    <div className="p-10 bg-secondary min-h-full">
      <h1 className="text-5xl font-bold text-primary mb-10">Recommended Resources</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {resources.map((resource) => (
          <div key={resource.id} className="bg-primary rounded-xl shadow-lg border border-primary overflow-hidden flex flex-col hover:shadow-2xl transition-all">
            <div className="p-8 flex-1">
              <span className="inline-block bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300 text-sm font-semibold px-3 py-1 rounded-full mb-3">
                {resource.topic}
              </span>
              <h3 className="text-3xl font-bold text-primary mb-3">{resource.title}</h3>
              <div className="flex items-center text-lg text-muted space-x-4">
                <span className="capitalize">{resource.type}</span>
                <span>•</span>
                <span>{resource.estimatedTime}</span>
              </div>
            </div>
            <a
              href={resource.link}
              target="_blank"
              rel="noopener noreferrer"
              className="block bg-accent text-center py-4 text-lg font-semibold text-indigo-600 hover:bg-indigo-100 dark:hover:bg-indigo-900 transition-colors"
            >
              View Resource
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

const ChatbotView: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'bot', content: "Hi! I'm Skilli. I'm here to help you understand complex topics. Ask me anything!" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async () => {
    const apiUrl = `${API_BASE_URL}/chatbot/message`;
    if (!input.trim() || isLoading) return;
    const userMessage: ChatMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Send a simple payload to the backend. The backend composes the request
    // to GROQ/Gemini (keeps the API key secret) and enforces safety/education checks.
    const payload = { message: input };

    try {
      const response = await fetchWithBackoff(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const result = await response.json(); // Backend returns { reply: string }
      const botResponse = (result && result.reply) ?
        result.reply :
        "I'm sorry, I couldn't get a response. Please try again.";
        
      setMessages((prev) => [
        ...prev,
        { role: 'bot', content: botResponse },
      ]);
    } catch (error) {
      console.error('Error calling Gemini API:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'bot', content: "Sorry, I'm having trouble connecting right now. Please try again in a moment." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-10 h-full flex flex-col bg-secondary">
      <h1 className="text-5xl font-bold text-primary mb-10">Skilli (AI Bot)</h1>
      <div className="flex-1 bg-primary border border-primary rounded-xl shadow-lg flex flex-col overflow-hidden">
        <div className="flex-1 p-8 space-y-6 overflow-y-auto">
          {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              {msg.role === 'bot' && (
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center mr-4 flex-shrink-0">
                  <Bot className="w-6 h-6 text-white" />
                </div>
              )}
              <div
                className={`max-w-xl p-5 rounded-2xl shadow ${
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white rounded-br-lg'
                    : 'bg-accent text-secondary rounded-bl-lg'
                }`}
              >
                <p className="text-lg leading-relaxed">{msg.content}</p>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center mr-4 flex-shrink-0">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div className="max-w-xl p-5 rounded-2xl shadow bg-accent text-secondary rounded-bl-lg">
                <Loader2 className="w-6 h-6 animate-spin text-indigo-600" />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <div className="border-t border-primary p-6 bg-primary">
          <div className="flex items-center bg-accent rounded-lg">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask Skilli anything..."
              className="flex-1 bg-transparent p-5 text-lg text-primary placeholder-muted focus:outline-none"
              disabled={isLoading}
            />
            <button
              onClick={handleSend}
              disabled={isLoading || !input.trim()}
              className="p-5 text-indigo-600 hover:text-indigo-800 disabled:text-gray-400 transition-colors"
            >
              {isLoading ? (
                <Loader2 className="w-6 h-6 animate-spin" />
              ) : (
                <Send className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const ProfileView: React.FC<{ userData: UserData }> = ({ userData }) => {
  return (
    <div className="p-10 bg-secondary min-h-full">
      <h1 className="text-5xl font-bold text-primary mb-10">Your Profile</h1>
      <div className="bg-primary max-w-2xl p-10 rounded-xl shadow-lg border border-primary">
        <div className="flex items-center space-x-6 mb-8">
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center">
            <span className="text-4xl font-bold text-white">
              {userData?.name?.charAt(0).toUpperCase() || 'S'}
            </span>
          </div>
          <div>
            <h2 className="text-4xl font-bold text-primary">{userData.name}</h2>
            <p className="text-xl text-muted mt-1">{userData.email}</p>
          </div>
        </div>
        <div className="space-y-6">
          <div>
            <label className="text-lg font-medium text-secondary">Full Name</label>
            <input
              type="text"
              value={userData.name}
              disabled
              className="w-full p-4 mt-2 bg-accent rounded-lg text-lg text-primary border border-primary"
            />
          </div>
          <div>
            <label className="text-lg font-medium text-secondary">Email Address</label>
            <input
              type="email"
              value={userData.email}
              disabled
              className="w-full p-4 mt-2 bg-accent rounded-lg text-lg text-primary border border-primary"
            />
          </div>
          <button
            className="w-full py-4 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition-colors text-xl"
            onClick={() => alert('Edit profile functionality not implemented.')}
          >
            Edit Profile (Coming Soon)
          </button>
        </div>
      </div>
    </div>
  );
};

// --- Floating Skilli Component ---

const FloatingSkilli: React.FC<{ onClick: () => void }> = ({ onClick }) => {
  return (
    <div 
      onClick={onClick}
      className="fixed bottom-8 right-8 z-50 cursor-pointer animate-skilli-jump hover:scale-110 transition-transform duration-300 group"
      title="Chat with Skilli!"
    >
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full blur-xl opacity-75 group-hover:opacity-100 transition-opacity"></div>
        <img 
          src="/image.jpg" 
          alt="Skilli Bot" 
          className="relative w-24 h-24 rounded-full border-4 border-white shadow-2xl object-cover"
        />
        <div className="absolute -top-2 -right-2 w-6 h-6 bg-green-500 rounded-full border-2 border-white animate-pulse"></div>
      </div>
    </div>
  );
};

// --- Main App Component ---

const App: React.FC = () => {
  // ✅ ADD: Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  
  const [currentPage, setCurrentPage] = useState<string>('dashboard');
  const [theme, setTheme] = useState<Theme>('light');
  
  // ✅ CHANGE: Get userData from localStorage instead of mock
  const [userData, setUserData] = useState<UserData>(() => {
    const saved = localStorage.getItem('user_data');
    return saved ? JSON.parse(saved) : MOCK_USER_DATA;
  });
  
  const [quizAccuracy, setQuizAccuracy] = useState<QuizAccuracy[]>(INITIAL_QUIZ_ACCURACY);
  const [weeklyStreak, setWeeklyStreak] = useState<number>(INITIAL_WEEKLY_STREAK);

  // ✅ ADD: Check authentication on mount
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('jwt_token');
      const savedUser = localStorage.getItem('user_data');
      
      if (token && savedUser) {
        try {
          // Verify token is still valid
          const response = await axios.get(`${API_BASE_URL}/auth/me`);
          setUserData(response.data);
          setIsAuthenticated(true);
        } catch (error) {
          console.error('Token invalid, logging out:', error);
          handleLogout();
        }
      }
      setIsCheckingAuth(false);
    };
    
    checkAuth();
  }, []);

  useEffect(() => {
    document.documentElement.className = theme;
  }, [theme]);
  
  // ✅ ADD: Login handler
  const handleLoginSuccess = (user: UserData & { token: string }) => {
    setUserData({
      userId: user.userId,
      name: user.name,
      email: user.email
    });
    setIsAuthenticated(true);
    console.log('✅ User logged in:', user);
  };

  // ✅ ADD: Logout handler
  const handleLogout = () => {
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user_data');
    setIsAuthenticated(false);
    setUserData(MOCK_USER_DATA);
    setCurrentPage('dashboard');
  };
  
  const handleQuizComplete = (score: number, total: number) => {
    const newAccuracy = total > 0 ? (score / total) * 100 : 0;
    
    setQuizAccuracy(prevAccuracy => [
      ...prevAccuracy.slice(-5),
      { name: `Quiz ${prevAccuracy.length + 1}`, accuracy: newAccuracy }
    ]);

    setWeeklyStreak(prevStreak => prevStreak + 1);
    
    setCurrentPage('dashboard');
  };

  // ✅ ADD: Show loading while checking auth
  if (isCheckingAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <Loader2 className="w-12 h-12 animate-spin text-indigo-600" />
      </div>
    );
  }

  // ✅ ADD: Show login page if not authenticated
  if (!isAuthenticated) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <>
      <GlobalStyles />
      <div className={`flex min-h-screen ${theme}`}>
        <Sidebar 
          currentPage={currentPage as Page} 
          setCurrentPage={setCurrentPage}
          theme={theme}
          setTheme={setTheme}
          onLogout={handleLogout}
        />
        <main className="flex-1 ml-72 h-screen overflow-y-auto bg-secondary">
          {currentPage === 'dashboard' && (
            <DashboardView 
              userData={userData} 
              quizAccuracy={quizAccuracy} 
              weeklyStreak={weeklyStreak} 
            />
          )}
          {currentPage === 'quizzes' && (
            <QuizView 
              onQuizComplete={handleQuizComplete} 
            />
          )}
          {currentPage === 'resources' && <ResourcesView />}
          {currentPage === 'chatbot' && <ChatbotView />}
          {currentPage === 'profile' && <ProfileView userData={userData} />}
          {currentPage === 'notes' && <NotesPage />}
        </main>
        
        {/* ✅ CHANGE 5: Added Timer Page Modal */}
        {currentPage === 'timer' && (
          <TimerPage onClose={() => setCurrentPage('dashboard')} />
        )}
        
        {/* ✅ Floating Skilli - Always visible on all pages */}
        <FloatingSkilli onClick={() => setCurrentPage('chatbot')} />
      </div>
    </>
  );
};

export default App;