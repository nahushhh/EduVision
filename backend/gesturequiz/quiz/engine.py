import random
from .questions import QUESTIONS

class QuizEngine:
    def __init__(self):
        self.score = 0
        self.streak = 0
        self.questions = QUESTIONS.copy()
        random.shuffle(self.questions)
        self.current_idx = 0
        
    def get_current_question(self):
        if self.current_idx >= len(self.questions):
            return None # Game Over
        return self.questions[self.current_idx]
        
    def submit_answer(self, zone):
        q = self.get_current_question()
        if not q: return False
        
        is_correct = (zone == q["ans"])
        
        if is_correct:
            self.score += 10 + (self.streak * 2)
            self.streak += 1
        else:
            self.streak = 0
            
        self.current_idx += 1
        return is_correct
