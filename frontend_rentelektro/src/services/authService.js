import axios from 'axios';

export function saveToken(response) {
    const accessToken = response.data.access_token;
    const refreshToken = response.data.refresh_token;
    const expiresIn = 900; // assuming 30 minutes in seconds
    const expirationTime = new Date().getTime() + expiresIn * 1000;

    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('tokenExpiration', expirationTime);
    localStorage.setItem('refresh_token', refreshToken);
}

export function isTokenExpired() {
    const expirationTime = localStorage.getItem('tokenExpiration');
    const now = new Date().getTime();

    return now > expirationTime;
}

export function removeToken() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('tokenExpiration');
}

export function getToken() {
    if (isTokenExpired()) {
        console.log('Token expired');
        localStorage.removeItem('access_token');
        localStorage.removeItem('tokenExpiration');
        return null;
    }

    return localStorage.getItem('access_token');
}

axios.interceptors.request.use(
    config => {
        const token = getToken();
        if (token) {
            config.headers['Authorization'] = 'Bearer ' + token;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

export function refreshToken() {
    return axios.post('api/users/refresh', { refresh_token: localStorage.getItem('refresh_token') })
        .then(response => {
            const accessToken = response.data.access_token;
            const expiresIn = 600; // Adjust as needed
            const expirationTime = new Date().getTime() + expiresIn * 1000;

            localStorage.setItem('access_token', accessToken);
            localStorage.setItem('tokenExpiration', expirationTime);
            localStorage.setItem('refresh_token', response.data.refresh_token); // Update refresh token
        })
        .catch(() => {
            localStorage.removeItem('access_token');
            localStorage.removeItem('tokenExpiration');
            localStorage.removeItem('refresh_token');
        });
}

// Call refreshToken periodically or based on your application's needs
setInterval(refreshToken, 25 * 60 * 1000); // Refresh token 5 minutes before expiration