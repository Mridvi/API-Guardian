# API Guardian 

Modern applications often expose APIs that handle requests from users, services, and third-party clients. Without proper protection, a client can send too many requests in a short period of time, leading to **API abuse, excessive resource consumption, service degradation, and potential denial-of-service situations**.

**API Guardian** is a lightweight API protection system built with **FastAPI and Redis** that addresses this problem by controlling request traffic before it reaches the application.

It combines **API-key authentication** with **Redis-based rate limiting** using the **Token Bucket algorithm** to ensure that clients stay within defined request limits.

The system also provides **rate-limit response headers** so clients can understand their current request limits and retry timing. A web-based **monitoring dashboard** provides visibility into request activity, successful requests, and rate-limited requests.

This project demonstrates practical backend concepts including **API security, middleware, rate limiting, Redis, asynchronous APIs, monitoring, and Dockerized application development**.

---

## 🚀 Features

- ⚡ **Redis-based Rate Limiting** using the **Token Bucket algorithm**
- 🔑 **API-Key Authentication** for protected endpoints
- 📊 **Monitoring Dashboard** for request statistics
- 📈 **Recent Request Activity** tracking
- 🚫 **429 Too Many Requests** handling
- ⏱️ **Rate Limit Response Headers**
- 🐳 **Dockerized** FastAPI and Redis environment

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI**
- **Redis**
- **Docker**
- **Lua**
- **HTML**
- **CSS**
- **JavaScript**

---

## ⚙️ How It Works

API requests pass through a **rate-limiting middleware** before reaching the API endpoint.

The system uses the **Token Bucket algorithm** to control the number of requests a client can make.

```text
Client Request
      │
      ▼
API Key Authentication
      │
      ▼
Rate Limiting Middleware
      │
      ▼
    Redis
      │
   ┌──┴───┐
   ▼      ▼
Allowed  Blocked
   │      │
   ▼      ▼
  200    429
```

Redis stores the **token count** and **timestamp** for each client. Tokens are automatically replenished based on the configured **refill rate**.

---

## 🔐 API Authentication

Protected endpoints require an **API key** to be sent through the request header.

### API Key

```text
X-API-Key: demo-key-123
```

### Example Request

```bash
curl -H "X-API-Key: demo-key-123" http://localhost:8000/api/example
```

If an invalid API key is provided, the API returns:

```text
401 Unauthorized
```

---

## 🚦 Rate Limiting

The default rate-limiting configuration is:

| **Configuration** | **Value** |
|---|---:|
| **Bucket Capacity** | **10 requests** |
| **Refill Rate** | **2 tokens/second** |
| **Tokens Per Request** | **1** |

When the rate limit is exceeded, the API returns:

```text
429 Too Many Requests
```

### Rate Limit Headers

The API provides the following response headers:

```text
X-RateLimit-Limit
X-RateLimit-Remaining
Retry-After
```

These headers allow clients to understand their current **rate-limit status** and how long they should wait before retrying.

---

## 📊 Monitoring Dashboard

API Guardian includes a **web-based monitoring dashboard** that provides visibility into API activity.

The dashboard displays:

- **Total Requests**
- **Successful Requests**
- **Rate-Limited Requests**
- **Recent Request Activity**
- **API Status**
- **Rate-Limit Information**


### Access the Dashboard

After starting the application, open:

```text
http://localhost:8000/dashboard
```

---

## 🧪 Testing Rate Limiting

You can send requests to the protected endpoint using the API key.

### Example Request

```bash
curl -H "X-API-Key: demo-key-123" http://localhost:8000/api/example
```

Sending multiple requests rapidly will eventually trigger the rate limiter.

The API will then return:

```text
429 Too Many Requests
```

The dashboard will also record the **rate-limited requests**.

---

## 🐳 Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Mridvi/API-Guardian.git
cd API-Guardian
```

### 2. Start the Application

Make sure **Docker Desktop** is running.

```bash
docker compose up --build
```

### 3. Open the API

```text
http://localhost:8000
```

### 4. Open the Dashboard

```text
http://localhost:8000/dashboard
```

---

## 📁 Project Structure

```text
API-Guardian/
│
├── src/
│   ├── main.py
│   ├── request_rate_limiter.lua
│   └── dashboard.png
│
├── dashboard/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🔮 Future Improvements

- **Allow different rate limits for different API keys**
- **Store request statistics permanently**
- **Add an interface to create and manage API keys**
- **Add more detailed request analytics to the dashboard**
- **Add configurable rate-limit settings**

---

## 📌 Project Purpose

API Guardian was built to explore and demonstrate practical **backend development and API security concepts**, including:

- **FastAPI**
- **API Authentication**
- **Middleware**
- **Rate Limiting**
- **Redis**
- **Token Bucket Algorithms**
- **Asynchronous APIs**
- **Docker**
- **API Monitoring**
