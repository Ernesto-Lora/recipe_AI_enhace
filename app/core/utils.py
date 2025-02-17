import openai
from django.conf import settings

mock_openai_response = [
    {
        "title": "Breakfast",
        "description": "A healthy and filling breakfast to start your day right.",
        "ingredients": [
            {"name": "Whole grain bread", "amount": 2, "unit": "piece"},  # Bread is typically counted in pieces
            {"name": "Avocado", "amount": 0.5, "unit": "piece"},  # Avocado is typically counted in pieces
            {"name": "Egg", "amount": 2, "unit": "piece"},  # Eggs are counted in pieces
            {"name": "Orange juice", "amount": 200, "unit": "ml"}  # Correct unit for liquids
        ],
        "calories": 600
    },
    {
        "title": "Lunch",
        "description": "A balanced lunch to keep you energized throughout the day.",
        "ingredients": [
            {"name": "Grilled chicken breast", "amount": 150, "unit": "g"},  # Correct unit for meat
            {"name": "Quinoa", "amount": 100, "unit": "g"},  # Correct unit for grains
            {"name": "Steamed broccoli", "amount": 100, "unit": "g"},  # Correct unit for vegetables
            {"name": "Salad with vinaigrette", "amount": 1, "unit": "cup"}  # Salad is typically measured in cups
        ],
        "calories": 600
    },
    {
        "title": "Dinner",
        "description": "A wholesome dinner to end the day.",
        "ingredients": [
            {"name": "Baked salmon", "amount": 150, "unit": "g"},  # Correct unit for fish
            {"name": "Sweet potato", "amount": 150, "unit": "g"},  # Correct unit for root vegetables
            {"name": "Steamed asparagus", "amount": 100, "unit": "g"},  # Correct unit for vegetables
            {"name": "Glass of red wine", "amount": 150, "unit": "ml"}  # Correct unit for liquids
        ],
        "calories": 600
    }
]

def generate_meal_plan_testing(calories_per_day, num_meals=3):
    """Mocked function to test without OpenAI API calls."""
    return mock_openai_response  # Use the predefined response for testing

import json

def generate_meal_plan(calories_per_day, num_meals=3):
    """Generate multiple recipes to fit a given daily caloric intake."""
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    prompt = (
        f"Create {num_meals} balanced meals that together sum up to approximately {calories_per_day} kcal. "
        "Each meal should include ingredients with portion sizes and the total calories per meal. "
        "Format the response as JSON with a list of recipes, each containing 'title', 'description', "
        "'ingredients' (with amount and unit), and 'calories'."
        "Respond **only** with a JSON array. Each item should have: "
         " - 'description': Brief description"
        " - 'ingredients': List of ingredients in format {name, amount, unit}"
        " - 'calories': Total calories per meal."
        "Ensure the response starts directly with '[' and ends with ']'. No explanations."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    raw_response = response.choices[0].message.content.strip()
    
    # Debugging logs
    print(f"\nRAW RESPONSE FROM OPENAI:\n{raw_response}\n")
    print(f"Type of raw_response: {type(raw_response)}")  # Check if it's a string

    try:
        meal_data = json.loads(raw_response)  # Convert to Python object

        # If OpenAI returned a dictionary instead of a list, extract the list
        if isinstance(meal_data, dict) and "meals" in meal_data:
            meal_data = meal_data["meals"]

        if not isinstance(meal_data, list):
            raise ValueError("Parsed response is not a list")

        return meal_data  # Correct format
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON")
        return None  # Return None if OpenAI response is invalid
    except ValueError as e:
        print(f"Error: {e}")
        return None
