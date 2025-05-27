import axios from 'axios';

// Создаем экземпляр axios с базовым URL
const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
});

// Интерцептор для добавления токена авторизации
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Интерцептор для обработки ошибок и обновления токена
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Если ошибка 401 и запрос не на обновление токена
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        const response = await axios.post('http://localhost:8000/api/token/refresh/', {
          refresh: refreshToken,
        });
        
        const { access } = response.data;
        localStorage.setItem('token', access);
        
        // Повторяем оригинальный запрос с новым токеном
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Если не удалось обновить токен, выходим из системы
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// API для работы с пользователями
export const userService = {
  getCurrentUser: () => api.get('users/me/'),
  updateProfile: (data) => api.patch('users/me/', data),
};

// API для работы с компаниями
export const companyService = {
  getCompanies: () => api.get('companies/'),
  getCompany: (id) => api.get(`companies/${id}/`),
  createCompany: (data) => api.post('companies/', data),
  updateCompany: (id, data) => api.patch(`companies/${id}/`, data),
  deleteCompany: (id) => api.delete(`companies/${id}/`),
};

// API для работы со складами
export const warehouseService = {
  getWarehouses: () => api.get('warehouses/'),
  getWarehouse: (id) => api.get(`warehouses/${id}/`),
  createWarehouse: (data) => api.post('warehouses/', data),
  updateWarehouse: (id, data) => api.patch(`warehouses/${id}/`, data),
  deleteWarehouse: (id) => api.delete(`warehouses/${id}/`),
};

// API для работы с товарами
export const productService = {
  getProducts: () => api.get('products/'),
  getProduct: (id) => api.get(`products/${id}/`),
  createProduct: (data) => api.post('products/', data),
  updateProduct: (id, data) => api.patch(`products/${id}/`, data),
  deleteProduct: (id) => api.delete(`products/${id}/`),
};

// API для работы с заказами
export const orderService = {
  getOrders: () => api.get('orders/'),
  getOrder: (id) => api.get(`orders/${id}/`),
  updateOrderStatus: (id, status) => api.patch(`orders/${id}/`, { status }),
};

// API для работы с поставками
export const supplyService = {
  getSupplies: () => api.get('supplies/'),
  getSupply: (id) => api.get(`supplies/${id}/`),
  createSupply: (data) => api.post('supplies/', data),
  updateSupply: (id, data) => api.patch(`supplies/${id}/`, data),
  deleteSupply: (id) => api.delete(`supplies/${id}/`),
};

// API для работы с отгрузками
export const shipmentService = {
  getShipments: () => api.get('shipments/'),
  getShipment: (id) => api.get(`shipments/${id}/`),
  createShipment: (data) => api.post('shipments/', data),
  updateShipment: (id, data) => api.patch(`shipments/${id}/`, data),
  deleteShipment: (id) => api.delete(`shipments/${id}/`),
};

// API для работы с услугами
export const serviceService = {
  getServices: () => api.get('services/'),
  getService: (id) => api.get(`services/${id}/`),
  createService: (data) => api.post('services/', data),
  updateService: (id, data) => api.patch(`services/${id}/`, data),
  deleteService: (id) => api.delete(`services/${id}/`),
};

// API для работы с отчетами
export const reportService = {
  getReports: () => api.get('reports/'),
  getReport: (id) => api.get(`reports/${id}/`),
  generateReport: (data) => api.post('reports/generate/', data),
};

export default api;
