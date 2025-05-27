class LLMNPCBrain:
    def __init__(self, name: str, personality: str):
        self.name = name
        self.personality = personality
        self.memory: list[str] = []

    def observe(self, event: str):
        self.memory.append(event)

    def decide_action(self):
        if len(self.memory) > 5:
            return "reflect"
        return "wander"

    def speak(self):
        return f"My name is {self.name}. I am {self.personality}."
