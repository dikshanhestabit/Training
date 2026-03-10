import asyncio
from autogen import ConversableAgent

class Planner(ConversableAgent):
    """
    Creating the Planner (Orchestrator) class.
    Inherits from ConversableAgent.
    Responsible for task decomposition, DAG generation, and multi-agent coordination.
    """
    def __init__(self, name, llm_config, agents_registry, system_message="You are a primary orchestrator. Decompose user queries into logical steps."):
        # Initializing the Planner with a registry of available agents.
        super().__init__(
            name=name,
            llm_config=llm_config,
            system_message=system_message,
            human_input_mode="NEVER",
        )
        self.agents_registry = agents_registry # Agent Registry Pattern
        self.task_graph = [] # Stores the DAG of tasks
        print(f"Adding Planner: {name}")

    def decompose_task(self, query):
        """
        Adding task decomposition logic.
        Parses the user query into atomic, executable steps.
        """
        print(f"Planner {self.name} is decomposing query: {query}")
        # Simulated decomposition for the architecture demonstration.
        # In a real implementation, this would use self.generate_reply() to ask the LLM for steps.
        steps = [
            {"id": 1, "task": "Research topic A", "agent": "worker_1", "depends_on": []},
            {"id": 2, "task": "Research topic B", "agent": "worker_2", "depends_on": []},
            {"id": 3, "task": "Consolidate research", "agent": "reflection", "depends_on": [1, 2]},
            {"id": 4, "task": "Final validation", "agent": "validator", "depends_on": [3]}
        ]
        self.task_graph = steps
        return steps

    def show_execution_tree(self):
        # Must show execution tree as per requirements.
        print("\n--- EXECUTION TREE ---")
        for step in self.task_graph:
            deps = f" (Depends on {step['depends_on']})" if step['depends_on'] else ""
            print(f"Step {step['id']}: {step['task']} -> Assigned to: {step['agent']}{deps}")
        print("----------------------\n")

    async def execute_dag(self):
        """
        Implementing DAG-based execution.
        Supports parallel execution of independent tasks.
        """
        print("Starting DAG execution...")
        completed_tasks = {}
        
        # Simple loop to handle dependencies (DAG Logic)
        while len(completed_tasks) < len(self.task_graph):
            tasks_to_run = []
            for step in self.task_graph:
                if step['id'] not in completed_tasks:
                    # Check if all dependencies are met
                    if all(dep in completed_tasks for dep in step['depends_on']):
                        tasks_to_run.append(step)
            
            if not tasks_to_run:
                break # Should not happen in a valid DAG

            # Running independent tasks in parallel
            print(f"Running parallel batch: {[t['id'] for t in tasks_to_run]}")
            batch_results = await asyncio.gather(*[self.run_step(t, completed_tasks) for t in tasks_to_run])
            
            for step, result in zip(tasks_to_run, batch_results):
                completed_tasks[step['id']] = result

        print("DAG Execution complete.")
        # Return the final task result (usually the validator's output)
        return completed_tasks[max(completed_tasks.keys())]

    async def run_step(self, step, completed_tasks):
        """
        Dispatching task to the appropriate agent from the registry.
        Adding logic to pass results from dependencies to the next agent.
        """
        agent_name = step['agent']
        agent = self.agents_registry.get(agent_name)
        if not agent:
            return f"Error: Agent {agent_name} not found."
            
        # Passing relevant data based on agent type
        if "worker" in agent_name:
            # Workers start the process with the decomposed task description
            return agent.execute_task(step['task'])
            
        elif "reflection" in agent_name:
            # Reflection agent receives results from its dependencies (the workers)
            worker_results = [str(completed_tasks[d]) for d in step['depends_on']]
            combined_input = "\n".join(worker_results)
            print(f"Passing {len(worker_results)} worker results to Reflection Agent.")
            return agent.reflect(combined_input)
            
        elif "validator" in agent_name:
            # Validator receives the result from its dependency (the reflection agent)
            # Typically has only one dependency in this 4-agent flow
            parent_id = step['depends_on'][0]
            reflection_result = completed_tasks[parent_id]
            print(f"Passing Reflection result from step {parent_id} to Validator.")
            return agent.validate(reflection_result)
        
        return "Unknown step"
