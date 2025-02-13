"""
Views for the recipe APIs
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.utils import generate_meal_plan, generate_meal_plan_testing
import json

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe import serializers
from recipe.serializers import RecipeSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            ),
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all() #All models for the database
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids) # Reduce the query to the ones with the tags user specified
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids) # Reduce the query to ones with the ingredients 

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['POST'], detail=False, url_path='generate-meal-plan')
    def generate_meal_plan_view(self, request):
        """Generate multiple recipes to fit a caloric requirement."""
        calories_per_day = request.data.get('calories', 1800)
        num_meals = request.data.get('meals', 3)

        meal_data = generate_meal_plan(calories_per_day, num_meals)
        print(f"Parsed meal_data: {meal_data}")
        print(f"Type of meal_data: {type(meal_data)}")


        if meal_data is None:
            return Response({"error": "Invalid JSON response from OpenAI"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not isinstance(meal_data, list):
            return Response({"error": "Expected a list of meals"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        created_recipes = []
        for meal in meal_data:
            if not all(k in meal for k in ["title", "description", "ingredients", "calories"]):
                return Response({"error": "Missing keys in OpenAI response"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            recipe = Recipe.objects.create(
                user=request.user,
                title=meal['title'],
                description=meal['description'],
                time_minutes=meal.get('time_minutes', 10),
                price=meal.get('price', 0),
                link=meal.get('link', ''),
            )

            # Add ingredients
            ingredients = []
            for ing in meal['ingredients']:
                ingredient_obj, _ = Ingredient.objects.get_or_create(
                    name=ing['name'], 
                    user=request.user
                )
                ingredients.append(ingredient_obj)

            recipe.ingredients.set(ingredients)
            created_recipes.append(RecipeSerializer(recipe).data)

        return Response(created_recipes, status=status.HTTP_201_CREATED)

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes.',
            ),
        ]
    )
)
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
