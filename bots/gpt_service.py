import requests
from django.conf import settings


def generate_response(prompt: str, history=None) -> str:
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = []
    if history:
        for user_msg, bot_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if 'choices' in data and len(data['choices']) > 0:
            return data['choices'][0]['message']['content'].strip()
        else:
            return "Извините, не могу сформировать ответ."
    except Exception as e:
        return f"Ошибка при обращении к ИИ: {str(e)}"