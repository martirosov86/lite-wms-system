import { createSlice } from '@reduxjs/toolkit';
import axios from 'axios';
import jwtDecode from 'jwt-decode';

const initialState = {
  token: localStorage.getItem('token'),
  refreshToken: localStorage.getItem('refreshToken'),
  isAuthenticated: false,
  user: null,
  loading: false,
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    loginSuccess: (state, action) => {
      state.loading = false;
      state.isAuthenticated = true;
      state.token = action.payload.access;
      state.refreshToken = action.payload.refresh;
      state.user = jwtDecode(action.payload.access);
      localStorage.setItem('token', action.payload.access);
      localStorage.setItem('refreshToken', action.payload.refresh);
    },
    loginFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    logout: (state) => {
      state.isAuthenticated = false;
      state.token = null;
      state.refreshToken = null;
      state.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
    },
  },
});

export const { loginStart, loginSuccess, loginFailure, logout } = authSlice.actions;

export const login = (email, password) => async (dispatch) => {
  try {
    dispatch(loginStart());
    const response = await axios.post('/api/token/', { email, password });
    dispatch(loginSuccess(response.data));
  } catch (error) {
    dispatch(loginFailure(error.response?.data?.detail || 'Ошибка авторизации'));
  }
};

export default authSlice.reducer;
