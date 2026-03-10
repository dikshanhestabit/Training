from autogen import ConversableAgent

class ValidatorAgent(ConversableAgent):
    """
    Creating the ValidatorAgent class.
    This agent performs the final validation check for errors or logic gaps.
    Inherits from ConversableAgent.
    """
    def __init__(self, name, llm_config, system_message="You are a validator agent. Check the final response for accuracy, safety, and correctness."):
        # Initializing the ValidatorAgent.
        super().__init__(
            name=name,
            llm_config=llm_config,
            system_message=system_message,
            human_input_mode="NEVER",
        )
        print(f"Adding ValidatorAgent: {name}")

    def validate(self, final_output):
        # Validating the result.
        print(f"Validator {self.name} is performing the final check...")
        # Simulated validation logic.
        is_valid = True 
        if is_valid:
            return f"VALIDATED: {final_output}"
        else:
            return "Validation failed. Needs reassessment."
