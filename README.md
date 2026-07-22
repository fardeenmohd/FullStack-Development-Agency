# Gemini Multi-Service AI Platform

| Agent File          | Persona               | Primary Role                                                                                                               |
| :------------------ | :-------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| `mother_agent.py`   | The Visionary         | Creates the initial `requirements.txt` from a high-level idea.                                                             |
| `father_agent.py`   | The Critic            | Validates the `requirements.txt` for logical consistency.                                                                  |
| `architect.py`      | The Architect         | Designs the `system_blueprint.json` defining microservice architecture.                                                    |
| `synthesizer.py`    | The Prompt Engineer   | Creates specific, context-rich prompts for developer agents.                                                               |
| `devops_agent.py`   | The DevOps Engineer   | Generates `Dockerfile`s and the `docker-compose.yml`.                                                                      |
| `po_agent.py`       | The Product Owner     | Creates tickets on the Kanban board from feature requests.                                                                 |
| `run_all.py`        | The Dispatcher/Developer | Takes tickets, generates code, applies it, and moves to `in_review`.                                                       |
| `designer_agent.py` | The UX/UI Designer    | Polishes frontend UI/UX and hot-reloads the service.                                                                       |
| `qa_gatekeeper.py`  | The QA Gatekeeper     | Generates and executes `unittest` scripts for backend code in review.                                                      |
| `docker_agent.py`   | The Build Engineer    | Attempts to build services with code changes and catches build errors.                                                     |
| `dba_agent.py`      | The DBA               | Generates and applies Flyway SQL migrations for JPA `@Entity` changes.                                                     |
| `secops_agent.py`   | The SecOps Engineer   | Scans completed code for security vulnerabilities and creates hotfix tickets.                                              |
| `documenter_agent.py` | The Technical Writer  | Generates release notes for `CHANGELOG.md` from archived tickets.                                                          |
| `innovator_agent.py`| The Innovator         | Invents new features and creates tickets when the system is idle.                                                          |
| `refactor_agent.py` | The Maintainer        | Refactors modified files for quality and rebuilds services after a sprint.                                                 |
| `surveillance_agent.py`| The SRE             | Monitors Docker logs for crashes, generates hotfixes, and restarts services.                                               |
| `local_llm.py`      | Local LLM Adapter     | Client for the locally hosted Ollama LLM.                                                                                  |
| `env_setup.py`      | Environment Setup     | Helper script to load `.env` file and expose API keys.                                                                     |
| `pull_model.py`     | Model Downloader      | One-time script to download the local code generation model.                                                               |
| `list_models.py`    | Model Lister          | Utility to list available cloud-based Google Gemini models.                                                                |

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

## Platform Features

*   **Dual-Workflow System:** Choose between full scaffolding from an idea or iterative, ticket-based development.
*   **Self-Healing Codebase:** AI agents automatically fix build errors and runtime crashes.
*   **Modular Microservices Architecture:** Services are loosely coupled, enabling independent development, deployment, and scaling.
*   **Advanced AI Agent System:** A team of specialized Python agents automates the entire software development lifecycle.
*   **Containerized Development & Deployment:** Utilizes Docker and Docker Compose for consistency and streamlined deployment.
*   **Automated QA:** Test suites are automatically generated for all services.

## Application Features

The platform generated by the AI agents is a powerful lead management and notification system. Key features include:

*   **Lead Scoring Engine:** The Python compute service includes a machine learning model that scores new business leads based on their description, using TF-IDF and cosine similarity to rank their relevance against existing data.
*   **Configurable Real-time Alerts:** The frontend allows users to create custom alerts based on specific criteria like target regions, product categories, and a minimum confidence score. The system will trigger an alert when a new lead matches these rules.
*   **Multi-Channel Notifications:** Users can configure notifications for important business events, such as the creation of a new lead or updates to a transaction. The system can deliver these notifications via email, SMS, or push notification.
*   **Lead Processing Pipeline:** An API endpoint visualizes the journey of a lead as it moves through various stages, from initial scoring to notification triggers and final transaction.

## Service Architecture

