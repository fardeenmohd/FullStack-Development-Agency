# Gemini Multi-Service AI Platform

This project implements a sophisticated multi-service AI platform, designed to leverage a microservices architecture for enhanced scalability, maintainability, and specialized functionality. It integrates AI agents for intelligent automation, a robust Java Spring Boot backend for core business logic, a high-performance Python FastAPI compute service, and a modern Next.js frontend for a dynamic user experience.

## Agent System Workflows

This project features two distinct, powerful workflows for managing the software development lifecycle:

### 1. The Parental Guidance System (Initial Scaffolding)

This workflow is designed to take a high-level startup idea and autonomously generate a complete, production-ready application scaffold.

1.  **Idea Inception (`mother_agent.py`)**: The "Mother Agent" (CTO) takes a user's idea and generates a comprehensive `requirements.txt` specification.
2.  **Critical Review (`father_agent.py`)**: The "Father Agent" (Lead Systems Reviewer) analyzes the specification for logical flaws. It provides feedback in a loop with the Mother Agent until the spec is approved.
3.  **Architectural Design (`architect.py`)**: The "Architect Agent" reads the approved spec and designs a detailed `system_blueprint.json`, outlining the entire microservice architecture.
4.  **Code Generation (`frontend_agent.py`, `compute_agent.py`, `enterprise_agent.py`)**: Specialized developer agents read the blueprint and generate the full codebase for the Next.js frontend, Python FastAPI compute engine, and Java Spring Boot backend.
5.  **Infrastructure & QA (`devops_agent.py`, `qa_agent.py`)**: The "DevOps Agent" creates the `docker-compose.yml` and `Dockerfile`s, while the "QA Agent" generates full test suites for all services.
6.  **Build & Surveillance (`docker_agent.py`)**: This agent takes over to build all Docker containers. If a build fails, it uses a local AI to analyze the error and fix the code, retrying automatically. Once the build succeeds, it transitions to a runtime surveillance mode to detect and hotfix crashes in real-time.

### 2. The Antigravity System (Iterative Development)

This workflow is designed for making granular, ticket-based changes to the existing application.

1.  **Feature Request (`po_agent.py`)**: A user provides a feature request. The "Product Owner Agent" breaks this down into detailed technical tickets and adds them to a Kanban-style board (`antigravity_board.json`).
2.  **Task Execution (`run_all.py`)**: The "Dispatcher" continuously watches the board. When a new ticket appears, it uses a local AI to generate the required code changes for the file specified in the ticket.
3.  **Hot-Reload (`run_all.py`)**: After applying the code change, the Dispatcher automatically triggers a Docker rebuild and restart for the affected service, making the changes live instantly.
4.  **Runtime Monitoring (`surveillance_agent.py`)**: This agent (or the `docker_agent.py`) monitors the live application for any runtime crashes, automatically attempting to fix them with AI assistance.

## Features

*   **Dual-Workflow System:** Choose between full scaffolding from an idea or iterative, ticket-based development.
*   **Self-Healing Codebase:** AI agents automatically fix build errors and runtime crashes.
*   **Modular Microservices Architecture:** Services are loosely coupled, enabling independent development, deployment, and scaling.
*   **Advanced AI Agent System:** A team of specialized Python agents automates the entire software development lifecycle.
*   **Java Spring Boot Backend:** Provides a secure and scalable API layer for managing business entities and data persistence.
*   **Python FastAPI Compute Service:** Dedicated service for CPU-intensive tasks and data processing.
*   **Next.js Frontend:** A modern and responsive web application built with TypeScript and Tailwind CSS.
*   **Containerized Development & Deployment:** Utilizes Docker and Docker Compose for consistency and streamlined deployment.
*   **Automated QA:** Test suites are automatically generated for all services.

## Architecture and Tech Stack

*   **Agents Service:** Python, Google Gemini Pro, Local Ollama (Qwen)
*   **Backend Service:** Java, Spring Boot, Maven
*   **Compute Service:** Python, FastAPI, Uvicorn
*   **Frontend Service:** Next.js, React, TypeScript, Tailwind CSS
*   **Containerization:** Docker, Docker Compose
*   **Quality Assurance:** Pytest, JUnit 5, Mockito, Jest, React Testing Library

## Getting Started

### Prerequisites

*   Docker Desktop
*   Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
2.  **Run the Parental Guidance System (Scaffolding):**
    Execute the `mother_agent.py` to start the initial application scaffolding process.
    ```bash
    python agents/mother_agent.py
    ```
    Follow the prompts. This will trigger the entire agent team to generate, build, and deploy the application.

3.  **Use the Antigravity System (Iterative Changes):**
    To make changes, use the `po_agent.py` to create tickets. The `run_all.py` dispatcher will handle the rest.
    ```bash
    # Run the dispatcher in a separate terminal
    python agents/run_all.py

    # In another terminal, create a ticket
    python agents/po_agent.py "Add a new button to the main dashboard"
    ```

### Accessing the Application

*   **Frontend Application:** `http://localhost:3000`
*   **Java Backend API:** `http://localhost:8080`
*   **Python Compute API:** `http://localhost:8000`

## Project Structure

```
.
├── .gitignore
├── docker-compose.yml              # Defines the multi-service Docker environment
├── agents/                         # Python-based AI agents and orchestration scripts
│   ├── mother_agent.py             # Visionary/CTO: Generates the initial product spec. Entry point for scaffolding.
│   ├── father_agent.py             # Critic/Reviewer: Reviews the spec for flaws.
│   ├── architect.py                # System Architect: Designs the microservice blueprint from the spec.
│   ├── synthesizer.py              # Prompt Engineer: Creates specific prompts for developer agents.
│   ├── frontend_agent.py           # Frontend Dev: Generates the Next.js codebase.
│   ├── compute_agent.py            # Python Dev: Generates the FastAPI compute engine.
│   ├── enterprise_agent.py         # Java Dev: Generates the Spring Boot backend.
│   ├── devops_agent.py             # DevOps Architect: Generates Dockerfiles and docker-compose.yml.
│   ├── qa_agent.py                 # QA Engineer: Generates test suites for all services.
│   ├── docker_agent.py             # Build & SRE: Builds Docker images, auto-fixes build errors, and monitors for runtime crashes.
│   ├── surveillance_agent.py       # SRE: Standalone version of the runtime surveillance from docker_agent.py.
│   ├── po_agent.py                 # Product Owner: Breaks feature requests into tickets for the Antigravity system.
│   ├── run_all.py                  # Dispatcher: Executes tickets from the Antigravity board.
│   ├── system_blueprint.json       # Defines the system's overall blueprint.
│   └── antigravity_board.json      # Kanban board for the Antigravity ticket-based system.
├── backend-java/                   # Java Spring Boot backend service
├── compute-python/                 # Python FastAPI compute service
├── frontend-nextjs/                # Next.js frontend application
└── qa-tests/                       # Centralized directory for QA test suites
```

