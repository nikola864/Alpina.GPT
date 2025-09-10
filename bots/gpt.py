import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def get_gpt_response(prompt, model="gpt-3.5-turbo", max_tokens=150):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Ошибка GPT: {str(e)}"