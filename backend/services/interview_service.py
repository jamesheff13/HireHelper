from services.ai_service import generate_question, generate_feedback

class InterviewService:
    def __init__(self):
        self.role = None
        self.history = []
        self.current_question = None

    def start(self, role):
        self.role = role
        self.history = []
        self.current_question = generate_question(self.role, self.history)

    def next(self, answer):
        if self.current_question and answer:
            self.history.append((self.current_question, answer))
        self.current_question = generate_question(self.role, self.history)
        return self.current_question

    def finish(self):
        if self.current_question:
            self.history.append((self.current_question, ""))  # Save last question if no answer
        feedback = generate_feedback(self.role, self.history)
        self.role = None
        self.history = []
        self.current_question = None
        return feedback