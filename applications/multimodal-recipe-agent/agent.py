#!/usr/bin/env python3
"""
Multimodal Recipe Agent with LanceDB and PydanticAI

A complete AI agent for recipe search with multimodal capabilities.
Uses LanceDB for data storage and PydanticAI for intelligent reasoning.
"""

import base64
from typing import Any, Dict, List, Optional

import lancedb
import torch
from dotenv import load_dotenv
from PIL import Image
from pydantic_ai import Agent
from sentence_transformers import SentenceTransformer
from transformers import CLIPModel, CLIPProcessor

# Load environment variables
load_dotenv()

# Configure Logfire with PydanticAI integration
try:
    import os

    import logfire

    # Check if Logfire environment variables are set
    logfire_token = os.getenv("LOGFIRE_TOKEN")
    logfire_project = os.getenv("LOGFIRE_PROJECT")

    if logfire_token and logfire_project:
        # Configure Logfire (will use environment variables)
        logfire.configure()

        # Instrument PydanticAI for automatic logging of agent calls, tool calls, and LLM calls
        logfire.instrument_pydantic_ai()

        print("✅ Logfire configured and PydanticAI instrumented")
        print(
            "📊 All agent calls, tool calls, and LLM interactions will be automatically logged"
        )
    else:
        print(
            "⚠️  Logfire environment variables not set (LOGFIRE_TOKEN, LOGFIRE_PROJECT)"
        )
        print("📝 Logfire logging disabled - agent will run without logging")
        logfire = None
except Exception as e:
    print(f"⚠️  Logfire configuration failed: {e}")
    print("📝 Logfire logging disabled - agent will run without logging")
    logfire = None

# Configuration
LANCEDB_PATH = "data/recipes.lance"
TEXT_MODEL = "all-MiniLM-L6-v2"
IMAGE_MODEL = "openai/clip-vit-base-patch32"
MAX_RESULTS = 10


