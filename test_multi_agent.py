import json
import time
from datetime import datetime
from multi_agent_engine import multi_agent_generate
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def evaluate_with_llm(instruction, generated, reference):
    """Evaluate generated output using LLM."""
    prompt = f"""Evaluate the generated output against the reference answer.

Instruction: {instruction}
Generated Output: {generated}
Reference Answer: {reference}

Rate on a scale of 1-10 for:
CORRECTNESS: [score]
COMPLETENESS: [score]
CLARITY: [score]
RELEVANCE: [score]
OVERALL: [average score]

REASONING: [brief explanation]"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
            temperature=0.3
        )
        raw = response["choices"][0]["message"]["content"]
        
        scores = {}
        for line in raw.split('\n'):
            if 'CORRECTNESS:' in line:
                scores['correctness'] = float(line.split(':')[1].strip())
            elif 'COMPLETENESS:' in line:
                scores['completeness'] = float(line.split(':')[1].strip())
            elif 'CLARITY:' in line:
                scores['clarity'] = float(line.split(':')[1].strip())
            elif 'RELEVANCE:' in line:
                scores['relevance'] = float(line.split(':')[1].strip())
            elif 'OVERALL:' in line:
                scores['overall'] = float(line.split(':')[1].strip())
        
        return {"scores": scores, "reasoning": raw, "raw_evaluation": raw}
    except:
        return {"scores": {}, "reasoning": "", "raw_evaluation": ""}

def calculate_metrics(generated, reference):
    """Calculate automated metrics."""
    gen_words = set(generated.lower().split())
    ref_words = set(reference.lower().split())
    
    precision = len(gen_words & ref_words) / len(gen_words) if gen_words else 0
    recall = len(gen_words & ref_words) / len(ref_words) if ref_words else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "length_ratio": len(generated.split()) / len(reference.split()) if reference else 0,
        "word_precision": precision,
        "word_recall": recall,
        "word_f1": f1,
        "char_jaccard": len(set(generated) & set(reference)) / len(set(generated) | set(reference)) if reference else 0
    }

def run_tests():
    """Run all 90 test cases."""
    with open('test_dataset_re_90.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    results = []
    
    for material in dataset:
        material_id = material['material_id']
        content = material.get('content', '')
        
        for test_case in material['test_cases']:
            test_id = test_case['test_id']
            task_type = test_case['task_type']
            instruction = test_case['instruction']
            reference = test_case['reference_answer']
            
            if isinstance(reference, dict):
                reference = json.dumps(reference)
            
            print(f"Running {test_id}...")
            
            start = time.time()
            try:
                generated = multi_agent_generate(instruction, content, task_type)
                error = None
            except Exception as e:
                generated = ""
                error = str(e)
            latency = time.time() - start
            
            llm_eval = evaluate_with_llm(instruction, generated, reference) if not error else {}
            auto_metrics = calculate_metrics(generated, reference) if not error else {}
            
            results.append({
                "test_id": test_id,
                "task_type": task_type,
                "material_id": material_id,
                "instruction": instruction,
                "generated_output": generated,
                "reference_answer": reference,
                "error": error,
                "latency_seconds": latency,
                "timestamp": datetime.now().isoformat(),
                "llm_evaluation": llm_eval,
                "automated_metrics": auto_metrics
            })
    
    with open('multi_agent_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nCompleted {len(results)} tests. Results saved to multi_agent_results.json")

if __name__ == "__main__":
    run_tests()


