from app.core.settings import patterns
import re


def exam_parser(cleaned_text):
    for pattern in patterns.FIND_SEQUENCE_ALTERNATIVES:
        match = re.search(pattern, cleaned_text)
        if match:
            start = match.start()
            body = cleaned_text[:start].strip()
            alternatives = {letter: content.strip() for letter, content in re.findall(patterns.EXTRACT_ALTERNATIVES, cleaned_text, re.DOTALL)}
            return {
                'body': body,
                'alternatives': alternatives
            }

    return {'body': cleaned_text.strip(), 'alternatives': {}}