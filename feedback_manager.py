import json
import os
from typing import List, Dict, Optional
from config import Config

class FeedbackManager:
    def __init__(self):
        self.file_path = Config.FEEDBACK_FILE
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.history = self._load_history()

    def _load_history(self) -> List[Dict]:
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except:
            return []

    def store_feedback(self, query: str, bot_response: str, feedback_type: str, correction: Optional[str] = None):
        entry = {
            "query": query,
            "bot_response": bot_response,
            "feedback_type": feedback_type,
            "correction": correction
        }
        self.history.append(entry)
        with open(self.file_path, 'w') as f:
            json.dump(self.history, f, indent=2)

    def get_correction_for_pattern(self, query: str) -> Optional[Dict]:
        for entry in reversed(self.history):
            if entry['query'].strip().lower() == query.strip().lower() and entry.get('correction'):
                return entry
        return None
        
    def get_stats(self):
        total = len(self.history)
        positive = len([x for x in self.history if x['feedback_type'] == 'positive'])
        corrections = len([x for x in self.history if x.get('correction')])
        return {"total": total, "positive": positive, "corrections": corrections}