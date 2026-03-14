# AI Contributor Guide

This repository implements a video game library using Clean Architecture.

AI agents should follow these rules when modifying the codebase.

---

# Architecture Rules

The backend follows a layered architecture:

presentation → application → domain → infrastructure

Dependencies must only flow inward.

Allowed imports:

presentation → application
application → domain
infrastructure → domain

Forbidden imports:

domain → infrastructure
domain → fastapi
domain → sqlalchemy

---

# Domain Layer

Location:
src/domain

Contains:

- entities
- enums
- repository interfaces

The domain layer must not depend on any framework.

---

# Application Layer

Location:
src/application

Contains business logic and use cases.

Services orchestrate domain entities and repositories.

Application services may depend on:

- domain entities
- repository interfaces
- external API clients

---

# Infrastructure Layer

Location:
src/infrastructure

Contains:

- SQLAlchemy models
- repository implementations
- external API clients

Infrastructure implements domain interfaces.

---

# Presentation Layer

Location:
src/presentation

Contains:

- FastAPI routes
- request/response schemas

Routes should only:

- validate inputs
- call application services
- return responses

Routes must not contain business logic.

---

# External API

The application integrates with the RAWG API.

External API calls must be implemented inside:

infrastructure/external_apis/rawg_client.py

Application services should call the client rather than using HTTP directly.

---

# Frontend

Frontend uses Next.js with TypeScript.

The frontend communicates with the backend through the REST API.

API helper functions are located in:

frontend/lib/api/

---

# Testing

Tests use fake implementations rather than real infrastructure.

Examples:

FakeGameRepository
FakeRawgClient

Tests should validate behavior of application services.

---

# Development Commands

Backend:

uvicorn main:app --reload

Frontend:

npm run dev

---

# Code Style Guidelines

Prefer:

- small services
- explicit types
- dependency injection
- domain-first modeling

Avoid:

- business logic in routes
- direct database access outside repositories
