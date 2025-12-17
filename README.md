# LLM-Powered Online Teaching Assistant for Requirements Engineering (RE) Course (APUOPE-RE)

A multi-agent AI system designed to assist students in learning Requirements Engineering through intelligent content generation, quizzes, assignments, and conceptual explanations.

---

## Multi-Agent Architecture Overview

This system employs a **4-agent collaborative architecture** with a sequential communication protocol, ensuring high-quality educational content through iterative review and refinement.

## Core Multi-Agent System (`multi_agent_engine.py`)

### Four Specialized Agents

#### Agent 1: GeneratorAgent - Task-specific Content Creation

Creates initial content tailored to specific educational tasks.

```python
class GeneratorAgent:
    def __init__(self, task_type):
        self.prompts = {
            "summarization": "You are an RE expert. Generate clear, accurate summaries.",
            "quiz_generation": "You are an RE expert. Generate well-structured quiz questions...",
            "qa_conceptual": "You are an RE expert. Provide clear, conceptual explanations...",
            "qa_application": "You are an RE expert. Provide practical, application-focused..."
        }
        self.system_prompt = self.prompts.get(task_type, self.prompts["summarization"])
```

#### Agent 2: ReviewerAgent - Quality Critique

Analyzes generated content and provides constructive feedback for improvement.

```python
class ReviewerAgent:
    def review(self, content, original_prompt, pdf_content=None):
        review_prompt = f"""Task: {original_prompt}

Generated content:
{content}

Provide critique with specific improvements."""
        # Returns critique for refinement
```

#### Agent 3: RefinerAgent - Content Improvement

Takes the original content and critique to produce an enhanced version.

```python
class RefinerAgent:
    def refine(self, original_content, critique, original_prompt, pdf_content=None):
        refine_prompt = f"""Original:
{original_content}

Critique:
{critique}

Provide improved version."""
        # Returns refined content based on critique
```

#### Agent 4: VerificationAgent - Final Validation

Performs final quality assurance before content delivery.

```python
class VerificationAgent:
    def verify(self, content, original_prompt, pdf_content=None):
        verify_prompt = f"""Content:
{content}

Verify accuracy and completeness. 
Return APPROVED or suggest final fixes."""
        # Returns APPROVED or suggestions
```

---

## Orchestration - Sequential Collaborative Pipeline

The `CoordinatorAgent` manages the entire workflow, ensuring agents collaborate in sequence:

```python
class CoordinatorAgent:
    def orchestrate(self, task_type, prompt, pdf_content=None):
        generator = GeneratorAgent(task_type)
        
        # Step 1: Generate initial content
        content = generator.generate(prompt, pdf_content)
        
        # Step 2: Review content
        critique = self.reviewer.review(content, prompt, pdf_content)
        
        # Step 3: Refine based on critique
        refined = self.refiner.refine(content, critique, prompt, pdf_content)
        
        # Step 4: Verify final output
        verification = self.verifier.verify(refined, prompt, pdf_content)
        
        return refined if "APPROVED" in verification.upper() else f"{refined}\n\n[Note: {verification}]"
```

---

## Integration Points

The multi-agent system is integrated across multiple components:

### `components/assignment.py`

```python
# Changed from fine_tuned_engine to multi_agent_engine
from multi_agent_engine import multi_agent_generate

def generate_conceptual_assignment(pdf_title, pdf_path, pdf_content):
    prompt = f"Create a real-life scenario-based conceptual assignment..."
    return multi_agent_generate(prompt, pdf_content, "assignment")
```

### `quiz_handler.py`

```python
# Changed from fine_tuned_engine to multi_agent_engine
from multi_agent_engine import multi_agent_generate

def generate_quiz(pdf_content, difficulty, pdf_path=None):
    prompt = f"Generate 3 {difficulty.upper()} multiple-choice questions..."
    raw_data = multi_agent_generate(prompt, pdf_content, "quiz_generation")
```

### `components/conceptual_examples.py`

```python
# Changed from fine_tuned_engine to multi_agent_engine
from multi_agent_engine import multi_agent_generate

def generate_content(prompt, pdf_path, pdf_content):
    task_type = "assignment" if "example" in prompt.lower() else "summarization"
    return multi_agent_generate(prompt, pdf_content, task_type)
```

---

## Key Architecture Features

| Feature | Description |
|---------|-------------|
| **4 Specialized Agents** | Each agent has a distinct role (Generate, Review, Refine, Verify) |
| **Sequential Communication** | Generator → Reviewer → Refiner → Verifier pipeline |
| **Agent-to-Agent Collaboration** | Critique and refinement loops ensure quality |
| **Centralized Model** | GPT-4o used for consistency across all agents |
| **Task-Specific Prompts** | 5 different task types with tailored system prompts |

---

## Task Types Supported

1. **Summarization** - Lecture content summaries
2. **Quiz Generation** - Multiple-choice question creation
3. **QA Conceptual** - Conceptual explanations and definitions
4. **QA Application** - Practical, application-focused answers
5. **Assignment** - Scenario-based assignment generation

---

## Project Structure

```
MultiAgent/
├── app.py                    # Main Streamlit application
├── multi_agent_engine.py     # Core multi-agent system
├── quiz_handler.py           # Quiz generation and handling
├── chatbot.py                # Chatbot interface
├── auth.py                   # Authentication module
├── db.py                     # Database operations
├── components/
│   ├── assignment.py         # Assignment generation
│   ├── conceptual_examples.py # Conceptual examples
│   ├── dashboard.py          # User dashboard
│   ├── feedback.py           # Feedback collection
│   ├── lecture_summaries.py  # Lecture summary generation
│   ├── progress_tracking.py  # Student progress tracking
│   └── quizzes.py            # Quiz interface
├── tests/                    # Test suite
└── requirements.txt          # Dependencies
```

---

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
