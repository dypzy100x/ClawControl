"""
Guardrails Engine - Soft alert mode
"""
import uuid
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import deque
from clawcontrol.core.config import config
from clawcontrol.core.constants import VIOLATIONS_LOG_FILE
from clawcontrol.api.models import GuardRule, ViolationEvent, GuardRuleCreate


class GuardrailsEngine:
    """
    Manages guardrail rules and evaluates violations.
    
    SOFT ALERT MODE: Violations are logged and surfaced via API
    but do NOT trigger automatic OpenClaw termination.
    """
    
    def __init__(self):
        self.rules: Dict[str, GuardRule] = {}
        self.violations: deque = deque(maxlen=1000)
        self.action_timestamps: deque = deque(maxlen=1000)
        self.violations_log = VIOLATIONS_LOG_FILE
        self.violations_log.parent.mkdir(parents=True, exist_ok=True)
        self._load_rules()
    
    def _load_rules(self):
        """Load rules from config file"""
        rules_data = config.load_json_file(config.rules_file, default={"rules": []})
        
        for rule_data in rules_data.get("rules", []):
            try:
                rule = GuardRule(**rule_data)
                self.rules[rule.id] = rule
            except Exception as e:
                print(f"Error loading rule: {e}")
    
    def _save_rules(self):
        """Save rules to config file"""
        rules_data = {
            "rules": [rule.model_dump() for rule in self.rules.values()]
        }
        config.save_json_file(config.rules_file, rules_data)
    
    def _log_violation(self, violation: ViolationEvent):
        """Persist violation to log file"""
        try:
            with open(self.violations_log, 'a') as f:
                log_entry = {
                    "ts": violation.ts.isoformat(),
                    "rule_id": violation.rule_id,
                    "log_excerpt": violation.log_excerpt,
                    "severity": violation.severity
                }
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Error logging violation: {e}")
    
    def get_all_rules(self) -> List[GuardRule]:
        """Get all guardrail rules"""
        return list(self.rules.values())
    
    def get_rule(self, rule_id: str) -> Optional[GuardRule]:
        """Get specific rule by ID"""
        return self.rules.get(rule_id)
    
    def create_rule(self, rule_create: GuardRuleCreate) -> GuardRule:
        """Create new guardrail rule"""
        rule_id = str(uuid.uuid4())
        rule = GuardRule(
            id=rule_id,
            **rule_create.model_dump()
        )
        
        self.rules[rule_id] = rule
        self._save_rules()
        
        return rule
    
    def update_rule(self, rule_id: str, rule_data: dict) -> Optional[GuardRule]:
        """Update existing rule"""
        if rule_id not in self.rules:
            return None
        
        current_rule = self.rules[rule_id]
        updated_data = current_rule.model_dump()
        updated_data.update(rule_data)
        
        self.rules[rule_id] = GuardRule(**updated_data)
        self._save_rules()
        
        return self.rules[rule_id]
    
    def delete_rule(self, rule_id: str) -> bool:
        """Delete rule by ID"""
        if rule_id in self.rules:
            del self.rules[rule_id]
            self._save_rules()
            return True
        return False
    
    def evaluate_log_line(self, log_line: str) -> Optional[ViolationEvent]:
        """
        Evaluate log line against rules (SOFT ALERT MODE)
        
        Violations are logged and returned but do NOT trigger
        automatic process termination.
        """
        for rule in self.rules.values():
            if not rule.enabled:
                continue
            
            for pattern in rule.block_patterns:
                if pattern.lower() in log_line.lower():
                    violation = ViolationEvent(
                        ts=datetime.now(),
                        rule_id=rule.id,
                        log_excerpt=log_line[:200],
                        severity="warning"
                    )
                    self.violations.append(violation)
                    self._log_violation(violation)
                    return violation
        
        return None
    
    def check_rate_limit(self, rule_id: str) -> bool:
        """Check if rate limit is exceeded"""
        rule = self.rules.get(rule_id)
        if not rule:
            return False
        
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        self.action_timestamps = deque(
            [ts for ts in self.action_timestamps if ts > one_minute_ago],
            maxlen=1000
        )
        
        if len(self.action_timestamps) >= rule.rate_limit_per_min:
            return True
        
        self.action_timestamps.append(datetime.now())
        return False
    
    def get_violations(self, since: Optional[datetime] = None, limit: int = 100) -> List[ViolationEvent]:
        """Get violations with optional filtering"""
        violations = list(self.violations)
        
        if since:
            violations = [v for v in violations if v.ts >= since]
        
        return violations[-limit:]


guardrails_engine = GuardrailsEngine()
