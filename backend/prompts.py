SUBJECT_REWRITE_PROMPT = """
Rewrite the intent into a realistic corporate email subject line.

Rules:
- Professional and believable
- Matches the company's industry and department
- Urgent but not alarming
- No quotes
- One line only

Context:
Company: {company}
Industry: {industry}
Department: {department}
Intent: {intent}

Return ONLY the subject line.
"""
