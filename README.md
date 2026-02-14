# Microservices Planning & Descriptions

## 1. API Gateway

**Tech:** Python FastAPI, HTTPS, Docker

- Entry point for all client requests (REST API)
- Handles authentication (delegates to Auth via gRPC)
- Forwards requests to Orders service (gRPC)
- Performs request validation, rate limiting, and logging
- Handles HTTPS termination
- Can implement request/response transformation

**Planned Steps:**
1. Scaffold FastAPI project with HTTPS support
2. Implement REST endpoints for order and auth flows
3. Integrate gRPC clients for Auth and Orders
4. Add middleware for logging, rate limiting, and error handling
5. Write Dockerfile and docker-compose integration
6. Add unit/integration tests

---

## 2. Auth Service

**Tech:** Go, gRPC, HTTPS, Docker, MongoDB

- Handles user authentication and authorization
- Provides gRPC endpoints for login, token verification, registration
- Publishes domain events (e.g., UserLoggedIn) to Message Broker (RabbitMQ)
- Stores user data and tokens in MongoDB
- Issues JWT and refresh tokens

**Planned Steps:**
1. Scaffold Go project with gRPC and HTTPS
2. Define protobuf contracts for Auth API
3. Implement login, registration, and token verification logic
4. Integrate MongoDB for user storage
5. Publish events to RabbitMQ
6. Write Dockerfile and docker-compose integration
7. Add unit/integration tests

---

## 3. Orders Service

**Tech:** Python FastAPI (or Go), gRPC, HTTPS, Docker, MongoDB

- Handles order creation, retrieval, and management
- Provides gRPC endpoints for order operations
- Publishes domain events (e.g., OrderCreated) to Message Broker (RabbitMQ)
- Stores order data in MongoDB

**Planned Steps:**
1. Scaffold project with gRPC and HTTPS
2. Define protobuf contracts for Orders API
3. Implement order creation, retrieval, and cancellation logic
4. Integrate MongoDB for order storage
5. Publish events to RabbitMQ
6. Write Dockerfile and docker-compose integration
7. Add unit/integration tests

---

## 4. Notifications Service

**Tech:** Python FastAPI, SSE, RabbitMQ, Docker

- Consumes events from RabbitMQ (OrderCreated, UserLoggedIn, etc.) using a background task (async worker)
- Publishes received events to an in-memory pub/sub queue (or async queue)
- SSE endpoint streams notifications to connected clients by reading from this in-memory queue
- Decouples message consumption from HTTP request handling for better scalability and reliability
- Can be extended to send emails, SMS, or push notifications
- Exposes `/notifications/stream` endpoint for real-time updates

**Detailed Architecture:**
1. **Background Task (RabbitMQ Consumer):**
    - Runs as an async task on FastAPI startup.
    - Connects to RabbitMQ and subscribes to the `notifications` queue.
    - On receiving a message, publishes it to an in-memory queue (e.g., Python list, asyncio.Queue, or pub/sub system).

2. **SSE Endpoint:**
    - Clients connect to `/notifications/stream` for real-time updates.
    - The endpoint reads from the in-memory queue and streams new notifications to each client as SSE events.
    - Each client receives only new messages that arrive after their connection.

3. **Benefits:**
    - Clean separation of concerns: message consumption and HTTP streaming are independent.
    - Improved reliability: SSE endpoint is not blocked by RabbitMQ or network issues.
    - Scalable: Multiple consumers or SSE endpoints can be added as needed.

**Planned Steps:**
1. Scaffold FastAPI project with SSE endpoint
2. Implement background task to consume from RabbitMQ and publish to in-memory queue
3. Implement SSE endpoint to stream from in-memory queue to clients
4. Add Dockerfile and docker-compose integration
5. Add unit/integration tests

---

## 5. Message Broker (RabbitMQ)

**Tech:** RabbitMQ, Docker

- Central event bus for async communication between services
- Used for publishing and consuming domain events
- Decouples services and enables event-driven architecture

**Planned Steps:**
1. Add RabbitMQ service to docker-compose
2. Define event topics/queues (e.g., auth, orders, notifications)
3. Document event contracts and payloads

---

## 6. MongoDB

**Tech:** MongoDB, Docker

- Each service (Auth, Orders) has its own MongoDB instance
- Used for persistent storage of users, orders, etc.

**Planned Steps:**
1. Add MongoDB services to docker-compose
2. Define database schemas/collections for each service
3. Implement backup and monitoring strategies

---

## 7. Common Steps

- Write Dockerfiles for each service
- Create a unified docker-compose.yml for local development
- Set up HTTPS certificates for all services
- Add CI/CD pipeline for build, test, and deploy

---
## Notifications Service

- Built with FastAPI
- Uses Server-Sent Events (SSE) to stream notifications to clients
- Consumes messages asynchronously from RabbitMQ
- Exposes `/notifications/stream` endpoint for real-time notifications

### How it works

