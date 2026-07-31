# Distributed Notification System

A production-style microservices notification platform built with FastAPI.

## Project Overview

This repository is a distributed notification system designed to handle user management, template management, and notification delivery across email and push channels.

It is built as a set of loosely coupled microservices with shared infrastructure utilities, enabling each service to focus on a single responsibility while using common conventions for responses, configuration, and messaging.

## Core Services

- `api-gateway` — the HTTP entrypoint for clients, routing incoming requests to downstream services.
- `user_service` — manages user registration, authentication, profiles, and preferences.
- `template_service` — manages notification templates and content that email/push services can render.
- `email_service` — sends notification emails asynchronously.
- `push_service` — sends push notifications asynchronously.

## Shared Components

The `shared` package contains reusable utilities used across services, including:

- response helpers (`shared/responses/response.py`)
- database helpers
- RabbitMQ helpers
- logging and config utilities
- authentication helpers

## Tech Stack

- FastAPI
- PostgreSQL
- RabbitMQ
- Redis
- Docker
- SQLAlchemy
- Alembic

## Architecture

The system is built as an event-driven microservices architecture.

- Services communicate asynchronously using RabbitMQ.
- PostgreSQL is used for persistent storage in services that require it.
- Redis can be used for caching, session storage, or rate limiting.
- Docker is used to containerize each service and infrastructure component.

## Request / Notification Flow

1. A client sends an HTTP request to the API Gateway.
2. The API Gateway routes the request to the appropriate backend service.
3. For user actions, the User Service receives requests under `/api/v1/users` and `/api/v1/auth`.
4. The User Service validates request data with Pydantic schemas, queries PostgreSQL through SQLAlchemy, and returns a shared JSON response.
5. If a user action triggers a notification, the service can publish an event to RabbitMQ.
6. The Template Service can be used to fetch or render notification templates.
7. The Email Service and Push Service subscribe to RabbitMQ notification events, then build and send the actual email or push payload.
8. All services share common helpers from `shared/` for responses, configuration, and messaging.

## Concrete Code Flow in the Current Project

- `services/user_service/app/main.py` initializes the User Service FastAPI app.
- `services/user_service/app/api/v1/users.py` defines user CRUD operations.
- `services/user_service/app/api/v1/auth.py` defines authentication endpoints.
- `shared/responses/response.py` provides the standard `success_response`/`error_response` output format.
- `shared/core/config.py` and service-level config files load environment variables for database, Redis, and RabbitMQ.

## Current Implementation Notes

- The User Service is currently the most complete service, with user and auth routes wired into a FastAPI app.
- The API Gateway and notification services are scaffolded in the repository structure but may still need implementation details.
- RabbitMQ is configured in the root Docker Compose file and is intended to support asynchronous event delivery between services.

## What this project is good for

- Building a production-ready notification platform
- Practicing microservice design with FastAPI
- Working with event-driven communication using RabbitMQ
- Implementing shared utilities across services
- Separating concerns between user management, templates, and notification delivery

## Notes

- Some service entrypoints and shared RabbitMQ logic may still be under development.
- The root Docker Compose file defines infrastructure services like PostgreSQL, RabbitMQ, and Redis.
- Each service is expected to have its own `requirements.txt` and Dockerfile.
