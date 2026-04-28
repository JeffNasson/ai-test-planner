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

User Input → AI Generation → Validation → Execution → Reporting → Storage


## Architecture
```
framework/
ai/            test generation
validation/    scoring + quality checks
execution/     Playwright runner
assertions/    result validation
data/          persistence layer
reporting/     logs + CI output

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