1. The service connects to RabbitMQ and listens for messages on the `notifications` queue.
2. When a message arrives, it is sent to connected clients via SSE.
3. Clients receive real-time notifications by subscribing to the SSE endpoint.
# Project Dependencies & Architecture

## Dependencies

- **Python FastAPI**: Main framework for API services (API Gateway, Order, etc.)
- **Go**: Used for the Auth microservice
- **Docker**: Containerization for all services
- **MongoDB**: Main database for each microservice

## Architecture Overview

All services are HTTPS servers and run as independent microservices:

1. **API Gateway** (Python FastAPI, HTTPS)
2. **Order Service** (Python FastAPI, HTTPS)
3. **Auth Service** (Go, HTTPS)
4. **MongoDB**: Each microservice has its own MongoDB instance
5. **Other Services**: Can be added as needed, following the same pattern

## Running the Project

- All services are containerized using Docker
- Each service exposes an HTTPS endpoint
- MongoDB runs as a container for each microservice

## To Do

- [ ] Add Dockerfiles for each service
- [ ] Implement HTTPS certificates for all services
- [ ] Define API contracts for each microservice
- [ ] Add more microservices as needed
# DI-405
the micro services for docker containers

# Main Arch
```mermaid
classDiagram
    class APIGateway {
        +startHttpServer(host: str, port: int): None
        +handleHttpRequest(request: HttpRequest): HttpResponse
        +forwardToAuthGrpc(request: AuthRequestDTO): AuthResponseDTO
        +forwardToOrdersGrpc(request: OrderRequestDTO): OrderResponseDTO
    }

    class AuthServiceGrpc {
        +startGrpcServer(host: str, port: int): None
        +Login(request: LoginRequest): LoginResponse
        +VerifyToken(request: VerifyTokenRequest): VerifyTokenResponse
        +PublishAuthEvent(event: AuthDomainEvent): None
    }

    class OrdersServiceGrpc {
        +startGrpcServer(host: str, port: int): None
        +CreateOrder(request: CreateOrderRequest): CreateOrderResponse
        +GetOrder(request: GetOrderRequest): GetOrderResponse
        +CancelOrder(request: CancelOrderRequest): CancelOrderResponse
        +PublishOrderEvent(event: OrderDomainEvent): None
    }

    class MessageBroker {
        +publish(topic: str, event: DomainEvent): None
        +subscribe(topic: str, handler: EventHandler): None
    }

    class NotificationsService {
        +startWorker(): None
        +handleOrderEvent(event: OrderDomainEvent): None
        +handleAuthEvent(event: AuthDomainEvent): None
        +sendEmail(to: str, message: str): bool
        +sendSMS(to: str, message: str): bool
    }

    %% Relationships (Async)
    APIGateway --> AuthServiceGrpc : HTTPS REST → gRPC
    APIGateway --> OrdersServiceGrpc : HTTPS REST → gRPC

    AuthServiceGrpc --> MessageBroker : publish events
    OrdersServiceGrpc --> MessageBroker : publish events

    MessageBroker --> NotificationsService : async consume

```

# Create Order flow
```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant GW as API Gateway (HTTPS/REST)
    participant Auth as Auth Service (gRPC)
    participant Orders as Orders Service (gRPC)
    participant Broker as Message Broker
    participant Notif as Notifications Service (Async Worker)

    Client->>GW: POST /api/v1/orders (JWT, order payload)
    GW->>Auth: VerifyToken(JWT)
    Auth-->>GW: TokenValid(userId)

    GW->>Orders: CreateOrder(userId, items)
    Orders-->>GW: OrderCreated(orderId, status)

    GW-->>Client: 201 Created (orderId)

    Orders-->>Broker: Publish OrderCreatedEvent
    Broker-->>Notif: Consume OrderCreatedEvent (async)
    Notif->>Notif: Send email/SMS/push
```

# Login flow
```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant GW as API Gateway (HTTPS/REST)
    participant Auth as Auth Service (gRPC)
    participant Broker as Message Broker
    participant Notif as Notifications Service (Async Worker)

    Client->>GW: POST /api/v1/auth/login (username, password)
    GW->>Auth: Login(credentials)
    Auth-->>GW: AuthToken(JWT, refreshToken)

    GW-->>Client: 200 OK (JWT, refreshToken)

    Auth-->>Broker: Publish UserLoggedInEvent
    Broker-->>Notif: Consume UserLoggedInEvent (async)
    Notif->>Notif: Send login alert email (optional)
```

# 🧾 Get Order Details Flow (Read-only, no notifications)
```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant GW as API Gateway (HTTPS/REST)
    participant Auth as Auth Service (gRPC)
    participant Orders as Orders Service (gRPC)

    Client->>GW: GET /api/v1/orders/{orderId} (JWT)
    GW->>Auth: VerifyToken(JWT)
    Auth-->>GW: TokenValid(userId)

    GW->>Orders: GetOrder(orderId, userId)
    Orders-->>GW: OrderDetails

    GW-->>Client: 200 OK (OrderDetails)
```
