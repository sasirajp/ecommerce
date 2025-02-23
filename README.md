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


## Design Decisions and trade-offs

1) Used FastAPI as BE framework & PostgresSQL as db
    Trade-off
        Pros - high performance framework and reliable db for structured data
        Cons - requires additional optimisation - connect db for each request is not optimal, need to implement connection pool.
2) Used python's queue.Queue and threading for background scheduling
    Trade-off
        Pros - python's queue is thread safe which is ideal for this scenario problem statement says to use in memory queue.
        Cons - Will cause serious issue in distributed env, should be using redis Queue/Kafka
3) Added worker threads to process orders
   Trade-off
        pros - Keeps API responsive, as processing happens in background.
        cons - For higher scalability, should be shifting to celery workers
               can also use master-slave architecture where slaves will process orders(for high scalability, mostly not required)
4) Containerized Application for easy set up.


## Assumptions
1) each order goes through definite cycle PENDING -> PROCESSING -> COMPLETED (Added retry logic if order is stuck for more than 10 mins, only possible if application crashes while processing a order).
2) Single server and 3 workers are efficient to handle rest service & order processing.
3) Each Order will be processed between 2 and 7 seconds.
4) On crash of application, processing will start again for non completed order won't continue orders in the queue.
5) Avg time is only required for completed orders only as per problem statement.
