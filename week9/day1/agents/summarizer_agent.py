from autogen import ConversableAgent

def get_summarizer_agent(llm_config):
    """
    Creates and returns a Summarizer Agent.
    Strict Role: Only condenses provided data.
    """
    agent = ConversableAgent(
        name="Summarizer_Agent",
        system_message=(
            "You are a Summarizer Specialist. Your sole job is to take raw research data and condense it into a concise, logical summary. "
            "Do not perform additional research. Do not add new knowledge. Do not formulate a final user response. "
            "If you have finished summarizing, state 'SUMMARY_COMPLETE' followed by the summary."
        ),
        llm_config=llm_config,
        max_consecutive_auto_reply=1,
        human_input_mode="NEVER",
    )

    def limit_memory(recipient, messages, sender, config):
        if len(messages) > 10:
            messages[:] = [messages[0]] + messages[-9:]
        return False, None

    agent.register_reply(
        [ConversableAgent, None],
        reply_func=limit_memory,
        position=0
    )
    return agent