The system is designed as a classic three-tier microservice application, with responsibilities clearly delineated by the `architect.py` agent to ensure scalability and separation of concerns.

### 1. Frontend Service (`frontend-nextjs`)

*   **Technology:** Next.js, React, TypeScript, Tailwind CSS
*   **Responsibility:** This service is the user-facing part of the application. It is responsible for rendering the entire user interface, managing client-side state, and providing an interactive experience. It communicates with the backend services via REST APIs to fetch and display data, as well as to submit user-generated content like new alert configurations or notification preferences.

### 2. Compute Service (`compute-python`)

*   **Technology:** Python, FastAPI
*   **Responsibility:** This service is designed for computationally intensive and specialized tasks, as defined by the architect agent's "heavy processing" designation. Its primary role in this application is to host the lead scoring ML model. It exposes a lightweight API that the Java backend can call to get a score for a new lead, offloading the complex calculations from the primary business logic service.

### 3. Backend Service (`backend-java`)

*   **Technology:** Java, Spring Boot, Maven
*   **Responsibility:** This is the core enterprise backend of the application. It handles all primary business logic, data persistence, and API orchestration. It is responsible for managing the database schema, handling user authentication, and exposing the main REST API that the frontend consumes. It coordinates with the Python Compute Service for specialized tasks like lead scoring before persisting the final data.

## Architecture and Tech Stack

*   **Agents Service:** Python, Google Gemini Pro, Local Ollama (Qwen)
*   **Backend Service:** Java, Spring Boot, Maven
*   **Compute Service:** Python, FastAPI, Uvicorn
*   **Frontend Service:** Next.js, React, TypeScript, Tailwind CSS
*   **Containerization:** Docker, Docker Compose
*   **Quality Assurance:** Pytest, JUnit 5, Mockito, Jest, React Testing Library

## Getting Started

### Prerequisites

*   **Docker Desktop:** Required for running the microservices.
*   **Git:** For cloning the repository.
*   **Ollama:** For running the local LLM (`qwen2.5-coder:7b`) that powers several autonomous agents. Ensure Ollama is running in the background.
*   **Git Bash (Windows only):** `start_agency.py` launches agents in separate Git Bash windows.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```
2.  **Set up Python Virtual Environment and Install Dependencies:**
    It's highly recommended to create and activate a Python virtual environment (`venv`) for the agents. `start_agency.py` is configured to activate this environment.
    ```bash
    python -m venv agents/venv
    # On Windows (in your primary terminal, not Git Bash):
    .\agents\venv\Scripts\activate
    # On macOS/Linux:
    source agents/venv/bin/activate
    
    # Install Python dependencies for all agents
    pip install -r agents/requirements.txt
    ```
    (Note: If `agents/requirements.txt` does not exist, run `pip install google-generativeai python-dotenv requests` for basic functionality. The `mother_agent.py` should generate a more comprehensive `requirements.txt` during scaffolding.)

3.  **Download Local LLM (if not already done):**
    The autonomous agents (Innovator, Refactor, SecOps, DBA, Designer, Surveillance, Documenter) rely on a local LLM. Run this script *once* to download the required `qwen2.5-coder:7b` model via Ollama.
    ```bash
    python agents/pull_model.py
    ```
    Ensure Ollama is running before executing this.

4.  **Start the Entire Autonomous Agency:**
    Launch all the background agents (Dispatcher, Designer, QA Gatekeeper, SecOps, DBA, etc.) with a single command from your project root. This will open multiple Git Bash terminal windows, one for each agent.
    ```bash
    python start_agency.py
    ```
    *   **Note for Windows users:** If your Git Bash installation path is different from the default, update the `GIT_BASH_PATH` variable inside `start_agency.py` to match your installation.

### Accessing the Application

*   **Frontend Application:** `http://localhost:3000`
*   **Java Backend API:** `http://localhost:8080`
*   **Python Compute API:** `http://localhost:8000`

## Project Structure and Agent Roles

