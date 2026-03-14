# Frontend Architecture Guide

This frontend is built using Next.js and TypeScript.

The goal is to keep UI, API communication, and types separated.

---

# Folder Structure

app/
Next.js routes and pages.

components/
Reusable React UI components.

lib/api/
Functions that communicate with the backend API.

types/
Shared TypeScript interfaces and types.

---

# Component Rules

React components should:

- only handle UI and interaction
- not contain fetch logic
- receive data through props

Example:

GameCard.tsx should only display game data and trigger events.

---

# API Layer

All HTTP requests should be defined in:

lib/api/

Example:

lib/api/games.ts

These functions call the FastAPI backend.

---

# Types

Shared types should be defined in:

types/

Example:

types/game.ts

Example type:

export interface Game {
  id: number
  title: string
  communal_rating: number
  personal_rating: number
  image_url: string
  release_date: string
}

---

# Data Flow

Page components fetch data using API functions.

Example flow:

page.tsx
  ↓
lib/api/games.ts
  ↓
FastAPI backend

---

# UI Philosophy

Prefer:

- small reusable components
- typed props
- simple state

Avoid:

- large components
- duplicated API calls
- business logic in components
