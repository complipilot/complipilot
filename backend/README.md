# Complipilot Backend

[![CI](https://github.com/<YOUR_USERNAME>/complipilot/actions/workflows/ci.yml/badge.svg)](https://github.com/<YOUR_USERNAME>/complipilot/actions/workflows/ci.yml)
[![Coverage Status](https://img.shields.io/codecov/c/github/<YOUR_USERNAME>/complipilot.svg)](https://codecov.io/gh/<YOUR_USERNAME>/complipilot)

A FastAPI-based backend for Complipilot, a compliance management system for tracking policies, gaps, tasks, and evidence.

---

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Database Migrations](#database-migrations)  
- [Running Locally](#running-locally)  
- [API Endpoints](#api-endpoints)  
- [Testing](#testing)  
- [CI/CD](#cicd)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- ✅ User registration & JWT-based authentication  
- ✅ “/me” endpoint to fetch current user  
- ✅ Models for `Policy`, `Gap`, `Task`, `Evidence`  
- ✅ Auto-generated OpenAPI docs  
- ✅ Full test coverage with Pytest  

## Tech Stack

- **Python** 3.12  
- **FastAPI**  
- **SQLModel** (built on SQLAlchemy)  
- **PostgreSQL** (or SQLite for local/dev)  
- **Alembic** for schema migrations  
- **Poetry** for dependency & virtual-env management  
- **GitHub Actions** for CI  

## Prerequisites

- Python 3.12+  
- Poetry (`pip install poetry`)  
- PostgreSQL (or you can switch to SQLite by adjusting `DATABASE_URL`)  
- Git  

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/<YOUR_USERNAME>/complipilot.git
   cd complipilot/backend
