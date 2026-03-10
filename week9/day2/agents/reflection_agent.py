from autogen import ConversableAgent

class ReflectionAgent(ConversableAgent):
    """
    Creating the ReflectionAgent class.
    This agent reviews outputs from workers and suggests improvements.
    Inherits from ConversableAgent.
    """
    def __init__(self, name, llm_config, system_message="You are a reflection agent. Critique the provided solution and suggest improvements."):
        # Initializing the ReflectionAgent.
        super().__init__(
            name=name,
            llm_config=llm_config,
            system_message=system_message,
            human_input_mode="NEVER",
        )
        print(f"Adding ReflectionAgent: {name}")

    def reflect(self, task_output):
        # Reflecting on the output to improve it.
        print(f"Reflection agent {self.name} is critiquing the output...")
        # Simulated reflection logic.
        return f"Refined and improved output based on: {task_output}"
