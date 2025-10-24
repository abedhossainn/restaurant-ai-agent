# Restaurant Recommendation AI Agent

An intelligent AI agent that finds restaurants based on natural language queries using search algorithms, constraint satisfaction, and deterministic planning.

## Agent Architecture

This agent combines goal based planning, constraint satisfaction, and utility based ranking:

- Goal based pipeline: A deterministic 7-state flow (INIT > PARSING > SEARCHING > FILTERING > RANKING > EXPLAINING > COMPLETE) drives the agent to the goal of returning the best matching restaurants.
- NLP parameter extraction: Google Gemini parses the user's natural language into structured parameters (cuisine, location, price, party size, special requests).
- Constraint Satisfaction (hard filters): Applies boolean constraints to the dataset (exact cuisine match, location substring match, price threshold, features like window seating or views).
- Utility based ranking: After filtering, candidates are scored with a weighted function: high rating boosts, distance and higher prices penalize, and view features add a bonus. Results are sorted by total utility.
- Explanation generation: Gemini produces a concise, user facing explanation describing why the top results match the query.
- Failure handling: If no rows remain after filtering or the CSV cannot be loaded, the agent returns a “no results” message.

- **Multi-constraint filtering** - Location, cuisine, price, features (window seating, views)

An intelligent AI agent that finds restaurants based on complex natural language queries using search algorithms, constraint satisfaction, and deterministic planning.- **Weighted relevance scoring** - Ranks results by rating, distance, price, and special features

- **Detailed decision logging** - Shows agent's reasoning at each step

## Features

- **Natural Language Processing** - Understands complex queries using Google Gemini LLM## Quick Start

- **Multi-Constraint Filtering** - Filters by cuisine, location, price, and special features

- **Weighted Ranking** - Scores restaurants based on rating, distance, price, and amenities### 1. Start the Application

- **Deterministic State Machine** - 7-state agent pipeline with transparent decision logging```bash

- **Real-time Status Updates** - Visual feedback during query processingcd "/home/abed/SENG/691 Agentic AI/Assignment 3"

- **Docker-based Deployment** - One-command setup with Docker Composedocker-compose up -d

## Deployment Guide

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Google Gemini API Key](https://ai.google.dev/)

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/abedhossainn/restaurant-ai-agent.git
   cd restaurant-ai-agent
   ```
2. **Start the application**
   ```bash
   docker compose up -d
   ```
3. **Access the web interface**
   - Open your browser and go to: http://localhost:3000
4. **Install the agent function**
   - In Open WebUI, go to Admin Panel → Functions → + Create New Function
   - Copy contents from `openwebui/functions/restaurant_agent.py` and paste
   - Set your Gemini API key and CSV path in the Valves section
   - Save and enable the function
5. **Start chatting!**
   - Create a new chat, select the agent, and ask for restaurant recommendations.
   - Configure the **Valves**:**Basic Query:**
