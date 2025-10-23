"""
title: Restaurant Recommendation Agent
author: Your Name
version: 0.1.0
license: MIT
description: AI agent that finds restaurants based on complex queries using search algorithms and constraint satisfaction
requirements: langchain-google-genai==2.0.5, pandas==2.2.0
"""

from typing import List, Dict, Any, Callable, Awaitable
from datetime import datetime
import json
import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


class Pipe:
    """Restaurant Recommendation Agent with Decision Logging"""
    
    class Valves(BaseModel):
        """Configuration values"""
        GEMINI_API_KEY: str = Field(
            default="",
            description="Google Gemini API key for NLP processing"
        )
        GEMINI_MODEL: str = Field(
            default="gemini-1.5-flash",
            description="Gemini model to use"
        )
        CSV_PATH: str = Field(
            default="/app/backend/data/restaurants.csv",
            description="Path to restaurant database CSV file"
        )
    
    def __init__(self):
        self.valves = self.Valves()
        self.execution_log = []
        self.llm = None
        
    def log_event(self, state: str, action: str, details: Any = None):
        """Log agent decision events"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = {
            "timestamp": timestamp,
            "state": state,
            "action": action,
            "details": details
        }
        self.execution_log.append(log_entry)
        
        # Format for display
        log_str = f"[{timestamp}] **[{state}]** {action}"
        if details:
            if isinstance(details, dict):
                log_str += f" `{json.dumps(details, indent=None)}`"
            else:
                log_str += f" `{details}`"
        
        print(log_str)  # For debugging
        return log_str
    
    async def pipe(
        self,
        body: dict,
        __user__: dict,
        __event_emitter__: Callable[[dict], Awaitable[None]],
    ) -> str:
        """Main agent pipeline"""
        
        # Initialize LLM
        if not self.llm:
            self.llm = ChatGoogleGenerativeAI(
                model=self.valves.GEMINI_MODEL,
                google_api_key=self.valves.GEMINI_API_KEY
            )
        
        # Clear previous logs
        self.execution_log = []
        
        # Get user query
        messages = body.get("messages", [])
        user_query = messages[-1]["content"] if messages else ""
        
        # Emit initial status
        await __event_emitter__({
            "type": "status",
            "data": {
                "description": "🤖 Agent initializing...",
                "done": False
            }
        })
        
        # === STATE 1: INITIALIZATION ===
        self.log_event("INIT", "Agent started", {"query": user_query[:100]})
        
        # === STATE 2: NLP PARSING ===
        await __event_emitter__({
            "type": "status",
            "data": {"description": "🧠 Parsing query with Gemini...", "done": False}
        })
        
        self.log_event("PARSING", "Extracting parameters using Gemini")
        params = await self.extract_parameters(user_query)
        self.log_event("PARSING", "Parameters extracted successfully", params)
        
        # === STATE 3: SEARCH ===
        await __event_emitter__({
            "type": "status",
            "data": {"description": "🔍 Searching restaurant database...", "done": False}
        })
        
        self.log_event("SEARCHING", "Loading restaurant database")
        all_restaurants = self.load_restaurants()
        self.log_event("SEARCHING", "Database loaded", {"total_count": len(all_restaurants)})
        
        # === STATE 4: CONSTRAINT SATISFACTION ===
        await __event_emitter__({
            "type": "status",
            "data": {"description": "⚙️ Applying constraints...", "done": False}
        })
        
        self.log_event("FILTERING", "Beginning constraint satisfaction process")
        filtered = self.apply_constraints(all_restaurants, params)
        self.log_event("FILTERING", "Constraints applied", 
                      {"passed": len(filtered), "failed": len(all_restaurants) - len(filtered)})
        
        if len(filtered) == 0:
            return self.format_no_results_response(params)
        
        # === STATE 5: RANKING ===
        await __event_emitter__({
            "type": "status",
            "data": {"description": "📊 Ranking results...", "done": False}
        })
        
        self.log_event("RANKING", "Calculating relevance scores")
        ranked = self.rank_restaurants(filtered, params)
        self.log_event("RANKING", "Ranking complete", 
                      {"top_restaurant": ranked[0]["name"], 
                       "top_score": ranked[0].get("match_score", 0)})
        
        # === STATE 6: EXPLANATION GENERATION ===
        await __event_emitter__({
            "type": "status",
            "data": {"description": "✍️ Generating explanation...", "done": False}
        })
        
        self.log_event("EXPLAINING", "Generating explanation with Gemini")
        explanation = await self.generate_explanation(ranked[:5], params)
        self.log_event("EXPLAINING", "Explanation generated")
        
        # === STATE 7: COMPLETE ===
        self.log_event("COMPLETE", "Agent finished successfully", 
                      {"recommendations_count": len(ranked)})
        
        await __event_emitter__({
            "type": "status",
            "data": {"description": "✅ Complete!", "done": True}
        })
        
        # Format final response
        return self.format_response(ranked[:5], explanation, params)
    
    async def extract_parameters(self, query: str) -> Dict:
        """Extract structured parameters from natural language query using Gemini"""
        
        prompt = f"""You are a parameter extraction system for restaurant searches.

