import axios from 'axios';

const API_BASE_URL = 'http://localhost:8082/api/quiz';

export interface Topic {
  topicId: number;
  topicName: string;
  difficultyLevel: string;
  description: string;
  questionCount: number;
}

export interface Question {
  questionId: number;
  topicId: number;
  questionText: string;
  questionType: string;
  difficultyLevel: string;
  correctAnswer: string;
  explanation: string;
  isActive: boolean;
}

export interface QuizResponseDto {
  topicId: number;
  topicName: string;
  description: string;
  difficultyLevel: string;
  questions: Question[];
}

export const quizApi = {
  // Get all topics with question counts
  getAllTopics: async (): Promise<Topic[]> => {
    try {
      const response = await axios.get<Topic[]>(`${API_BASE_URL}/topics`);
      return response.data;
    } catch (error) {
      console.error('Error fetching topics:', error);
      throw error;
    }
  },

  // Get questions by topic and difficulty
  getQuestionsByDifficulty: async (
    topicId: number,
    difficulty: string,
    userId?: number
  ): Promise<QuizResponseDto> => {
    try {
      const url = userId 
        ? `${API_BASE_URL}/${topicId}/difficulty/${difficulty}?userId=${userId}`
        : `${API_BASE_URL}/${topicId}/difficulty/${difficulty}`;
      
      const response = await axios.get<QuizResponseDto>(url);
      return response.data;
    } catch (error) {
      console.error('Error fetching questions by difficulty:', error);
      throw error;
    }
  },

  // Get all questions for a topic
  getAllQuestions: async (topicId: number): Promise<Question[]> => {
    try {
      const response = await axios.get<Question[]>(
        `${API_BASE_URL}/${topicId}/questions`
      );
      return response.data;
    } catch (error) {
      console.error('Error fetching all questions:', error);
      throw error;
    }
  },

  // Submit quiz attempt
  submitQuiz: async (quizData: {
    userId: number;
    topicId: number;
    score: number;
    totalQuestions: number;
    timeTaken: number;
    answers: { questionId: number; selectedAnswer: string }[];
  }): Promise<any> => {
    try {
      const response = await axios.post(`${API_BASE_URL}/submit`, quizData);
      return response.data;
    } catch (error) {
      console.error('Error submitting quiz:', error);
      throw error;
    }
  },
};
