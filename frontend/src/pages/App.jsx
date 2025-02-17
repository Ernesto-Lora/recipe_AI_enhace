import { useState } from "react";
import axios from "axios";

const API_GENERATE_MEAL_PLAN = "http://127.0.0.1:8000/api/recipe/recipes/generate-meal-plan/";
const API_GET_RECIPES = "http://127.0.0.1:8000/api/recipe/recipes/";

const fetchAuthToken = () => localStorage.getItem("authToken");

export default function MealPlanner() {
  const [calories, setCalories] = useState(1800);
  const [meals, setMeals] = useState(3);
  const [mealPlan, setMealPlan] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [error, setError] = useState(null);
  const [showRecipes, setShowRecipes] = useState(false);
  const [showMealPlan, setShowMealPlan] = useState(false);

  const fetchMealPlan = async () => {
    try {
      const token = fetchAuthToken();
      if (!token) throw new Error("No authentication token found.");
      
      const response = await axios.post(
        API_GENERATE_MEAL_PLAN,
        { calories, meals },
        { headers: { Authorization: `Token ${token}` } }
      );
      setMealPlan(response.data);
      setShowMealPlan(true);
    } catch (err) {
      setError(err.message);
    }
  };

  const fetchSavedRecipes = async () => {
    try {
      const token = fetchAuthToken();
      if (!token) throw new Error("No authentication token found.");
      
      const response = await axios.get(API_GET_RECIPES, {
        headers: { Authorization: `Token ${token}` },
      });
      setRecipes(response.data);
      setShowRecipes(true);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="meal-planner-container">
      <style>
        {`
          .meal-planner-container {
            padding: 24px;
            max-width: 800px;
            margin: 0 auto;
            background-color: #f7fafc;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          }
          .meal-planner-container h1 {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            color: #2d3748;
            margin-bottom: 16px;
          }
          .input-group {
            background-color: white;
            padding: 16px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 24px;
          }
          .input-group label {
            display: block;
            font-weight: 600;
            color: #4a5568;
          }
          .input-group input {
            width: 100%;
            padding: 8px;
            margin-top: 8px;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            box-sizing: border-box;
          }
          .input-group input:focus {
            outline: none;
            border-color: #63b3ed;
            box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.5);
          }
          .button {
            width: 100%;
            padding: 8px;
            margin-top: 16px;
            border: none;
            border-radius: 4px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
          }
          .button.blue {
            background-color: #4299e1;
          }
          .button.blue:hover {
            background-color: #3182ce;
          }
          .button.green {
            background-color: #48bb78;
          }
          .button.green:hover {
            background-color: #38a169;
          }
          .error-message {
            color: #e53e3e;
            text-align: center;
          }
          .meal-plan, .saved-recipes {
            margin-top: 24px;
          }
          .meal-plan h2, .saved-recipes h2 {
            font-size: 20px;
            font-weight: 600;
            color: #2d3748;
          }
          .meal-card, .recipe-card {
            background-color: white;
            padding: 16px;
            margin-top: 8px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          }
          .meal-card h3, .recipe-card h3 {
            font-size: 18px;
            font-weight: 600;
            color: #3182ce;
          }
          .recipe-card h3 {
            color: #38a169;
          }
          .meal-card p, .recipe-card p {
            color: #4a5568;
          }
          .meal-card ul, .recipe-card ul {
            margin-top: 8px;
            padding-left: 20px;
            color: #4a5568;
          }
          .meal-card li, .recipe-card li {
            margin-bottom: 4px;
          }
        `}
      </style>

      <h1>Meal Planner</h1>
      <div className="input-group">
        <label>Calories:</label>
        <input
          type="number"
          value={calories}
          onChange={(e) => setCalories(e.target.value)}
        />
        <label>Meals:</label>
        <input
          type="number"
          value={meals}
          onChange={(e) => setMeals(e.target.value)}
        />
        <button className="button blue" onClick={fetchMealPlan}>
          Generate Meal Plan
        </button>
        <button className="button green" onClick={fetchSavedRecipes}>
          Show Saved Recipes
        </button>
      </div>

      {error && <p className="error-message">{error}</p>}

      {showMealPlan && (
        <div className="meal-plan">
          <h2>Generated Meal Plan</h2>
          {mealPlan.map((meal) => (
            <div key={meal.id} className="meal-card">
              <h3>{meal.title} - {meal.calories} kcal</h3>
              <p>{meal.description}</p>
              <ul>
                {meal.ingredients.map((ing) => (
                  <li key={ing.id}>{ing.amount} {ing.unit} {ing.name}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}

      {showRecipes && (
        <div className="saved-recipes">
          <h2>Saved Recipes</h2>
          {recipes.map((recipe) => (
            <div key={recipe.id} className="recipe-card">
              <h3>{recipe.title} - {recipe.calories} kcal</h3>
              <p>{recipe.description}</p>
              <ul>
                {recipe.ingredients.map((ing) => (
                  <li key={ing.id}>{ing.amount} {ing.unit} {ing.name}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}