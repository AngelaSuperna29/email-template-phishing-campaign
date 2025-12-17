SUBJECT_REWRITE_PROMPT = """
Rewrite the following intent into a professional corporate IT notification subject.

Rules:
- Do NOT copy the intent verbatim
- Professional and realistic
- No quotes
- One line only

Company: {company}
Department: {department}
Intent: {intent}

Return ONLY the subject line.
"""


DYNAMIC_PARAGRAPH_PROMPT = """
Write ONE short paragraph for a corporate IT notification email.

STRICT RULES:
- 1 paragraph only
- 1–2 sentences
- No markdown
- No links
- No URLs
- No phone numbers
- No email addresses
- Professional, urgent tone

Context:
Company: {company}
Company Website: {company_url}
Industry: {industry}
Department: {department}
Subject meaning: {subject}


Style reference:
"This is an important security notification regarding your account. To ensure uninterrupted access, please verify your account details immediately."

Return ONLY the paragraph text.
"""
