# Multi-Agent Orchestration Flow

```mermaid
graph TD
    UserQuery[User Query] --> Orchestrator[Orchestrator / Planner]
    Orchestrator -->|Task Decomposition| Tasks[Task Graph / DAG]
    
    subgraph Parallel Execution
        Tasks --> Worker1[Worker Agent 1]
        Tasks --> Worker2[Worker Agent N]
    end
    
    Worker1 --> Reflection[Reflection Agent]
    Worker2 --> Reflection
    
    Reflection -->|Refined Output| Validator[Validator Agent]
    
    Validator -->|Final Result| User[Final Answer to User]
    
    Reflection -.->|Improvement Loop| Worker1
    Validator -.->|Error Correction| Reflection
```

## Description
1. **User Query**: The starting point of the interaction.
2. **Orchestrator / Planner**: Parses the query and breaks it down into a Directed Acyclic Graph (DAG) of tasks.
3. **Worker Agents**: Execute individual atomic tasks in parallel where independent.
4. **Reflection Agent**: Critiques the workers' outputs and suggests improvements.
5. **Validator Agent**: Performs a final logic and safety check before delivery.
