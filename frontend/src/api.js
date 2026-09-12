import axios from 'axios';

const api = axios.create({
    baseUrl : 'http://localhost:8000/api'
});

api.interceptors.request.use((config) => {
    if (token){
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
})

export default api;