import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  sidebarOpen: true,
  loading: false,
  notification: null,
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    showNotification: (state, action) => {
      state.notification = {
        message: action.payload.message,
        type: action.payload.type || 'info',
      };
    },
    clearNotification: (state) => {
      state.notification = null;
    },
  },
});

export const { toggleSidebar, setLoading, showNotification, clearNotification } = uiSlice.actions;

export default uiSlice.reducer;
