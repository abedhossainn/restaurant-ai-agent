# Setup Instructions

## ✅ Deployment Complete!

Your Restaurant Recommendation AI Agent is now running.

## Access the Application

**Open WebUI URL**: http://localhost:3000

## Next Steps

### 1. Create Account
- Open http://localhost:3000 in your browser
- Create a local account (no email required)
- This is stored locally in the Docker container

### 2. Install the Agent Function

1. Click your **profile icon** (bottom left corner)
2. Click **"Admin Panel"**
3. Click **"Functions"** in the left sidebar
4. Click **"+ Create New Function"** button
5. **Delete** the template code
6. **Copy** the entire contents of: `openwebui/functions/restaurant_agent.py`
7. **Paste** into the code editor
8. Scroll to the bottom to find **"Valves"** section
9. Set the following values:
   - `GEMINI_API_KEY`: `AIzaSyC14gRPUXiJxsX7ICk8nRLsBtprE2TMA4I`
   - `GEMINI_MODEL`: `gemini-1.5-flash` (default is fine)
   - `CSV_PATH`: `/app/backend/data/restaurants.csv`
10. Click **"Save"**
11. **Toggle the switch** to enable the function

### 3. Test the Agent

1. Go back to the main chat interface
2. Click **"+"** to create a new chat
3. Click the **model selector dropdown** (top of chat)
4. Find and select **"Restaurant Recommendation Agent"**
5. Enter this test query:

```
Find a Turkish restaurant in Downtown Baltimore, MD for two people to have dinner under $65 on Thursday night at 7:30 pm with a table for two near a window with a view of the garden or the street.
```

### 4. Observe the Results

You should see:

✅ **Real-time status updates**:
- 🤖 Agent initializing...
- 🧠 Parsing query with Gemini...
- 🔍 Searching restaurant database...
- ⚙️ Applying constraints...
- 📊 Ranking results...
- ✍️ Generating explanation...
- ✅ Complete!

✅ **Natural language explanation** of the top recommendations

✅ **Match analysis** showing how each restaurant satisfies your criteria

✅ **Agent decision log** showing the reasoning process:
- Parameters extracted
- Constraints applied
- Restaurants filtered at each step
- Ranking scores calculated

## Project Files

All project files are in: `/home/abed/SENG/691 Agentic AI/Assignment 3/`

```
├── docker-compose.yml           # Container configuration
├── .env                         # API keys
├── README.md                    # Documentation
├── requirements.txt             # Python dependencies
├── data/
│   ├── restaurants.csv          # Database (12 restaurants)
│   └── data_loader.py           # Utility script
├── openwebui/
│   └── functions/
│       └── restaurant_agent.py  # Main agent code ⭐
└── docs/
    └── architecture.md          # Technical details
```

## Example Queries to Try

**Basic Query:**
```
Find Turkish restaurants in Downtown Baltimore
```

**With Price Constraint:**
```
Show me Turkish places under $50 for two
```

**Complex Query (Full Features):**
```
Find a Turkish restaurant in Downtown Baltimore, MD for two people to have dinner under $65 on Thursday night at 7:30 pm with a table for two near a window with a view of the garden or the street.
```

**No Results Test:**
```
Find Italian restaurants in Downtown Baltimore under $20
```

## Useful Commands

```bash
# View logs
docker logs -f restaurant-agent-ui

# Restart container
docker-compose restart

# Stop container
docker-compose down

# Start container
docker-compose up -d

# Access container shell
docker exec -it restaurant-agent-ui bash
```

## Troubleshooting

### Can't access http://localhost:3000
- Wait 30 seconds for container to fully start
- Check container status: `docker ps`
- Check logs: `docker logs restaurant-agent-ui`

### Function doesn't appear
- Make sure you saved the function
- Make sure you enabled the toggle switch
- Refresh the page

### No results from agent
- Verify the CSV file is in the container: 
  ```bash
  docker exec restaurant-agent-ui ls -la /app/backend/data/
  ```
- Check that GEMINI_API_KEY is set in function valves
- Review the agent logs in the response

### Gemini API errors
- Verify API key is correct
- Check quota at: https://ai.google.dev/

## What Makes This an AI Agent?

This project demonstrates:

✅ **States**: INIT → PARSING → SEARCHING → FILTERING → RANKING → EXPLAINING → COMPLETE

✅ **Actions**: extract_parameters(), load_restaurants(), apply_constraints(), rank_restaurants(), generate_explanation()

✅ **Goals**: Find top 5 restaurants matching ALL constraints, ranked by relevance

✅ **Search Algorithms**: Sequential database search, breadth-first constraint filtering

✅ **Constraint Satisfaction**: Boolean CSP with hard constraints (location, cuisine, price, features)

✅ **Planning**: Deterministic fixed-sequence planning (no backtracking)

✅ **Decision Logging**: Transparent reasoning at every step

See `docs/architecture.md` for detailed technical explanation.

## Ready to Go! 🚀

Your agent is deployed and ready to recommend restaurants!
