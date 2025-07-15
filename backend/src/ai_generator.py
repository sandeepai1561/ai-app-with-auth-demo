import os
import json
from openai import OpenAI
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    """
    generate_challenge_with_ai
    :param difficulty:
    :return:
    """
    prompt = f"Generate a challenge with difficulty {difficulty}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1024,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        challenge_data = json.loads(content)

        required_keys = ["title", "options", "correct_answer_id", "explanation"]
        for key in required_keys:
            if key not in challenge_data:
                raise Exception("")
        return challenge_data
    except Exception as e:
        raise {
            "message": "Error generating challenge",
            "error": str(e),
            "options": [

            ],
            "correct_answer_id": 0,
            "explanation": "",
        }