import asyncio
from agents.worker_agent import WorkerAgent
from agents.reflection_agent import ReflectionAgent
from agents.validator import ValidatorAgent
from orchestrator.planner import Planner

async def main():
    """
    Creating the main entry point for the 4-agent architecture.
    This script initializes all agents and runs the orchestration flow.
    """
    # Adding LLM configuration (simulated for demonstration)
    llm_config = {"config_list": [{"model": "gpt-4", "api_key": "YOUR_API_KEY"}]}

    # Initializing worker agents
    worker_1 = WorkerAgent(name="worker_1", llm_config=llm_config)
    worker_2 = WorkerAgent(name="worker_2", llm_config=llm_config)

    # Initializing reflection and validator agents
    reflection = ReflectionAgent(name="reflection", llm_config=llm_config)
    validator = ValidatorAgent(name="validator", llm_config=llm_config)

    # Creating the Agent Registry
    registry = {
        "worker_1": worker_1,
        "worker_2": worker_2,
        "reflection": reflection,
        "validator": validator
    }

    # Initializing the Orchestrator / Planner
    orchestrator = Planner(name="orchestrator", llm_config=llm_config, agents_registry=registry)

    # Running a user query
    user_query = "What are the latest trends in autonomous agent orchestration?"
    
    # Executing Step 1: Task Decomposition
    steps = orchestrator.decompose_task(user_query)
    
    # Executing Step 2: Showing Execution Tree
    orchestrator.show_execution_tree()
    
    # Executing Step 3: DAG Execution (Parallel workers)
    final_result = await orchestrator.execute_dag()
    
    print(f"\nFINAL ANSWER: {final_result}")

if __name__ == "__main__":
    # Starting the main loop
    asyncio.run(main())
