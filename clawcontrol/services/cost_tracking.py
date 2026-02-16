"""Cost Tracking - API usage and cost monitoring"""
from datetime import datetime
from typing import Dict
from collections import defaultdict

class CostTracker:
    def __init__(self):
        self.daily_costs = defaultdict(float)
        self.monthly_budget = 0
        self.token_usage = {"input": 0, "output": 0}
    
    def track_tokens(self, input_tokens: int, output_tokens: int, model: str = "gpt-4"):
        self.token_usage["input"] += input_tokens
        self.token_usage["output"] += output_tokens
        
        # Simple pricing (update with real prices)
        cost = (input_tokens * 0.00003) + (output_tokens * 0.00006)
        
        today = datetime.now().date().isoformat()
        self.daily_costs[today] += cost
        
        return cost
    
    def set_budget(self, monthly_budget: float):
        self.monthly_budget = monthly_budget
    
    def get_current_spend(self) -> float:
        return sum(self.daily_costs.values())
    
    def check_budget_status(self) -> Dict:
        current = self.get_current_spend()
        if self.monthly_budget == 0:
            return {"status": "no_budget_set"}
        
        percent = (current / self.monthly_budget) * 100
        
        if percent > 100:
            status = "exceeded"
        elif percent > 90:
            status = "warning"
        elif percent > 75:
            status = "on_track"
        else:
            status = "under_budget"
        
        return {
            "status": status,
            "current_spend": current,
            "budget": self.monthly_budget,
            "percent_used": percent
        }

cost_tracker = CostTracker()
