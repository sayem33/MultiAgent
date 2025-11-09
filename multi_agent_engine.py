import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o"

class GeneratorAgent:
    def __init__(self, task_type):
        self.prompts = {
            "summarization": "You are an RE expert. Generate clear, accurate summaries.",
            "quiz": "You are an RE expert. Generate well-structured quiz questions with answers.",
            "assignment": "You are an RE expert. Generate practical scenario-based assignments."
        }
        self.system_prompt = self.prompts.get(task_type, self.prompts["summarization"])
    
    def generate(self, prompt, pdf_content=None):
        full_prompt = f"Based on:\n{pdf_content[:2000]}\n\n{prompt}" if pdf_content else prompt
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=600
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"

class ReviewerAgent:
    def __init__(self):
        self.system_prompt = "You are an RE quality reviewer. Critique content for accuracy, completeness, and clarity. Provide specific improvement suggestions."
    
    def review(self, content, original_prompt, pdf_content=None):
        context = f"Original material: {pdf_content[:1000]}\n\n" if pdf_content else ""
        review_prompt = f"{context}Task: {original_prompt}\n\nGenerated content:\n{content}\n\nProvide critique with specific improvements."
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": review_prompt}
                ],
                max_tokens=400
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"

class RefinerAgent:
    def __init__(self):
        self.system_prompt = "You are an RE content refiner. Improve content based on reviewer feedback while maintaining original intent."
    
    def refine(self, original_content, critique, original_prompt, pdf_content=None):
        context = f"Source material: {pdf_content[:1000]}\n\n" if pdf_content else ""
        refine_prompt = f"{context}Task: {original_prompt}\n\nOriginal:\n{original_content}\n\nCritique:\n{critique}\n\nProvide improved version."
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": refine_prompt}
                ],
                max_tokens=600
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return original_content

class VerificationAgent:
    def __init__(self):
        self.system_prompt = "You are an RE verification expert. Check if content meets requirements and is factually accurate."
    
    def verify(self, content, original_prompt, pdf_content=None):
        context = f"Reference: {pdf_content[:1000]}\n\n" if pdf_content else ""
        verify_prompt = f"{context}Task: {original_prompt}\n\nContent:\n{content}\n\nVerify accuracy and completeness. Return APPROVED or suggest final fixes."
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": verify_prompt}
                ],
                max_tokens=200
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return "APPROVED"

class CoordinatorAgent:
    def __init__(self):
        self.reviewer = ReviewerAgent()
        self.refiner = RefinerAgent()
        self.verifier = VerificationAgent()
    
    def orchestrate(self, task_type, prompt, pdf_content=None):
        generator = GeneratorAgent(task_type)
        
        # Step 1: Generate initial content
        content = generator.generate(prompt, pdf_content)
        if "Error:" in content:
            return content
        
        # Step 2: Review content
        critique = self.reviewer.review(content, prompt, pdf_content)
        
        # Step 3: Refine based on critique
        refined = self.refiner.refine(content, critique, prompt, pdf_content)
        
        # Step 4: Verify final output
        verification = self.verifier.verify(refined, prompt, pdf_content)
        
        # Return refined content if approved, otherwise return with verification notes
        return refined if "APPROVED" in verification.upper() else f"{refined}\n\n[Note: {verification}]"

coordinator = CoordinatorAgent()

def multi_agent_generate(prompt, pdf_content=None, task_type="summarization"):
    """Multi-agent collaborative generation with review and refinement."""
    return coordinator.orchestrate(task_type, prompt, pdf_content)