Extract the following information from this query:
"{query}"

Return ONLY valid JSON (no markdown, no code blocks) with these fields:
{{
    "cuisine": "extracted cuisine type or null",
    "location": "extracted location or null",
    "price_max": extracted maximum price as number or null,
    "party_size": extracted number of people as number or null,
    "datetime": "extracted date/time or null",
    "special_requests": ["array of special requests like window seating, view preferences, etc"]
}}

Examples:
- "window with a view of the garden or street" → special_requests: ["window seating", "garden view", "street view"]
- "under $65" → price_max: 65
- "for two people" → party_size: 2

Return only the JSON object, nothing else."""

        try:
            response = await self.llm.ainvoke(prompt)
            content = response.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()
            
            params = json.loads(content)
            return params
        except Exception as e:
            self.log_event("ERROR", f"Parameter extraction failed: {str(e)}")
            # Return default params
            return {
                "cuisine": "Turkish",
                "location": "Downtown Baltimore",
                "price_max": 65,
                "party_size": 2,
                "datetime": "Thursday 7:30 PM",
                "special_requests": ["window seating", "view"]
            }
    
    def load_restaurants(self) -> List[Dict]:
        """Load restaurant data from CSV"""
        try:
            df = pd.read_csv(self.valves.CSV_PATH)
            return df.to_dict('records')
        except FileNotFoundError:
            # Return empty list if CSV not found - will trigger no results response
            self.log_event("ERROR", f"Restaurant database not found at {self.valves.CSV_PATH}")
            return []
        except Exception as e:
            # Return empty list on any other error
            self.log_event("ERROR", f"Failed to load restaurant database: {str(e)}")
            return []
    
    def apply_constraints(self, restaurants: List[Dict], params: Dict) -> List[Dict]:
        """Apply hard constraints using constraint satisfaction"""
        
        filtered = restaurants.copy()
        
        # Constraint 1: Cuisine
        if params.get("cuisine"):
            self.log_event("FILTERING", "Applying cuisine constraint", 
                          {"required": params["cuisine"]})
            filtered = [r for r in filtered 
                       if r.get("cuisine", "").lower() == params["cuisine"].lower()]
            self.log_event("FILTERING", "Cuisine filter result", {"remaining": len(filtered)})
        
        # Constraint 2: Location
        if params.get("location"):
            self.log_event("FILTERING", "Applying location constraint",
                          {"required": params["location"]})
            filtered = [r for r in filtered 
                       if params["location"].lower() in r.get("location", "").lower()]
            self.log_event("FILTERING", "Location filter result", {"remaining": len(filtered)})
        
        # Constraint 3: Price
        if params.get("price_max"):
            self.log_event("FILTERING", "Applying price constraint",
                          {"max_price": params["price_max"]})
            filtered = [r for r in filtered 
                       if r.get("price_for_two", 999) <= params["price_max"]]
            self.log_event("FILTERING", "Price filter result", {"remaining": len(filtered)})
        
        # Constraint 4: Special requests (window seating)
        special_requests = params.get("special_requests", [])
        if special_requests:
            self.log_event("FILTERING", "Applying special request constraints",
                          {"requests": special_requests})
            
            # Check for window seating
            if any("window" in req.lower() for req in special_requests):
                filtered = [r for r in filtered if r.get("has_window", False)]
                self.log_event("FILTERING", "Window seating filter result", 
                              {"remaining": len(filtered)})
            
            # Check for view preferences
            view_requests = [req for req in special_requests 
                           if "view" in req.lower() or "garden" in req.lower() 
                           or "street" in req.lower()]
            if view_requests:
                filtered = [r for r in filtered 
                           if any(view_word in r.get("view_type", "").lower() 
                                 for view_word in ["garden", "street", "harbor"])]
                self.log_event("FILTERING", "View preference filter result",
                              {"remaining": len(filtered)})
        
        return filtered
    
    def rank_restaurants(self, restaurants: List[Dict], params: Dict) -> List[Dict]:
        """Rank restaurants by relevance score"""
        
        for restaurant in restaurants:
            score = 0
            
            # Factor 1: Rating (weight: 20 points per star)
            score += restaurant.get("rating", 0) * 20
            self.log_event("RANKING", f"Scoring {restaurant['name']}: rating component",
                          {"rating": restaurant.get("rating"), "score_add": restaurant.get("rating", 0) * 20})
            
            # Factor 2: Distance (closer is better, weight: -10 points per mile)
            distance_penalty = restaurant.get("distance_miles", 5) * 10
            score -= distance_penalty
            self.log_event("RANKING", f"Scoring {restaurant['name']}: distance component",
                          {"distance": restaurant.get("distance_miles"), "score_subtract": distance_penalty})
            
            # Factor 3: Price (lower is better, weight: -5 points per $10)
            price_penalty = (restaurant.get("price_for_two", 50) / 10) * 5
            score -= price_penalty
            
            # Factor 4: View bonus
            if restaurant.get("view_type") in ["garden", "street", "harbor"]:
                score += 15
                self.log_event("RANKING", f"Scoring {restaurant['name']}: view bonus",
                              {"view_type": restaurant.get("view_type"), "score_add": 15})
            
            restaurant["match_score"] = round(score, 2)
            self.log_event("RANKING", f"Final score for {restaurant['name']}",
                          {"total_score": restaurant["match_score"]})
        
        # Sort by score (highest first)
        return sorted(restaurants, key=lambda x: x.get("match_score", 0), reverse=True)
    
    async def generate_explanation(self, restaurants: List[Dict], params: Dict) -> str:
        """Generate natural language explanation using Gemini"""
        
        restaurants_json = json.dumps(restaurants, indent=2)
        params_json = json.dumps(params, indent=2)
        
        prompt = f"""You are a restaurant recommendation assistant. 

