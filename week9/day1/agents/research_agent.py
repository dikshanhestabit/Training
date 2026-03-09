from autogen import ConversableAgent

def get_research_agent(llm_config):
    """
    Creates and returns a Research Agent.
    Strict Role: Only gathers raw information.
    """
    agent = ConversableAgent(
        name="Research_Agent",
        system_message=(
            "You are a Research Specialist. Your sole job is to gather relevant information on a given topic. "
            "Do not summarize. Do not provide final answers. Provide only the raw technical findings or data you discover. "
            "If you have gathered enough information, state 'RESEARCH_COMPLETE' followed by the data."
        ),
        llm_config=llm_config,
        max_consecutive_auto_reply=1,
        human_input_mode="NEVER",
    )

    def limit_memory(recipient, messages, sender, config):
        if len(messages) > 10:
            # Keep the system message (index 0) and the last 9 messages
            messages[:] = [messages[0]] + messages[-9:]
        return False, None

    agent.register_reply(
        [ConversableAgent, None],
        reply_func=limit_memory,
        position=0
    )
    return agent
