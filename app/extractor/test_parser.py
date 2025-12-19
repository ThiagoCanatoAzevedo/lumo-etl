
import re
from typing import List, Dict, Tuple


def clean_text(text: str) -> str:
    text = re.sub(r'\*\d+\*\*?r?\d*\*?', '', text)
    text = re.sub(r'VALIDINEP\d*.*?(?=\n|$)', '', text, flags=re.MULTILINE)
    text = re.sub(r'LOGO\s*MATÉRIA\s*\d*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^\s*FORMAÇÃO GERAL\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'^\s*COMPONENTE ESPECÍFICO\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_alternatives(content: str) -> Tuple[Dict[str, str], int]:
    pattern = r'\n\s*([A-E])\s+([^\n]+(?:\n(?!\s*[A-E]\s+)[^\n]+)*)'
    matches = list(re.finditer(pattern, content, flags=re.MULTILINE))
    
    if not matches:
        return {}, -1
    
    alternatives = {}
    first_pos = matches[0].start()
    
    for match in matches:
        letter = match.group(1)
        text = match.group(2).strip()
        text = clean_text(text)
        text = ' '.join(line.strip() for line in text.split('\n') if line.strip())
        
        if text:
            alternatives[letter] = text
    
    return alternatives, first_pos


def extract_statement(content: str, first_alt_pos: int) -> str:
    if first_alt_pos <= 0:
        statement = content
    else:
        statement = content[:first_alt_pos]
    
    statement = clean_text(statement)
    lines = [line.strip() for line in statement.split('\n') if line.strip()]
    statement = '\n'.join(lines)
    
    return statement.strip()


def is_valid_question(statement: str, alternatives: Dict[str, str]) -> bool:
    if not statement or len(statement.strip()) < 10:
        return False
    
    if len(alternatives) < 4:
        return False
    
    required_letters = {'A', 'B', 'C', 'D'}
    if not required_letters.issubset(alternatives.keys()):
        return False
    
    return True


def test_parser(text: str) -> List[Dict]:
    results = []
    text = re.sub(
        r'QUESTÃO\s+DISCURSIVA.*?(?=QUESTÃO\s+\d+|$)',
        '',
        text,
        flags=re.DOTALL | re.IGNORECASE
    )
    text = re.sub(
        r'QUESTIONÁRIO\s+DE\s+PERCEPÇÃO.*$',
        '',
        text,
        flags=re.DOTALL | re.IGNORECASE
    )
    text = re.sub(
        r'AVALIAÇÃO\s+GLOBAL.*$',
        '',
        text,
        flags=re.DOTALL | re.IGNORECASE
    )
    text = re.sub(
        r'RASCUNHO.*?(?=QUESTÃO\s+\d+|$)',
        '',
        text,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    question_pattern = r'QUESTÃO\s+(\d+)\s*\n(.*?)(?=QUESTÃO\s+\d+\s*\n|QUESTIONÁRIO|AVALIAÇÃO|$)'
    
    matches = re.finditer(question_pattern, text, flags=re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        number = int(match.group(1))
        content = match.group(2)
        
        if re.search(r'DISCURSIVA|RASCUNHO', content, re.IGNORECASE):
            continue
        
        alternatives, first_alt_pos = extract_alternatives(content)
        
        statement = extract_statement(content, first_alt_pos)
        
        if is_valid_question(statement, alternatives):
            results.append({
                "number": number,
                "statement": statement,
                "alternatives": alternatives
            })
    return results