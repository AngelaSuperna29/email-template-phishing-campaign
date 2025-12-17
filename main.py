from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <- Add this for frontend
from pydantic import BaseModel
from mistral_client import call_mistral
from industry_detector import infer_industry
from prompts import SUBJECT_REWRITE_PROMPT

app = FastAPI()

# ---------------- CORS setup ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (OK for dev/demo)
    allow_credentials=True,
    allow_methods=["*"],  # Allow GET, POST, OPTIONS
    allow_headers=["*"],
)

# ---------------- Request Model ----------------
class EmailRequest(BaseModel):
    company: str
    department: str
    subject: str | None = None
    company_url: str | None = None
    industry: str | None = None

# ---------------- Email Generation Endpoint ----------------
@app.post("/generate-email")
def generate_email(data: EmailRequest):
    # Use provided subject or default intent
    intent = data.subject or "account verification required"

    # Generate final subject via Mistral
    subject_prompt = SUBJECT_REWRITE_PROMPT.format(
        intent=intent,
        company=data.company,
        department=data.department
    )
    final_subject = call_mistral(subject_prompt).strip()

    # Determine industry
    if data.industry:
        industry = data.industry
    elif data.company_url:
        industry = infer_industry(data.company, data.company_url)
    else:
        industry = "Corporate"

    # Generate dynamic email content
    paragraph_prompt = f"""
You are generating the MAIN MESSAGE of a corporate security email.

STRICT RULES (DO NOT BREAK):
- Output ONLY sentence text
- 1–2 sentences only
- No quotes
- No links
- No generic phrases like "important security notification"
- Content MUST change meaningfully based on department and industry

THREAT MODELING RULES:
- HR → payroll, employee records, policy compliance
- Finance → invoices, payment systems, financial access
- IT → credentials, VPN, system access
- Operations → internal tools, workflow disruption
- Tech industry → systems, platforms, access control
- Healthcare industry → compliance, records, access integrity

CONTEXT:
Company: {data.company}
Industry: {industry}
Department: {data.department}
Subject: {final_subject}

TASK:
Describe a REALISTIC issue that would affect THIS department
inside THIS industry, requiring immediate verification.

Return ONLY the sentence text.
"""

    dynamic_content = call_mistral(paragraph_prompt)
    # Clean text: remove quotes, extra spaces, limit to 220 chars
    dynamic_content = " ".join(dynamic_content.replace('"', '').split())[:220]

    # ---------------- HTML Template ----------------
    final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Important Account Notification</title>
</head>
<body style="font-family: sans-serif; line-height: 1.6;">

<p>Hello {{{{target.first_name}}}},</p>

<p>{dynamic_content}</p>

<p style="margin: 25px 0;">
<a href="{{{{click_url}}}}" style="background-color:#007bff;color:white;padding:12px 20px;text-decoration:none;border-radius:5px;font-weight:bold;">
Verify Your Account
</a>
</p>

<p>If you did not request this action, please disregard this message. If you believe this email is suspicious, please report it using the link below.</p>

<p style="font-size:0.9em;color:#666;">
<a href="{{{{report_url}}}}">Report this email as suspicious</a>
</p>

<p>Thank you,<br>{data.company} IT Support Team</p>

<img src="{{{{pixel_url}}}}" width="1" height="1" style="display:none;" alt="" />

</body>
</html>"""

    return {
        "subject": final_subject,
        "html": final_html
    }
