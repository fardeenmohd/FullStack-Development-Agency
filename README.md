# Gemini Multi-Service AI Platform

This project implements a sophisticated multi-service AI platform, designed to leverage a microservices architecture for enhanced scalability, maintainability, and specialized functionality. It integrates AI agents for intelligent automation, a robust Java Spring Boot backend for core business logic, a high-performance Python FastAPI compute service, and a modern Next.js frontend for a dynamic user experience.

## Features

*   **Modular Microservices Architecture:** Services are loosely coupled, enabling independent development, deployment, and scaling.
*   **Advanced AI Agent System:** A collection of Python-based agents (e.g., `architect`, `compute_agent`, `devops_agent`, `frontend_agent`, `qa_agent`, `mother_agent`, `father_agent`, `synthesizer`) are designed to automate various tasks, orchestrate workflows, and provide intelligent decision-making capabilities.
*   **Java Spring Boot Backend:** Provides a secure and scalable API layer for managing business entities, data persistence, and core application logic.
*   **Python FastAPI Compute Service:** Dedicated service for CPU-intensive computational tasks, data processing, and potentially serving machine learning model inferences with high efficiency.
*   **Next.js Frontend:** A modern and responsive web application built with Next.js, offering a fast and interactive user interface.
*   **Containerized Development & Deployment:** Utilizes Docker and Docker Compose for consistent development environments and streamlined deployment across different environments.
*   **Comprehensive Quality Assurance (QA):** Separate test suites ensure the reliability and correctness of each service component.

## Architecture and Tech Stack

The platform is structured around a microservices paradigm, orchestrated via Docker Compose, incorporating the following key technologies:

*   **Agents Service:**
    *   **Language & Framework:** Python
    *   **Purpose:** Orchestration, intelligent automation, task management, and potential integration with AI/ML capabilities.
*   **Backend Service:**
    *   **Language & Framework:** Java, Spring Boot
    *   **Build Tool:** Apache Maven
    *   **Purpose:** Exposes RESTful APIs, handles business logic, and manages data interactions.
*   **Compute Service:**
    *   **Language & Framework:** Python, FastAPI
    *   **ASGI Server:** Uvicorn
    *   **Purpose:** Executes computationally intensive tasks, data transformations, and potentially hosts AI/ML model endpoints.
*   **Frontend Service:**
    *   **Framework:** Next.js (React)
    *   **Language:** TypeScript
    *   **Purpose:** Delivers the user interface, manages user interactions, and consumes APIs from backend and compute services.
*   **Containerization:**
    *   **Tools:** Docker, Docker Compose
    *   **Purpose:** Defines and runs the multi-container application.
*   **Quality Assurance:**
    *   **Tools:** Pytest (Python), JUnit (Java), Jest/React Testing Library (JavaScript)
    *   **Purpose:** Ensures the functional and performance integrity of each service.

## Getting Started

These instructions will help you set up and run a copy of the project on your local machine for development and testing.

### Prerequisites

*   Docker Desktop (or Docker Engine and Docker Compose) installed and running.
*   Git for cloning the repository.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git # Replace with your actual repository URL
    cd your-repo-name
    ```
2.  **Build and run all services using Docker Compose:**
    This command will build the necessary Docker images for each service and then start all containers. The initial build process may take several minutes depending on your internet connection and system resources.
    ```bash
    docker-compose up --build
    ```

### Accessing the Application

Once all services are up and running, you can access them via your web browser or API clients:

*   **Frontend Application:** Navigate to `http://localhost:3000` (This port is typically exposed by the `frontend-nextjs` service. Check `docker-compose.yml` if different).
*   **Java Backend API:** Access the backend service APIs at `http://localhost:8080` (Check `docker-compose.yml` for the exact port).
*   **Python Compute API:** Interact with the compute service APIs at `http://localhost:8000` (Check `docker-compose.yml` for the exact port).

## Project Structure

