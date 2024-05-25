# RentElektro

RentElektro is a web application for managing electric vehicle rentals. The project uses FastAPI for the backend, Vue.js for the frontend, and Docker for containerization.

## Features

- User authentication and authorization
- Browse available electric vehicles for rent
- Book and manage rentals
- Admin interface for managing vehicle inventory
- Monitoring and observability with Prometheus and Grafana

## Technology Stack

- **Frontend:** Vue.js
- **Backend:** FastAPI
- **Database:** PostgreSQL, MongoDB
- **Cache:** Redis
- **Reverse Proxy:** NGINX
- **Monitoring:** Prometheus, Grafana, cAdvisor
- **CMS:** Directus
- **Containerization:** Docker

## Prerequisites

- Docker and Docker Compose

## Getting Started

### Clone the repository

```bash
git clone https://github.com/your-username/rentelektro.git
cd rentelektro
```
### Prepare envs based on examples

## Run the application with Docker
```bash
docker-compose up --build
```

This will start the FastAPI backend, Vue.js frontend, and other services in separate Docker containers.

Access the application
Frontend: http://localhost:8080
Backend: http://localhost:8000
Directus: http://localhost:8055
Grafana: http://localhost:3000
Prometheus: http://localhost:9090
cAdvisor: http://localhost:8090

Contributing
Contributions are welcome! Please open an issue or submit a pull request.

License
This project is licensed under the MIT License.