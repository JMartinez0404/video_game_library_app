# Video Game Library App — Architecture Overview

## Overview

This project follows a **Clean Architecture / Layered Architecture** approach with elements of **Domain-Driven Design (DDD)** and the **Repository Pattern**.

The core principle of this architecture is:

> Business logic should not depend on frameworks, databases, or external systems.

Instead, external systems depend on the core business logic.

This makes the system:

- Easier to test  
- Easier to refactor  
- Easier to extend  
- More maintainable over time  

---

# Architectural Layers

The project is organized into the following layers:

Presentation (FastAPI routes)
↓
Application (Use Cases / Services)
↓
Domain (Entities + Repository Interfaces)
↓
Infrastructure (Database, Object-Relational Mapping (ORM), External APIs)


Each layer has a specific responsibility and strict dependency direction.

---

# 1. Domain Layer (`src/domain/`)

The **Domain Layer** contains the core business concepts and rules.

It has:

- No FastAPI  
- No SQLAlchemy  
- No database logic  
- No external API calls  

This layer is pure Python and framework-independent.

---

## `entities.py`

Defines the core domain models:

- `PlayState` (Enum)  
- `Platform` (Enum)  
- `VideoGame` (dataclass)  

These represent the core business objects of the application.

The `VideoGame` dataclass is the canonical representation of a game inside the system.

---

## `repositories.py`

Defines the `GameRepository` abstract base class.

This is a repository interface that declares:

- `add(video_game: VideoGame) -> VideoGame`  
- `list() -> List[VideoGame]`  

This is an example of **Dependency Inversion**.

---

# 2. Application Layer (`src/application/`)

The Application Layer contains **use cases** and orchestrates domain logic.

It depends on:

- Domain entities  
- Repository interfaces  

It does **not** depend on:

- FastAPI  
- SQLAlchemy  
- Database models  

---

## `game_use_cases.py`

Defines `GameService`.

Responsibilities:

- Coordinates adding a video game  
- Retrieves the video game library  

This is where business logic would live if it became more complex.

---

# 3. Infrastructure Layer (`src/infrastructure/`)

The Infrastructure Layer contains concrete implementations of interfaces defined in the domain.

This includes:

- Database models  
- Repository implementations  
- External API clients  
- Session management  

Infrastructure depends on the domain — never the other way around.

---

## `databases/models.py`

Defines the SQLAlchemy ORM model:

`GameModel`

This represents how video games are stored in the database.

Important distinction:

- `GameModel` is a persistence model.  
- `VideoGame` is a domain model.  

They are intentionally separate.

---

## `databases/sessions.py`

Responsible for:

- Creating the SQLAlchemy engine  
- Configuring the session factory  
- Providing `get_db()` dependency for FastAPI  
- Managing session lifecycle  

This ensures:

- One database session per request  
- Proper cleanup after each request  

---

## `repositories/game_repository.py`

Implements the domain `GameRepository` interface using SQLAlchemy.

`SQLAlchemyGameRepository`:

- Converts `VideoGame` → `GameModel`  
- Persists to the database  
- Converts `GameModel` → `VideoGame`  

This is the adapter between domain logic and the database.

---

## `external_apis/rawg_client.py`

Reserved for integration with external APIs (e.g., RAWG video game database).

This keeps external API logic isolated from domain and application layers.

---

## `presentation/routes.py`

Defines FastAPI routes.

Responsibilities:

- Accept HTTP requests  
- Validate request data (via schemas)  
- Construct the service layer  
- Return responses  

Routes remain thin and delegate business logic to the application layer.

---

## `presentation/schemas.py`

Defines Pydantic models for:

- Request validation  
- Response serialization  

These models:

- Validate incoming data  
- Provide OpenAPI documentation  
- Keep API contracts separate from domain models  

---

# 4. Entry Point (`src/main.py`)

Responsible for:

- Creating the FastAPI application  
- Including routers  
- Creating database tables (development only)  

This is the application bootstrap layer.

---

# 5. Tests (`tests/`)

Contains unit tests and test utilities.

---

## `fakes.py`

Contains fake repository implementations for testing.

This allows testing `GameService` without touching the database.

---

## `test_game_service.py`

Tests application logic in isolation from infrastructure.

This is possible because of the repository abstraction.

---

# Why This Architecture Is Important

## 1. Separation of Concerns

Each layer has a single responsibility:

- Domain → business rules  
- Application → orchestration  
- Infrastructure → external systems  
- Presentation → HTTP handling  

This prevents tight coupling.

---

## 2. Dependency Inversion

The domain defines interfaces.  
Infrastructure implements them.

This means:

- You can swap databases without changing business logic.  
- You can mock repositories in tests.  
- The system remains flexible.  

---

## 3. Testability

Because business logic does not depend on the database:

- You can test `GameService` with fake repositories.  
- You don’t need a real database for unit tests.  

This leads to fast, reliable testing.

---

## 4. Maintainability

As the project grows, you can:

- Add new use cases without touching infrastructure  
- Add new infrastructure (e.g., PostgreSQL, Redis, external APIs)  
- Introduce more complex business rules safely  

The architecture scales with complexity.

---

# Data Flow Example

When a client sends a POST request:

HTTP Request
↓
FastAPI Route
↓
Pydantic Schema Validation
↓
Domain Entity (VideoGame)
↓
GameService (Application Layer)
↓
GameRepository (Interface)
↓
SQLAlchemyGameRepository (Infrastructure)
↓
Database


Each layer only knows about the layer directly below it.

---