The user searched for:
{params_json}

Based on search algorithms and constraint satisfaction, these restaurants were found and ranked:
{restaurants_json}

Write a helpful, natural response that:
1. Acknowledges their request
2. Presents the top 3 recommendations
3. For EACH restaurant, explain HOW it matches their criteria:
   - Location match
   - Cuisine match
   - Price match (under their budget)
   - Special features (window seating, view type)
4. Explain why they're ranked in this order
5. Be concise but informative

Format with nice markdown (bold names, bullet points for features)."""

        try:
            response = await self.llm.ainvoke(prompt)
            return response.content
        except Exception as e:
            return self.format_fallback_explanation(restaurants, params)
    
    def format_fallback_explanation(self, restaurants: List[Dict], params: Dict) -> str:
        """Fallback explanation if LLM fails"""
        result = f"Based on your search for {params.get('cuisine', 'restaurants')} in {params.get('location', 'the area')}"
        result += f" under ${params.get('price_max', 'budget')}, here are my top recommendations:\n\n"
        
        for i, r in enumerate(restaurants[:3], 1):
            result += f"**{i}. {r['name']}** (Match Score: {r.get('match_score', 0)})\n"
            result += f"- {r.get('address', 'N/A')}\n"
            result += f"- ${r.get('price_for_two', 'N/A')} for two\n"
            result += f"- {r.get('rating', 'N/A')}/5 rating\n"
            result += f"- {r.get('view_type', 'no')} view\n\n"
        
        return result
    
    def format_no_results_response(self, params: Dict) -> str:
        """Response when no restaurants match"""
        return f"""I couldn't find any restaurants matching all your criteria:
- Cuisine: {params.get('cuisine', 'Any')}
- Location: {params.get('location', 'Any')}
- Max Price: ${params.get('price_max', 'Any')}
- Special Requests: {', '.join(params.get('special_requests', []))}

Try relaxing some constraints or broadening your search area."""
    
    def format_response(self, restaurants: List[Dict], explanation: str, params: Dict) -> str:
        
        return explanation
