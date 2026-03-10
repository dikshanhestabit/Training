from autogen import ConversableAgent

class WorkerAgent(ConversableAgent):
    """
    Creating the WorkerAgent class.
    This agent is responsible for executing specific sub-tasks assigned by the Orchestrator.
    It inherits from ConversableAgent to maintain consistency with the AutoGen framework.
    """
    def __init__(self, name, llm_config, system_message="You are a helpful worker agent. Execute the assigned task precisely."):
        # Initializing the WorkerAgent with common configuration.
        super().__init__(
            name=name,
            llm_config=llm_config,
            system_message=system_message,
            human_input_mode="NEVER",
        )
        # Adding a log to track task assignment.
        print(f"Adding WorkerAgent: {name} to the registry.")

    def execute_task(self, task_description):
        # Executing the assigned task.
        print(f"Worker {self.name} is executing: {task_description}")
        # In a real scenario, this would involve a chat or a tool call.
        # For this implementation, we simulate the execution.
        return f"Result from {self.name} for task: {task_description}"
