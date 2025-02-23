# Ecommerce Application

## Setup & Installation

### 1. Start the Application
To build and run the application using Docker, execute:
```sh
docker-compose up --build
```

### 2. Apply Database Migrations
After the containers are running, apply database migrations using Alembic:
```sh
docker exec -it app alembic upgrade head
```

### 3. Load Initial Data
To load initial data into PostgreSQL, run:
```sh
docker exec -i ecommerce_postgres psql -U postgres -d postgres < init.sql
```

### 4. Restart the Application
After migrations and data loading, restart the application:
```sh
docker-compose down
docker-compose up
```

## API Endpoints

### **Accessing FastAPI Docs**
`http://localhost:8000/docs`

### **1. Create an Order**
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/order/create_order' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 2,
  "item_ids": [
    12, 3
  ],
  "total_amount": 55.0
}'
```

### **2. Get an Order by ID**
```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/order/get_order/2' \
  -H 'accept: application/json'
```

### **3. Get Application Metrics**
```sh
curl -X 'GET' \
  'http://localhost:8000/metrics' \
  -H 'accept: application/json'
```


# Design Decisions and Trade-offs

## 1. Backend Framework and Database
- **Technology Used:** FastAPI as the backend framework & PostgreSQL as the database.
- **Trade-offs:**
    - **Pros:** High-performance framework and a reliable database for structured data.
    - **Cons:** Requires additional optimization, as connecting to the database for each request is not optimal. A connection pool needs to be implemented.

## 2. Background Scheduling
- **Technology Used:** Python's `queue.Queue` and threading.
- **Trade-offs:**
    - **Pros:** Python's queue is thread-safe, making it ideal for this scenario where the problem statement specifies using an in-memory queue.
    - **Cons:** In a distributed environment, this approach would cause serious issues. A better alternative would be using Redis Queue or Kafka for message handling.

## 3. Worker Threads for Order Processing
- **Trade-offs:**
    - **Pros:** Keeps the API responsive since processing happens in the background.
    - **Cons:**
        - For higher scalability, the architecture should shift to Celery workers.
        - A master-slave architecture can also be used, where slave nodes handle order processing (mostly unnecessary unless scaling significantly).

## 4. Containerized Application
- The application is containerized for easier setup and deployment.

---

# Assumptions
1. Each order follows a definite cycle: `PENDING -> PROCESSING -> COMPLETED`.
    - Retry logic is added if an order is stuck for more than 10 minutes (only possible if the application crashes while processing an order).
2. A single server with three worker threads is efficient to handle REST service and order processing.
3. Each order processing time ranges between 2 to 7 seconds.
4. On application crash, processing will restart for **non-completed orders**, but in-memory queue orders will not persist.
5. **Average processing time is calculated only for completed orders**, as specified in the problem statement.


