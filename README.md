## AI-Driven QA Test Planner

## Overview

This project is a modular QA automation framework that generates, validates, executes, and reports test cases using AI.

It models a production-style testing pipeline with dynamic test generation, quality validation, Playwright-based execution, and CI integration for automated test runs and reporting.

Includes a validation feedback loop that iteratively improves AI-generated tests until quality thresholds are met.


## How It Works

1. **User Input**  
   Provide a testing task (e.g., "Test login functionality")

2. **AI Generation**  
   Generates structured test cases (positive, negative, edge cases)

3. **Validation**  
   Scores and validates test case quality

4. **Feedback Loop**  
   Retries with feedback when validation fails

5. **Execution**  
   Executes validated test cases using Playwright

6. **Assertions**  
   Verifies expected outcomes

7. **Reporting and Storage**  
   Logs and persists results (JSON and logs)

## Pipeline

User Input → AI Generation → Validation → Retry Feedback Loop → Execution → Reporting → Storage


## CI/CD Integration

This project includes a GitHub Actions-based CI pipeline that:

- Automatically runs tests on every push and pull request
- Executes Playwright tests in a headless environment
- Generates structured test results (TXT + JSON)
- Uploads test artifacts for inspection directly in GitHub
- Fails the pipeline on test failures to prevent bad code from passing

This simulates a real-world QA workflow where automated tests act as a quality gate before changes are merged.

## Continuous Integration Workflow

On each push or pull request:

1. GitHub Actions spins up a clean environment
2. Installs dependencies (Playwright, Python packages)
3. Executes saved test cases
4. Generates reports
5. Uploads artifacts for debugging and traceability
6. Marks the build as pass/fail based on results

This ensures consistent, repeatable test execution across environments.

## Architecture
AI → JSON → Validation → Data Manager → Executor → Assertions → Reporting → CI Pipeline

orchestrator/
pipeline.py    main system flow

config/
config.py      environment + paths
```

## Key Features

- AI-generated test cases (positive, negative, edge cases)
- Validation with scoring and retry feedback loop
- Playwright-based test execution
- Decoupled assertion logic
- JSON-based persistence for replayable test runs
- CI pipeline (GitHub Actions) for automated test execution
- Confidence-based validation gating prevents low-quality AI-generated tests from executing.

## Observability and Validation Telemetry
The framework includes structured validation telemetry for tracking:
- confidence scoring
- retry history
- validation rule frequency
- AI recovery behavior
- workflow-level metrics
- attempt-level metrics


## Running the Project
```
	1.	Clone the repository
            git clone https://github.com/JeffNasson/ai-test-planner.git
            cd ai-test-planner
	2.	Install dependencies
            pip install -r requirements.txt
	3.	Install Playwright browsers
            playwright install
	4.	Run the pipeline
            python main.py
```

## Design Diagram
                ┌────────────────────┐
                │      User Input    │
                │   (CLI / Task)     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   AI Engine        │
                │ (generate tests)   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   Validator        │
                │ (score + feedback) │
                └─────────┬──────────┘
                          │
                ┌─────────▼──────────┐
                │ Retry w/ Feedback  │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   Test Executor    │
                │  (Playwright)      │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   Assertions       │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   Reporting        │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │  Results Storage   │
                │ (JSON + Logs)      │
                └────────────────────┘


## CI Status
![Tests](https://github.com/JeffNasson/ai-test-planner/actions/workflows/tests.yml/badge.svg)
