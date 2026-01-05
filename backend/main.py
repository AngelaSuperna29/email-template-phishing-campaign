from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mistral_client import call_mistral
from industry_detector import infer_industry
from prompts import SUBJECT_REWRITE_PROMPT, DYNAMIC_PARAGRAPH_PROMPT

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Request Model ----------------
class EmailRequest(BaseModel):
    company: str
    department: str
    subject: str | None = None
    company_url: str | None = None
    industry: str | None = None

# ---------------- Endpoint ----------------
@app.post("/generate-email")
def generate_email(data: EmailRequest):

    # 1️⃣ Intent fallback
    intent = data.subject or "account verification required"

    # 2️⃣ Industry detection
    if data.industry:
        industry = data.industry
    elif data.company_url:
        industry = infer_industry(data.company, data.company_url)
    else:
        industry = "Corporate"

    # 3️⃣ Subject generation (NOW industry-aware)
    subject_prompt = SUBJECT_REWRITE_PROMPT.format(
        intent=intent,
        company=data.company,
        industry=industry,
        department=data.department
    )

    final_subject = call_mistral(subject_prompt).strip()

    # 4️⃣ Dynamic content generation (KEY FIX)
    paragraph_prompt = DYNAMIC_PARAGRAPH_PROMPT.format(
        company=data.company,
        company_url=data.company_url or "N/A",
        industry=industry,
        department=data.department,
        subject=final_subject
    )

    dynamic_content = call_mistral(paragraph_prompt).strip()

    # Normalize (safety)
    dynamic_content = " ".join(dynamic_content.replace('"', "").split())

    # 5️⃣ Final HTML
    final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{final_subject}</title>
</head>

<body style="font-family: sans-serif; line-height: 1.6;">

<p>Hello {{{{target.first_name}}}},</p>

{dynamic_content}

<p style="margin: 25px 0;">
<a href="{{{{click_url}}}}"
   style="background-color:#007bff;color:white;padding:12px 20px;
   text-decoration:none;border-radius:5px;font-weight:bold;">
Verify Your Account
</a>
</p>

<p>If you did not request this action, please disregard this message.
If you believe this email is suspicious, please report it below.</p>

<p style="font-size:0.9em;color:#666;">
<a href="{{{{report_url}}}}">Report this email as suspicious</a>
</p>

<p>Thank you,<br>{data.company} {data.department} Team</p>

<img src="{{{{pixel_url}}}}" width="1" height="1" style="display:none;" alt="" />

</body>
</html>"""

    return {
        "subject": final_subject,
        "html": final_html
    }
