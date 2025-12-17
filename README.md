# APUOPE-RE: Multi-Agent Teaching Assistant

This application serves as an interactive teaching assistant for Requirements Engineering (RE) courses. It employs a multi-agent AI architecture to generate high-quality educational content, including quizzes, assignments, and conceptual explanations.

## Architecture Overview

The system utilizes a sequential collaborative workflow involving four specialized agents. Unlike traditional single-pass LLM interactions, this architecture enforces an iterative review process where content is generated, critiqued, and refined before being presented to the student.

The workflow is managed by a central orchestration layer (`CoordinatorAgent`) that directs the data flow through the following pipeline:

1.  **Generator:** Creates initial content based on the specific educational task.
2.  **Reviewer:** Analyzes the output for accuracy and clarity, providing structured critique.
3.  **Refiner:** Synthesizes the original content and the critique to produce an improved version.
4.  **Verifier:** Performs a final quality assurance check to ensure the content meets educational standards.

## Core Implementation

The backend logic is contained within `multi_agent_engine.py`. This module defines the individual agent classes and the orchestration logic used to manage them.

### Agent Configuration
Each agent is initialized with specific system prompts to define their distinct roles:
*   **GeneratorAgent:** Uses task-specific prompts (e.g., summarization, quiz generation, conceptual QA) to frame the initial response.
*   **ReviewerAgent:** Uses a critique-focused prompt to identify flaws in the generated text.
*   **RefinerAgent:** Uses a synthesis prompt to apply the feedback.
*   **VerificationAgent:** Uses a validation prompt to approve the final output or append necessary corrections.

### Orchestration
The `CoordinatorAgent` class manages the sequential execution. It passes the output of the Generator to the Reviewer, then to the Refiner, and finally to the Verifier. The final output is only returned to the UI once it has passed through this verification chain.

## Integration

The multi-agent engine is integrated into the application via specific component modules. It replaces standard API calls to ensure all content benefits from the multi-agent review process.

*   **Assignments (`components/assignment.py`):** Uses the engine to generate real-life scenario-based assignments.
*   **Quizzes (`quiz_handler.py`):** Generates difficulty-graded multiple-choice questions.
*   **Examples (`components/conceptual_examples.py`):** Dynamically switches between summarization and application tasks based on user input.

## System Capabilities

The architecture supports five primary task types, all using GPT-4o for consistency:
*   **Summarization:** condensing lecture notes.
*   **Quiz Generation:** creating structured assessment items.
*   **QA Conceptual:** defining terms and concepts.
*   **QA Application:** providing practical examples.
*   **Assignments:** generating complex scenarios.

## Project Structure

```text
MultiAgent/
├── app.py                    # Main Streamlit application
├── multi_agent_engine.py     # Core multi-agent implementation
├── quiz_handler.py           # Quiz logic and parsing
├── chatbot.py                # Chatbot interface
├── auth.py                   # User authentication
├── db.py                     # Database interactions
├── components/               # UI Modules
│   ├── assignment.py
│   ├── conceptual_examples.py
│   ├── dashboard.py
│   ├── feedback.py
│   ├── lecture_summaries.py
│   ├── progress_tracking.py
│   └── quizzes.py
├── tests/                    # Test suite
└── requirements.txt          # Python dependencies
```

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables** (OpenAI API key, etc.)

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```
   Or use the provided script:
   ```bash
   ./run.sh
   ```

---