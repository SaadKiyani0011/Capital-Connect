import React, { createContext, useState, useContext, useEffect } from 'react';
import { User, UserRole, AuthContextType } from '../types';
import toast from 'react-hot-toast';
import api from '../api/axiosConfig';

// Create Auth Context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Local storage keys
const USER_STORAGE_KEY = 'business_nexus_user';
const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

// Auth Provider Component
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const mapBackendUserToFrontend = (data: any): User => {
    // If data comes from profile endpoint, user info is nested under 'user'
    const userInfo = data.user || data;
    return {
      id: String(userInfo.id),
      name: userInfo.username,
      email: userInfo.email,
      role: userInfo.role as UserRole,
      avatarUrl: userInfo.avatarUrl || `https://ui-avatars.com/api/?name=${encodeURIComponent(userInfo.username)}&background=random`,
      bio: userInfo.bio || '',
      isOnline: userInfo.isOnline || false,
      createdAt: userInfo.date_joined || new Date().toISOString()
    };
  };

  // Fetch current user from API if token exists
  const fetchCurrentUser = async () => {
    try {
      const response = await api.get('/accounts/profile/');
      const mappedUser = mapBackendUserToFrontend(response.data);
      setUser(mappedUser);
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(mappedUser));
    } catch (error) {
      console.error('Failed to fetch user profile:', error);
      logout();
    }
  };

  // Check for stored user on initial load
  useEffect(() => {
    const storedToken = localStorage.getItem(ACCESS_TOKEN_KEY);
    const storedUser = localStorage.getItem(USER_STORAGE_KEY);
    
    if (storedToken && storedUser) {
      setUser(JSON.parse(storedUser));
      fetchCurrentUser();
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (email: string, password: string, role: UserRole): Promise<void> => {
    setIsLoading(true);
    try {
      // Backend expects username by default, we'll send email as username
      const response = await api.post('/accounts/login/', { username: email, password });
      
      const { access, refresh } = response.data;
      localStorage.setItem(ACCESS_TOKEN_KEY, access);
      localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
      
      // Fetch user profile after successful login
      const profileResponse = await api.get('/accounts/profile/');
      const userData = mapBackendUserToFrontend(profileResponse.data);
      
      setUser(userData);
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(userData));
      toast.success('Successfully logged in!');
    } catch (error: any) {
      const msg = error.response?.data?.detail || 'Invalid credentials or server error';
      toast.error(msg);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (name: string, email: string, password: string, role: UserRole): Promise<void> => {
    setIsLoading(true);
    try {
      // Using email as username to ensure uniqueness and match login logic
      await api.post('/accounts/register/', { 
        username: email,
        email: email,
        password: password,
        role: role
      });
      
      // Auto login after registration
      await login(email, password, role);
      toast.success('Account created successfully!');
    } catch (error: any) {
      const msg = error.response?.data?.username?.[0] || error.response?.data?.email?.[0] || 'Registration failed';
      toast.error(msg);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const forgotPassword = async (email: string): Promise<void> => {
    toast.error("Forgot password not implemented in backend yet");
  };

  const resetPassword = async (token: string, newPassword: string): Promise<void> => {
    toast.error("Reset password not implemented in backend yet");
  };

  const logout = (): void => {
    setUser(null);
    localStorage.removeItem(USER_STORAGE_KEY);
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    toast.success('Logged out successfully');
  };

  const updateProfile = async (userId: string, updates: Partial<User>): Promise<void> => {
    try {
      if (!user) throw new Error("Not logged in");
      
      // We only update the basic User fields via the backend's CustomUser update capability if needed,
      // Or we can patch the specific profile. Since we don't have a direct /update/ endpoint for CustomUser,
      // we'll patch the profile.
      const endpoint = user.role === 'entrepreneur' ? '/accounts/profile/entrepreneur/' : '/accounts/profile/investor/';
      
      // Assuming updates contains profile specific fields. 
      await api.patch(endpoint, updates);
      
      // Re-fetch user profile to sync state
      await fetchCurrentUser();
      toast.success('Profile updated successfully');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to update profile');
      throw error;
    }
  };

  const value = {
    user,
    login,
    register,
    logout,
    forgotPassword,
    resetPassword,
    updateProfile,
    isAuthenticated: !!user,
    isLoading
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};