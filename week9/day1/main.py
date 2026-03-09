import os
from autogen import UserProxyAgent, GroupChat, GroupChatManager
from agents.research_agent import get_research_agent
from agents.summarizer_agent import get_summarizer_agent
from agents.answer_agent import get_answer_agent

# Local LLM Config (Using tinyllama for faster CPU performance)
llm_config = {
    "config_list": [
        {
            "model": "tinyllama",
            "api_key": "not-needed",
            "base_url": "http://localhost:11434/v1",
        }
    ],
    "cache_seed": 42,
}

def main():
    # 1. Initializing specialized agents
    research_agent = get_research_agent(llm_config)
    summarizer_agent = get_summarizer_agent(llm_config)
    answer_agent = get_answer_agent(llm_config)

    # 2. Defining the User Proxy Agent with termination logic
    user_proxy = UserProxyAgent(
        name="User_Proxy",
        system_message="A proxy for the human user to initiate tasks.",
        human_input_mode="NEVER",
        is_termination_msg=lambda x: "SUMMARY_COMPLETE" in (x.get("content", "") or "") or "RESEARCH_COMPLETE" in (x.get("content", "") or ""), # Adjusting to move flow along
        code_execution_config=False,
    )

    # 3. Defining the GroupChat for native orchestration
    groupchat = GroupChat(
        agents=[user_proxy, research_agent, summarizer_agent, answer_agent],
        messages=[],
        max_round=6, 
        speaker_selection_method="round_robin",
        allow_repeat_speaker=False
    )

    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    print("\n--- Starting NATIVE Agentic Workflow (GroupChat) ---\n")
    
    user_query = "What are the latest breakthroughs in agentic AI architecture?"

    # Initiating the group chat
    user_proxy.initiate_chat(
        manager,
        message=user_query,
        clear_history=True
    )

if __name__ == "__main__":
    main()
