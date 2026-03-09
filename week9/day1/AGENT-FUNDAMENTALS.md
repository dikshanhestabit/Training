# AGENT-FUNDAMENTALS

## 1. What is an AI Agent?
An AI agent is an autonomous system that uses a Large Language Model (LLM) as its "brain" to perceive its environment, reason about a task, and take actions to achieve a goal.

### Agent vs. Chatbot vs. Pipeline
| Feature | Chatbot | Pipeline | AI Agent |
| :--- | :--- | :--- | :--- |
| **Control** | User-driven | Pre-defined sequence | Self-directed (LLM decides) |
| **Logic** | Static response | Linear flow (A -> B -> C) | Loop (Perception -> Reasoning -> Action) |
| **Feedback** | Minimal | None | Internal feedback loops |
| **Tool Use** | Usually none | Fixed API calls | Dynamic tool selection |


## 2. Perception → Reasoning → Action Loop
The core lifecycle of an agent involves three main stages:
1.  **Perception**: Receiving input (e.g., user query, environment data, or messages from other agents).
2.  **Reasoning**: Using the LLM to process findings, plan sub-tasks, and decide on the next steps.
3.  **Action**: Executing an operation (e.g., calling a tool, writing a file, or sending a message to another agent).


## 3. ReAct Pattern (Reason + Act)
The **ReAct** pattern combines *reasoning* (chain-of-thought) with *acting* (tool use).
- **Thought**: The agent describes what it needs to do.
- **Action**: The agent performs an action (e.g., searching the web).
- **Observation**: The agent reads the result of the action and repeats the loop until the task is complete.


## 4. Message-Based Communication Protocols
In multi-agent systems, communication is handled via structured message passing.
- **Role Isolation**: Each agent has a specific `system_message` that defines its boundaries (e.g., "You are a Summarizer; do not research").
- **Protocols**: Agents pass JSON or text-based messages. In systems like AutoGen, this is orchestrated via `send()` and `receive()` methods or group chat managers.


## 5. Role Control & Task Delegation
- **System Prompts**: The first instruction given to the LLM to define its persona and constraints.
- **Task Delegation**: A master agent (Planner) breaks down a complex task and delegates parts to specialized workers (Executors).
- **Isolation**: Ensuring an agent doesn't overstep its role (e.g., a Summarizer shouldn't try to gather new data).
