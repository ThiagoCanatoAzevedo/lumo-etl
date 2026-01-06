import re

def clean_raw_text_pdf(raw_text: str, metadata: dict) -> str:
    course = metadata.get("course_exam", "").upper()

    raw_text = re.sub(
        r'(QUESTÃO\s+\d+)\s+(?=[A-ZÁÉÍÓÚÃÕÇ])',
        r'\1\n',
        raw_text,
        flags=re.IGNORECASE
    )

    raw_text = re.sub(r'\*.*?\*', '', raw_text)

    if course:
        raw_text = re.sub(re.escape(course), '', raw_text, flags=re.IGNORECASE)

    raw_text = "\n".join(
        line for line in raw_text.splitlines()
        if not re.fullmatch(r'\s*\d+\s*', line)
    )

    parts = re.split(r'Disponível em:', raw_text, flags=re.IGNORECASE, maxsplit=1)
    before = parts[0]
    after = f"Disponível em:{parts[1]}" if len(parts) > 1 else ""

    before = "\n".join(
        line for line in before.splitlines()
        if line.strip()
        and (
            re.fullmatch(r'QUESTÃO\s+\d+', line.strip(), flags=re.IGNORECASE)
            or re.fullmatch(r'TEXTO\s+\d+', line.strip(), flags=re.IGNORECASE)
            or '.' in line
        )
    )

    return f"{before.strip()}\n\n{after.strip()}"