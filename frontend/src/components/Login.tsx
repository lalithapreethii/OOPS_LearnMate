import React, { useState } from 'react';
import { BookMarked, Mail, Lock, Loader2, Eye, EyeOff } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8082/api';

interface LoginProps {
  onLoginSuccess: (userData: { userId: number; name: string; email: string; token: string }) => void;
}

const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isRegisterMode, setIsRegisterMode] = useState(false);
  
  // Registration fields
  const [username, setUsername] = useState('');
  const [fullName, setFullName] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // Step 1: Login to get JWT token
      const loginResponse = await axios.post(`${API_BASE_URL}/auth/login`, {
        email: email.toLowerCase().trim(),
        password: password
      });

      const { token } = loginResponse.data;

      if (!token) {
        throw new Error('No token received from server');
      }

      // Step 2: Get user details using the token
      const meResponse = await axios.get(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const userData = meResponse.data;

      // Step 3: Store token and call success callback
      localStorage.setItem('jwt_token', token);
      localStorage.setItem('user_data', JSON.stringify(userData));

      onLoginSuccess({
        userId: userData.userId,
        name: userData.name,
        email: userData.email,
        token: token
      });

      console.log('✅ Login successful:', userData);
    } catch (err: any) {
      console.error('❌ Login failed:', err);
      
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else if (err.response?.status === 401) {
        setError('Invalid email or password');
      } else if (err.response?.status === 404) {
        setError('User not found');
      } else {
        setError('Login failed. Please check your credentials and try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // Step 1: Register new user
      const registerResponse = await axios.post(`${API_BASE_URL}/auth/register`, {
        username: username.trim(),
        fullName: fullName.trim(),
        email: email.toLowerCase().trim(),
        password: password
      });

      console.log('✅ Registration successful:', registerResponse.data);

      // Step 2: Auto-login after registration
      const loginResponse = await axios.post(`${API_BASE_URL}/auth/login`, {
        email: email.toLowerCase().trim(),
        password: password
      });

      const { token } = loginResponse.data;

      // Step 3: Get user details
      const meResponse = await axios.get(`${API_BASE_URL}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const userData = meResponse.data;

      // Step 4: Store token and call success callback
      localStorage.setItem('jwt_token', token);
      localStorage.setItem('user_data', JSON.stringify(userData));

      onLoginSuccess({
        userId: userData.userId,
        name: userData.name,
        email: userData.email,
        token: token
      });

    } catch (err: any) {
      console.error('❌ Registration failed:', err);
      
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else if (err.response?.status === 400) {
        setError('Invalid input. Please check all fields.');
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
        {/* Logo & Title */}
        <div className="flex flex-col items-center mb-8">
          <BookMarked className="w-16 h-16 text-indigo-600 mb-3" />
          <h1 className="text-3xl font-bold text-gray-800">KnowWhereYouLack</h1>
          <p className="text-gray-600 mt-2">
            {isRegisterMode ? 'Create your account' : 'Welcome back!'}
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {/* Login/Register Form */}
        <form onSubmit={isRegisterMode ? handleRegister : handleLogin} className="space-y-4">
          {isRegisterMode && (
            <>
              {/* Username Field */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Username
                </label>
                <div className="relative">
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter username"
                    required
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  />
                  <Mail className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
                </div>
              </div>

              {/* Full Name Field */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name
                </label>
                <div className="relative">
                  <input
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Enter full name"
                    required
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  />
                  <Mail className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
                </div>
              </div>
            </>
          )}

          {/* Email Field */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <div className="relative">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
              <Mail className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
            </div>
          </div>

          {/* Password Field */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
                minLength={6}
                className="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
              <Lock className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-3.5 text-gray-400 hover:text-gray-600"
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                {isRegisterMode ? 'Creating Account...' : 'Logging in...'}
              </>
            ) : (
              isRegisterMode ? 'Create Account' : 'Login'
            )}
          </button>
        </form>

        {/* Toggle Register/Login */}
        <div className="mt-6 text-center">
          <button
            onClick={() => {
              setIsRegisterMode(!isRegisterMode);
              setError('');
              setUsername('');
              setFullName('');
              setEmail('');
              setPassword('');
            }}
            className="text-indigo-600 hover:text-indigo-800 font-medium"
          >
            {isRegisterMode 
              ? 'Already have an account? Login' 
              : "Don't have an account? Register"}
          </button>
        </div>

        {/* Demo Credentials */}
        <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <p className="text-xs text-gray-600 font-medium mb-2">Demo Credentials:</p>
          <p className="text-xs text-gray-500">Email: demo@student.com</p>
          <p className="text-xs text-gray-500">Password: demo123</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
