import openai
from django.conf import settings

def enhance_recipe_text(recipe_text):
    """Use OpenAI API to enhance a given recipe text."""
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    prompt = f"Improve this recipe description while keeping it concise and engaging: {recipe_text}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
