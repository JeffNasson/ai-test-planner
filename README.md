# AI-Driven QA Automation Framework

## Overview
This project is a modular QA automation framework built with Python and Playwright. It combines AI-generated test cases with data-driven execution and structured reporting.

## Features
- AI-generated test cases (positive, negative, edge)
- JSON-based test persistence and replay
- Data-driven testing architecture
- Simulated API-based test data generation
- Environment configuration (dev/staging/prod)
- Structured assertion system
- Test reporting (TXT + JSON)

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

## How to Run
1. Create .env file:
   ENV=dev

2. Run:
   python main.py

## Example Output
- PASS / FAIL results
- Metrics (pass rate, totals)
- Saved reports in /test_results


## CI Status

![Tests](https://github.com/JeffNasson/ai-test-planner/actions/workflows/tests.yml/badge.svg)
