# Video Game Library App – Project Context

## Overview

The Video Game Library App is a full-stack portfolio project that allows users to maintain a personal video game library.

Users can:

- Add games manually
- View their game library
- Delete games
- Search for games using the RAWG API
- Import games directly from RAWG into their personal library

The goal of this project is to demonstrate **clean architecture**, **testability**, and **modern full-stack development**.

---

# Architecture

The backend follows a **layered Clean Architecture style** to enforce separation of concerns.

src
├── application
│ └── services / use cases
│
├── domain
│ ├── entities
│ └── repository interfaces
│
├── infrastructure
│ ├── database models
│ ├── repository implementations
│ └── external API clients
│
└── presentation
├── FastAPI routes
└── request/response schemas


### Layer Responsibilities

| Layer | Responsibility |
|-----|-----|
| Domain | Core business entities and interfaces |
| Application | Use cases and business logic |
| Infrastructure | Database and external APIs |
| Presentation | HTTP routes and validation |

This architecture ensures:

- Domain logic is independent from frameworks
- External services can be replaced easily
- Code is easy to test with fakes

---

# Backend Stack

Framework: **:contentReference[oaicite:2]{index=2}**  
Database ORM: **:contentReference[oaicite:3]{index=3}**  
Server: **:contentReference[oaicite:4]{index=4}**

Database:

- SQLite (development)

External API:

- **:contentReference[oaicite:5]{index=5}**

---

# Frontend Stack

Framework: **:contentReference[oaicite:6]{index=6}**  
Language: **:contentReference[oaicite:7]{index=7}**  
UI: **:contentReference[oaicite:8]{index=8}**

The frontend communicates with the backend through a REST API.

Current features include:

- Displaying the game library
- Searching for external games
- Importing games into the library

---

# Domain Model

## VideoGame Entity

Fields:

| Field | Type |
|-----|-----|
| id | int \| None |
| title | str |
| communal_rating | float |
| personal_rating | float |
| play_state | PlayState |
| platform | Platform |
| image_url | str |
| release_date | str |

---

## PlayState Enum

Represents progress through a game.

NOT_STARTED
STARTED
PLAYED_ENOUGH
BEATEN
PLAY_AGAIN

---

## Platform Enum

Represents the gaming platform.

Examples:
PS1
PS2
PS3
PS4
PS5
SWITCH
DS
THREE_DS
WII
PSP

---

# External API Integration

The project integrates with the RAWG API to allow searching and importing games.

Supported operations:

### Search Games

GET /external/video_games/search?game_name=...
Returns a list of matching games from RAWG.

---

### Get Game By ID

GET /external/video_games/{game_id}
Returns detailed information about a game.

---

### Import Game From RAWG

POST /external/video_games/{game_id}/import

---

Flow:

RAWG API
↓
ExternalGameService
↓
Domain VideoGame entity
↓
Repository.save()
↓
Stored in database

---

# Database

The database uses SQLAlchemy models in the infrastructure layer.

Example table:

video_games

Columns:
id
title
communal_rating
personal_rating
play_state
platform
image_url
release_date

Enums are stored as **strings** in the database.

---

# Testing

Tests use **fake implementations** instead of the real database.

Example:
FakeGameRepository
FakeRawgClient

This allows:

- fast tests
- no database dependency
- deterministic behavior

Test categories include:

- service tests
- API route tests
- integration tests

---

# Current Features

Implemented backend features:

- Add game to library
- List library
- Delete games
- Search RAWG
- Import RAWG game by ID

Implemented frontend features:

- View library
- Search external games
- Import game into library

---

# Planned Improvements

## Backend

- Platform mapping from RAWG → Platform enum
- Pagination for search results
- Sorting and filtering library
- Proper error handling
- API rate limiting
- Authentication

---

## Frontend

- Display game cover images
- Better game cards
- Loading states
- Error messages
- Library filters
- Mobile responsive layout

---

# Development Setup

## Backend

Run server:
uvicorn main:app --reload

API runs at:
http://localhost:8000

---

## Frontend

Run Next.js:
npm run dev

Frontend runs at:
http://localhost:3000

---

# Project Goals

This project is designed to demonstrate:

- Clean architecture
- Dependency inversion
- Testable services
- Full-stack integration
- Modern React + TypeScript development
- External API integration
