# prompts.py

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


DYNAMIC_PARAGRAPH_PROMPT = """
Write the MAIN MESSAGE CONTENT of a corporate email.

VERY IMPORTANT:
- The scenario MUST CHANGE based on Industry and Department
- Do NOT always use IT security language
- Choose a realistic reason someone from this department would contact an employee

Possible examples (DO NOT copy):
- Finance → payroll issue, invoice verification, tax update
- HR → policy update, document verification, benefits review
- IT → access issue, security update, system maintenance
- Operations → workflow update, compliance check
- Industry context must influence tone and terminology

STRICT OUTPUT RULES:
- Output VALID HTML only
- Use <p> tags
- 2 short paragraphs max
- No markdown
- No explanations
- No meta text

Context:
Company: {company}
Company Website: {company_url}
Industry: {industry}
Department: {department}
Email Subject: {subject}

The content must look like it genuinely came from this department
inside this company and industry.

Return ONLY the HTML content.
"""
