#  SecurePassManager

SecurePassManager is a simple, secure, and fast password management application.  
It uses a Flask API, a Vite-powered frontend, a PostgreSQL database, and Docker for deployment.

---

## Getting Started (Local Setup)

### 1. Clone the Repository

git clone https://github.com/your-username/SecurePass-Manager.git
cd SecurePass-Manager


#### 2.Start the Backend & Database with Docker

```
docker compose build
docker compose up
```

##### 3.Start the Frontend with Vite (in a separate terminal)

```
cd front-end
npm install
npm run build
npm run dev
```
