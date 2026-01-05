
import re
from typing import Dict

def solution_parser(text: str) -> Dict[int, str]:
    answers = {}
    
    text = re.sub(r'GABARITO.*?(?=\n)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'PADRÃO DE RESPOSTA.*?(?=\n)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'VALIDINEP.*?(?=\n)', '', text, flags=re.IGNORECASE)
    
    patterns = [
        r'(?:QUESTÃO|Questão|questão)\s+0*(\d+)\s*[-:.)]\s*([A-E])',
        r'[Qq]\.?\s*0*(\d+)\s*[-:.)]\s*([A-E])',
        r'^[\s]*0*(\d+)\s*[-:.)\s]\s*([A-E])',
        r'0*(\d+)\s*[)\]]\s*([A-E])',
        r'^[\s]*0*(\d+)\s{2,}([A-E])',
        r'(?:^|[^\w])0*(\d+)\s+([A-E])(?:[^\w]|$)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.MULTILINE)
        
        for num_str, letter in matches:
            try:
                number = int(num_str)
                letter = letter.upper()
                if letter in 'ABCDE':
                    if number not in answers:
                        answers[number] = letter
    
            except (ValueError, TypeError):
                continue
    return dict(sorted(answers.items()))


def solution_parser_with_sections(text: str) -> Dict[str, Dict[int, str]]:
    result = {
        "knowledge_area": {},
        "specific_component": {},
        "all": {}
    }
    
    fg_match = re.search(
        r'FORMAÇÃO\s+GERAL.*?(?=COMPONENTE\s+ESPECÍFICO|\Z)',
        text,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    ce_match = re.search(
        r'COMPONENTE\s+ESPECÍFICO.*',
        text,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    if fg_match:
        fg_text = fg_match.group(0)
        result["knowledge_area"] = solution_parser(fg_text)
    
    if ce_match:
        ce_text = ce_match.group(0)
        result["specific_component"] = solution_parser(ce_text)
    
    if not result["knowledge_area"] and not result["specific_component"]:
        result["all"] = solution_parser(text)
    else:
        result["all"] = {**result["knowledge_area"], **result["specific_component"]}
    
    return result


def validate_solution(answers: Dict[int, str], expected_count: int = None) -> Dict:
    validation = {
        "total_answers": len(answers),
        "numbered_questions": sorted(answers.keys()),
        "first_question": min(answers.keys()) if answers else None,
        "last_question": max(answers.keys()) if answers else None,
        "missing_questions": [],
        "letters_distribution": {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
    }
    
    for letter in answers.values():
        if letter in validation["letters_distribution"]:
            validation["letters_distribution"][letter] += 1
    
    if expected_count and answers:
        first = validation["first_question"]
        last = validation["last_question"]
        expected = set(range(first, last + 1))
        founded = set(answers.keys())
        validation["missing_questions"] = sorted(expected - founded)
    
    return validation