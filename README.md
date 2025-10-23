# Restaurant Recommendation AI Agent

An intelligent AI agent that finds restaurants based on natural language queries using search algorithms, constraint satisfaction, and deterministic planning.
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
3. **Access the web interface**
   - Open your browser and go to: http://localhost:3000
4. **Install the agent function**
   - In Open WebUI, go to Admin Panel → Functions → + Create New Function
   - Copy contents from `openwebui/functions/restaurant_agent.py` and paste
   - Set your Gemini API key and CSV path in the Valves section
   - Save and enable the function
5. **Start chatting!**
   - Create a new chat, select the agent, and ask for restaurant recommendations.
# 🍽️ Restaurant Recommendation AI Agent# Restaurant Recommendation AI Agent



[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)AI agent that finds restaurants based on complex natural language queries using search algorithms, constraint satisfaction, and deterministic planning.

[![Docker](https://img.shields.io/badge/Docker-Required-2496ED.svg)](https://www.docker.com/)

[![Open WebUI](https://img.shields.io/badge/Open_WebUI-Latest-green.svg)](https://github.com/open-webui/open-webui)## Features

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)- **Natural language query understanding** - Extracts parameters from complex queries using Gemini LLM

- **Multi-constraint filtering** - Location, cuisine, price, features (window seating, views)

An intelligent AI agent that finds restaurants based on complex natural language queries using search algorithms, constraint satisfaction, and deterministic planning.- **Weighted relevance scoring** - Ranks results by rating, distance, price, and special features

- **Detailed decision logging** - Shows agent's reasoning at each step

## ✨ Features- **Real-time status updates** - Visual feedback during query processing



- **Natural Language Processing** - Understands complex queries using Google Gemini LLM## Quick Start

- **Multi-Constraint Filtering** - Filters by cuisine, location, price, and special features

- **Weighted Ranking** - Scores restaurants based on rating, distance, price, and amenities### 1. Start the Application

- **Deterministic State Machine** - 7-state agent pipeline with transparent decision logging```bash

- **Real-time Status Updates** - Visual feedback during query processingcd "/home/abed/SENG/691 Agentic AI/Assignment 3"

- **Docker-based Deployment** - One-command setup with Docker Composedocker-compose up -d

```

## Quick Start

### 2. Access Open WebUI

### PrerequisitesOpen your browser and navigate to: **http://localhost:3000**



- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)### 3. Install the Agent Function

- [Google Gemini API Key](https://ai.google.dev/) (free tier available)1. Create an account (local only, no email needed)

2. Click your profile icon (bottom left)

### Installation3. Click "Admin Panel"

4. Click "Functions" in the sidebar

1. **Clone the repository**5. Click "+ Create New Function"

   ```bash6. Copy the entire contents of `openwebui/functions/restaurant_agent.py`

   git clone https://github.com/yourusername/restaurant-ai-agent.git7. Paste into the editor

   cd restaurant-ai-agent8. Scroll to the "Valves" section at the bottom

   ```9. Set `GEMINI_API_KEY` to your API key (already in .env)

10. Set `CSV_PATH` to `/app/backend/data/restaurants.csv`

2. **Start the application**11. Click "Save"
# Restaurant Recommendation AI Agent

An intelligent AI agent that finds restaurants based on natural language queries using search algorithms, constraint satisfaction, and deterministic planning.

## Deployment Guide

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Google Gemini API Key](https://ai.google.dev/)

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/restaurant-ai-agent.git
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