The project's intelligence lies in the `agents` directory. The agents form a sophisticated, autonomous software factory that operates around a multi-stage Kanban board (`todo` -> `in_progress` -> `in_review` -> `done` -> `archived`). They are best understood by their role in this pipeline.

### 1. Core Scaffolding & Task Management Agents

These agents handle the initial project creation and the core task loop (creating and executing tickets).

*   **`mother_agent.py` (The Visionary):** Entry point for scaffolding. Creates the initial `requirements.txt` from a high-level idea.
*   **`father_agent.py` (The Critic):** Validates the `requirements.txt` for logical consistency.
*   **`architect.py` (The Architect):** Designs the `system_blueprint.json` from the requirements, defining the microservice architecture.
*   **`synthesizer.py` (The Prompt Engineer):** Creates specific, context-rich prompts for developer agents based on the blueprint.
*   **`devops_agent.py` (The DevOps Engineer):** Generates `Dockerfile`s and the `docker-compose.yml`.
*   **`po_agent.py` (The Product Owner):** Creates tickets on the Kanban board from user or AI (`innovator_agent`) feature requests.
*   **`run_all.py` (The Dispatcher/Developer):** The primary worker. It takes tickets from the `todo` column, generates the code, applies it, and moves the ticket to `in_review`. It also retries tickets kicked back from the QA or Designer agents.

### 2. Pipeline & Quality Gate Agents

These specialist agents watch the `in_review` column, acting as automated code review and quality gates before a ticket can be marked as "done".

*   **`designer_agent.py` (The UX/UI Designer):** Watches for `frontend` tickets in review. It automatically polishes the UI/UX of the code using a design system prompt and then hot-reloads the frontend service.
*   **`qa_gatekeeper.py` (The QA Gatekeeper):** Watches for `compute` or `enterprise` tickets in review. It generates and executes `unittest` scripts inside the appropriate Docker container to validate the new code. If tests fail, it rejects the ticket and sends it back to `todo` with the failure logs for the Dispatcher to fix.
*   **`docker_agent.py` (The Build Engineer):** Though used in scaffolding, its primary loop function is to attempt to build any service that has a code change, catching build errors before they break the application.

### 3. Autonomous Post-Process & Surveillance Agents

These agents run continuously, observing the system state and performing automated maintenance, security, and documentation tasks on tickets that are already in the `done` or `archived` columns.

*   **`dba_agent.py` (The DBA):** Scans completed `enterprise` tickets. If it detects a change to a JPA `@Entity` file, it auto-generates a Flyway SQL migration script and restarts the database to apply the schema change.
*   **`secops_agent.py` (The SecOps Engineer):** Continuously scans all completed code in `done` and `archived` for security vulnerabilities. If a flaw is found, it injects a high-priority hotfix ticket into the front of the `todo` queue.
*   **`documenter_agent.py` (The Technical Writer):** Batches completed tickets from the `archived` column and uses an LLM to write professional, user-friendly release notes, which it prepends to the project's `CHANGELOG.md`.
*   **`innovator_agent.py` (The Innovator):** An autonomous product manager. When the entire system is idle (no tickets in `todo` or `in_progress`), it invents a new, synergistic feature and calls `po_agent.py` to create a new ticket, starting the development cycle anew.
*   **`refactor_agent.py` (The Maintainer):** After a "sprint" is complete, this agent refactors all modified files for quality and then rebuilds the services to ensure nothing was broken.
*   **`surveillance_agent.py` (The SRE):** Provides runtime self-healing. It monitors Docker logs for crash signatures, and if a service fails, it uses an LLM to generate a hotfix, applies it, and restarts the service.

### 4. Utility & Helper Scripts

These scripts support the agent ecosystem.

*   **`local_llm.py` (Local LLM Adapter):** A crucial client for the locally hosted Ollama LLM (`qwen2.5-coder:7b`), used by all the autonomous loop agents.
*   **`env_setup.py`:** A simple helper script to load the `.env` file and expose the Gemini API key to the agents.
*   **`pull_model.py`:** A one-time setup script to download the required local code generation model.
*   **`list_models.py`:** A utility to list available cloud-based Google Gemini models.
