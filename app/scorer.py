import os
import json
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))


def score_cv(cv_text, job_description):
    """Send CV and job description to Groq for analysis and scoring."""

    prompt = f"""You are an expert technical recruiter. Analyze the following CV against the job description.

JOB DESCRIPTION:
{job_description}

CV CONTENT:
{cv_text}

Respond ONLY with valid JSON in this exact structure, no other text:
{{
  "match_score": <integer 0-100>,
  "summary": "<2-3 sentence overall assessment>",
  "matching_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "experience_assessment": "<1-2 sentences on experience level fit>",
  "recommendation": "<one of: Strong Match, Good Match, Weak Match, Not a Match>"
}}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        raw_text = response.choices[0].message.content.strip()
        raw_text = raw_text.replace('```json', '').replace('```', '').strip()

        result = json.loads(raw_text)
        return result

    except json.JSONDecodeError:
        raise ValueError("AI returned an unexpected format. Please try again.")
    except Exception as e:
        raise ValueError(f"Analysis failed: {str(e)}")