```
.
├── .gitignore                      # Specifies intentionally untracked files to ignore
├── docker-compose.yml              # Defines and configures the multi-service Docker environment
├── agents/                         # Python-based AI agents and orchestration scripts
│   ├── venv/                       # Python virtual environment (ignored by Git)
│   ├── architect.py                # Agent for architectural tasks
│   ├── compute_agent.py            # Agent for compute-related tasks
│   ├── devops_agent.py             # Agent for DevOps tasks
│   ├── enterprise_agent.py         # Agent for enterprise-specific logic
│   ├── father_agent.py             # Core orchestration agent
│   ├── frontend_agent.py           # Agent for frontend-related tasks
│   ├── list_models.py              # Script for listing models
│   ├── mother_agent.py             # Core orchestration agent
│   ├── pipeline_state.json         # Stores state of pipelines
│   ├── prompt_for_*.txt            # Text prompts for various agents
│   ├── qa_agent.py                 # Agent for QA and testing
│   ├── run_all.py                  # Script to run all agents/services
│   ├── synthesizer.py              # Agent for synthesizing information
│   └── system_blueprint.json       # Defines the system's overall blueprint
├── backend-java/                   # Java Spring Boot backend service
│   ├── Dockerfile                  # Docker build instructions for the backend
│   ├── pom.xml                     # Maven project configuration and dependencies
│   └── src/                        # Source code, resources, and tests
│       ├── main/
│       │   ├── java/               # Java source files (com.b2b.*)
│       │   └── resources/          # Application properties, SQL schemas
│       └── test/                   # Java test files
├── compute-python/                 # Python FastAPI compute service
│   ├── config.py                   # Configuration settings for the service
│   ├── Dockerfile                  # Docker build instructions for the compute service
│   ├── main.py                     # Main application entry point
│   ├── requirements.txt            # Python dependencies
│   ├── routers/                    # Defines API endpoints and routing logic
│   ├── schemas/                    # Pydantic models for request/response data validation
│   └── services/                   # Business logic and external service integrations (e.g., hunter, scorer)
├── frontend-nextjs/                # Next.js frontend application
│   ├── Dockerfile                  # Docker build instructions for the frontend
│   ├── app/                        # Next.js App Router for pages and layouts (e.g., auth, dashboard)
│   ├── components/                 # Reusable React components (e.g., Sidebar, Toast)
│   ├── context/                    # React Context API for global state management (e.g., AuthContext)
│   ├── lib/                        # Utility functions and API client configurations (e.g., api.ts)
│   ├── styles/                     # Global CSS styles (e.g., globals.css)
│   └── types/                      # TypeScript type definitions (e.g., index.ts)
└── qa-tests/                       # Centralized directory for Quality Assurance test suites
    ├── compute/                    # Tests specifically for the compute-python service
    │   └── test_compute_engine.py
    ├── enterprise/                 # Tests specifically for the backend-java service
    │   └── src/
    │       └── test/
    │           └── java/
    └── frontend/                   # Tests specifically for the frontend-nextjs application
        └── frontend/
            └── __tests__/
                └── NextJS_Frontend_test_suite.test.js
```

## Usage

*   **Interacting with the Frontend:** Once the Docker containers are running, open your web browser and navigate to the frontend URL (e.g., `http://localhost:3000`). You can then interact with the application, log in, navigate dashboards, and utilize features like the lead hunter.
*   **API Interactions:** For direct interaction with the backend or compute APIs, you can use tools like Postman, Insomnia, or `curl`. Refer to the specific service's documentation or source code (e.g., `compute-python/routers/compute.py`) for available endpoints and expected request/response formats.
*   **Agent Operations:** The AI agents are designed to run autonomously within their service context as defined by Docker Compose. For development or debugging, individual agent scripts within the `agents/` directory can be executed manually within their Python environment.

## Running Tests

To ensure the stability and correctness of the application, dedicated test suites are provided for each service.

1.  **Ensure Services are Running:** For integration or end-to-end tests, make sure all relevant services are up and accessible via `docker-compose up`. For unit tests, services might not need to be running.
2.  **Execute Tests:**
    *   **For Python Compute Service:**
        ```bash
        docker compose exec compute-python pytest /app/qa-tests/compute/
        ```
    *   **For Java Backend Service:**
        ```bash
        docker compose exec backend-java mvn test # If qa-tests/enterprise is part of backend-java's Maven project
        # Alternatively, if tests are run from a separate container or environment:
        # docker compose exec qa-java-runner mvn test /app/qa-tests/enterprise/
        ```
    *   **For Next.js Frontend:**
        ```bash
        docker compose exec frontend-nextjs npm test # Or `yarn test`
        ```
    *(Note: The exact `docker compose exec` commands and test paths might need slight adjustments based on the Dockerfile's `WORKDIR` and how the `qa-tests` volume is mounted or copied into each service's container.)*

## Contributing

We welcome contributions to this project! Please follow these guidelines:

1.  **Fork the repository.**
2.  **Create a new feature branch:** `git checkout -b feature/your-feature-name`
3.  **Implement your changes.**
4.  **Write and run relevant tests** to ensure your changes work as expected and don't introduce regressions.
5.  **Commit your changes** with a clear and concise message: `git commit -m 'feat: Add new awesome feature'`
6.  **Push your branch** to your forked repository: `git push origin feature/your-feature-name`
7.  **Open a Pull Request** against the main repository, describing your changes and their benefits.

## License

This project is open-sourced under the MIT License. See the `LICENSE` file (if present) for full details.
