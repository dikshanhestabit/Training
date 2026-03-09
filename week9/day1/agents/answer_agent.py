from autogen import ConversableAgent

def get_answer_agent(llm_config):
    """
    Creates and returns an Answer Agent.
    Strict Role: Formulates final response from summary.
    """
    agent = ConversableAgent(
        name="Answer_Agent",
        system_message=(
            "You are an Answer Agent. Your job is to take a provided summary and formulate a polished, direct, "
            "and final response to the user's initial query. "
            "Do not perform research and do not summarize raw data yourself. Use only the summary provided to you."
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
