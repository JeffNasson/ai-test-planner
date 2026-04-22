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

## Architecture
AI → JSON → Data Manager → Executor → Assertions → Reporting

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