class RecipeSearchTools:
    """Tools for the PydanticAI agent"""

    def _safe_convert(self, value):
        """Safely convert numpy types to Python types for JSON serialization"""
        import numpy as np

        if isinstance(value, np.ndarray):
            if value.size == 1:  # scalar array
                return value.item()
            else:  # multi-element array
                return value.tolist()
        elif (
            hasattr(value, "item") and hasattr(value, "size") and value.size == 1
        ):  # numpy scalar
            return value.item()
        elif hasattr(value, "tolist"):  # other numpy array-like
            return value.tolist()
        elif isinstance(value, (list, tuple)):
            return [self._safe_convert(item) for item in value]
        else:
            return value

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🔧 Using device: {self.device}")

        # Load models
        print("📥 Loading models...")
        self.text_model = SentenceTransformer(TEXT_MODEL)
        self.text_model.to(self.device)

        self.image_model = CLIPModel.from_pretrained(IMAGE_MODEL)
        self.image_processor = CLIPProcessor.from_pretrained(IMAGE_MODEL)
        self.image_model.to(self.device)

        # Connect to database
        self.db = lancedb.connect(LANCEDB_PATH)
        self.table = self.db.open_table("recipes")

        print("✅ Tools ready!")

    def search_recipes_by_text(
        self, query: str, limit: int = MAX_RESULTS
    ) -> List[Dict[str, Any]]:
        """Search recipes by text query"""
        # Generate query embedding
        query_embedding = self.text_model.encode(
            [query], convert_to_tensor=True, device=self.device
        )
        query_vector = query_embedding.cpu().numpy().flatten()

        # Search in LanceDB using text embeddings
        results = (
            self.table.search(query_vector, vector_column_name="text_embedding")
            .limit(limit)
            .to_pandas()
        )

        # Convert to list of dicts for PydanticAI
        recipes = []
        for _, row in results.iterrows():
            recipe = {
                "id": self._safe_convert(row["id"]),
                "title": self._safe_convert(row["title"]),
                "ingredients": self._safe_convert(row["ingredients"]),
                "ingredient_tags": self._safe_convert(row.get("ingredient_tags", [])),
                "instructions": self._safe_convert(row["instructions"]),
                "num_ingredients": self._safe_convert(row["num_ingredients"]),
                "image_name": self._safe_convert(row["image_name"]),
                "score": self._safe_convert(row.get("_distance", 0)),
            }
            recipes.append(recipe)

        return recipes

    def search_recipes_by_image(
        self, image_path: str, limit: int = MAX_RESULTS
    ) -> List[Dict[str, Any]]:
        """Search recipes by image"""
        try:
            # Load and process image
            image = Image.open(image_path).convert("RGB")
            inputs = self.image_processor(
                images=image, return_tensors="pt", padding=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Generate image embedding
            with torch.no_grad():
                image_features = self.image_model.get_image_features(**inputs)
                image_features = image_features / image_features.norm(
                    dim=-1, keepdim=True
                )

            query_vector = image_features.cpu().numpy().flatten()

            # Search in LanceDB using image embeddings
            results = (
                self.table.search(query_vector, vector_column_name="image_embedding")
                .limit(limit)
                .to_pandas()
            )

            # Convert to list of dicts for PydanticAI
            recipes = []
            for _, row in results.iterrows():
                recipe = {
                    "id": self._safe_convert(row["id"]),
                    "title": self._safe_convert(row["title"]),
                    "ingredients": self._safe_convert(row["ingredients"]),
                    "ingredient_tags": self._safe_convert(
                        row.get("ingredient_tags", [])
                    ),
                    "instructions": self._safe_convert(row["instructions"]),
                    "num_ingredients": self._safe_convert(row["num_ingredients"]),
                    "image_name": self._safe_convert(row["image_name"]),
                    "score": self._safe_convert(row.get("_distance", 0)),
                }
                recipes.append(recipe)

            return recipes

        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return []

    def get_available_ingredients(self) -> List[str]:
        """Get all unique ingredients in the dataset"""
        try:
            # Get all ingredient tags
            results = self.table.search().select(["ingredients"]).to_pandas()
            all_ingredients = set()

            for _, row in results.iterrows():
                if row["ingredients"]:
                    all_ingredients.update(row["ingredients"])

            return sorted(list(all_ingredients))
        except Exception as e:
            print(f"Error getting ingredients: {e}")
            return []

    def browse_recipes(self, limit: int = MAX_RESULTS) -> List[Dict[str, Any]]:
        """Browse all recipes"""
        try:
            results = self.table.search().limit(limit).to_pandas()

            recipes = []
            for _, row in results.iterrows():
                recipe = {
                    "id": self._safe_convert(row["id"]),
                    "title": self._safe_convert(row["title"]),
                    "ingredients": self._safe_convert(row["ingredients"]),
                    "ingredient_tags": self._safe_convert(
                        row.get("ingredient_tags", [])
                    ),
                    "instructions": self._safe_convert(row["instructions"]),
                    "num_ingredients": self._safe_convert(row["num_ingredients"]),
                    "image_name": self._safe_convert(row["image_name"]),
                }
                recipes.append(recipe)

            return recipes
        except Exception as e:
            print(f"Error browsing recipes: {e}")
            return []

    def get_recipe_image_base64_from_binary(self, recipe_id: str) -> Optional[str]:
        """Get recipe image as base64 from stored binary data in database"""
        try:
            result = self.table.search().where(f"id = '{recipe_id}'").to_pandas()
            if len(result) > 0:
                row = result.iloc[0]
                image_binary = row.get("image_binary")
                if image_binary is not None:
                    return base64.b64encode(image_binary).decode("utf-8")
        except Exception as e:
            print(f"Error getting image binary for recipe {recipe_id}: {e}")
        return None

    def get_recipes_with_images(self, query: str, limit: int = MAX_RESULTS) -> str:
        """Search recipes and return formatted response with image placeholders"""
        try:
            recipes = self.search_recipes_by_text(query, limit)

            if not recipes:
                return "No recipes found matching your query."

            response_parts = []
            response_parts.append(
                f"Here are {len(recipes)} recipes that match your query:\n"
            )

            for recipe in recipes:
                response_parts.append(f"## {recipe['title']}")
                response_parts.append(
                    f"**Ingredients:** {recipe['num_ingredients']} ingredients"
                )

                # Add ingredients list
                if recipe.get("ingredients"):
                    ingredients_text = ", ".join(
                        recipe["ingredients"][:5]
                    )  # Show first 5 ingredients
                    if len(recipe["ingredients"]) > 5:
                        ingredients_text += "..."
                    response_parts.append(f"*{ingredients_text}*")

                # Add instructions preview
                if recipe.get("instructions"):
                    instructions = recipe["instructions"]
                    if len(instructions) > 200:
                        instructions = instructions[:200] + "..."
                    response_parts.append(f"**Instructions:** {instructions}")

                # Use placeholder for image - will be replaced by app
                response_parts.append(f"![Recipe Image]({recipe['id']})")

                response_parts.append("---\n")

            return "\n".join(response_parts)

        except Exception as e:
            return f"Error searching recipes: {str(e)}"

    def get_recipes_with_images_from_image(
        self, image_path: str, limit: int = MAX_RESULTS
    ) -> str:
        """Search recipes by image and return formatted response with image placeholders"""
        try:
            recipes = self.search_recipes_by_image(image_path, limit)

            if not recipes:
                return "No recipes found matching the uploaded image."

            response_parts = []
            response_parts.append(
                f"Here are {len(recipes)} recipes that match your uploaded image:\n"
            )

            for recipe in recipes:
                response_parts.append(f"## {recipe['title']}")
                response_parts.append(
                    f"**Ingredients:** {recipe['num_ingredients']} ingredients"
                )

                # Add ingredients list
                if recipe.get("ingredients"):
                    ingredients_text = ", ".join(
                        recipe["ingredients"][:5]
                    )  # Show first 5 ingredients
                    if len(recipe["ingredients"]) > 5:
                        ingredients_text += "..."
                    response_parts.append(f"*{ingredients_text}*")

                # Add instructions preview
                if recipe.get("instructions"):
                    instructions = recipe["instructions"]
                    if len(instructions) > 200:
                        instructions = instructions[:200] + "..."
                    response_parts.append(f"**Instructions:** {instructions}")

                # Use placeholder for image - will be replaced by app
                response_parts.append(f"![Recipe Image]({recipe['id']})")

                response_parts.append("---\n")

            return "\n".join(response_parts)

        except Exception as e:
            return f"Error searching recipes by image: {str(e)}"


# Initialize tools
tools_instance = RecipeSearchTools()

# Create PydanticAI agent
agent = Agent(
    "gpt-4o-mini",
    tools=[
        tools_instance.get_recipes_with_images,
        tools_instance.get_recipes_with_images_from_image,
        tools_instance.get_available_ingredients,
    ],
    system_prompt="""You are a helpful recipe assistant. You can search for recipes by text or image.

CRITICAL RULES - FOLLOW THESE EXACTLY:
1. ALWAYS use the provided tools to search for recipes - NEVER generate recipe responses manually
2. When user provides an image path (e.g., "path: /path/to/image.jpg"), use get_recipes_with_images_from_image tool with that exact path
3. For ANY text-based recipe search request, use get_recipes_with_images tool  
4. These tools automatically format recipes with image placeholders that will be replaced by the app
5. NEVER use external image URLs like https://via.placeholder.com or any other external image services
6. ONLY use the exact format: ![Recipe Image](recipe_id) for image placeholders
7. The app will automatically replace these placeholders with actual recipe images
8. DO NOT generate your own recipe responses - always use the tools

Be helpful and provide detailed recipe information with proper markdown formatting.""",
)


def main():
    """Test the agent"""
    print("🍳 Multimodal Recipe Agent")
    print("=" * 40)

    # Test the agent
    print("\n🔍 Testing agent...")

    # Test text search
    result = agent.run_sync("Find me some chicken pasta recipes")
    print(f"Agent response: {result.data}")

    print("\n✅ Agent test completed!")


if __name__ == "__main__":
    main()
