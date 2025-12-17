#!/usr/bin/env python3
"""
Recipe Data Import Script

This script imports recipe data, cleans it, generates embeddings, and stores it in LanceDB.
Based on the recipe-final project but simplified for the tutorial.
"""

import ast
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import lancedb
import numpy as np
import pandas as pd
import pyarrow as pa
import torch
from PIL import Image
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from transformers import CLIPModel, CLIPProcessor

# Configuration
DATA_DIR = "data"
CSV_FILE = "recipes.csv"
IMAGES_DIR = "data/images"
LANCEDB_PATH = "data/recipes.lance"

# Model settings
TEXT_MODEL = "all-MiniLM-L6-v2"  # Fast, efficient text embeddings
IMAGE_MODEL = "openai/clip-vit-base-patch32"  # Good image embeddings
BATCH_SIZE = 32


def load_data() -> pd.DataFrame:
    """Step 1: Load the CSV data"""
    print("📊 Step 1: Loading data...")
    print("📥 Make sure you've downloaded the dataset from:")
    print(
        "   https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images"
    )
    print("   and placed recipes.csv in the current directory")

    csv_path = os.path.join(DATA_DIR, CSV_FILE)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"CSV file not found at {csv_path}\n"
            "Please download the dataset from Kaggle and place recipes.csv in the data/ directory"
        )

    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df):,} recipes from CSV")
    return df


def clean_ingredients(ingredients_str: str) -> List[str]:
    """Clean and parse ingredients from string format"""
    if pd.isna(ingredients_str) or ingredients_str == "":
        return []

    try:
        # Try to parse as Python list
        if isinstance(ingredients_str, str) and ingredients_str.startswith("["):
            ingredients = ast.literal_eval(ingredients_str)
        else:
            # Split by comma and clean
            ingredients = [ing.strip().lower() for ing in ingredients_str.split(",")]

        # Filter out empty strings and clean
        ingredients = [ing for ing in ingredients if ing and len(ing) > 1]
        return ingredients
    except Exception as e:
        print(f"Error parsing ingredients '{ingredients_str}': {e}")
        return []


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Step 2: Clean and prepare the data"""
    print("🧹 Step 2: Cleaning data...")

    # Remove rows with missing essential data
    initial_count = len(df)
    df = df.dropna(subset=["title", "ingredients", "instructions"])
    df = df[df["title"].str.strip() != ""]
    df = df[df["ingredients"].str.strip() != ""]
    df = df[df["instructions"].str.strip() != ""]

    print(f"✅ Removed {initial_count - len(df):,} invalid recipes")

    # Clean ingredients
    df["ingredients"] = df["ingredients"].apply(clean_ingredients)

    # Add ingredient tags (simplified version)
    df["ingredient_tags"] = df["ingredients"].apply(lambda x: x[:10] if x else [])

    # Add num_ingredients
    df["num_ingredients"] = df["ingredients"].apply(len)

    # Add image_name if not present
    if "image_name" not in df.columns:
        df["image_name"] = df["id"].apply(lambda x: f"{x}.jpg")

    print(f"✅ Cleaned data: {len(df):,} recipes remaining")
    return df


def create_sample_images(df: pd.DataFrame) -> None:
    """Step 3: Create sample images for demonstration"""
    print("🖼️  Step 3: Creating sample images...")

    # Create images directory
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Create sample images with different colors
    colors = [
        (255, 200, 150),  # Orange
        (200, 255, 200),  # Green
        (200, 200, 255),  # Blue
        (255, 255, 200),  # Yellow
        (255, 200, 255),  # Pink
    ]

    for i, (_, row) in enumerate(df.iterrows()):
        # Create a simple colored image
        color = colors[i % len(colors)]
        image = Image.new("RGB", (224, 224), color)

        # Save the image
        image_path = os.path.join(IMAGES_DIR, row["image_name"])
        image.save(image_path, "JPEG")

    print(f"✅ Created {len(df)} sample images")


def load_models():
    """Step 4: Load embedding models"""
    print("🤖 Step 4: Loading models...")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Load text model
    text_model = SentenceTransformer(TEXT_MODEL)
    text_model.to(device)

    # Load image model
    image_model = CLIPModel.from_pretrained(IMAGE_MODEL)
    image_processor = CLIPProcessor.from_pretrained(IMAGE_MODEL)
    image_model.to(device)

    print("✅ Models loaded successfully")
    return text_model, image_model, image_processor, device


def generate_embeddings(
    df: pd.DataFrame, text_model, image_model, image_processor, device
):
    """Step 5: Generate embeddings for all recipes"""
    print("🔢 Step 5: Generating embeddings...")

    text_embeddings = []
    image_embeddings = []
    image_binaries = []

    for i, (_, row) in tqdm(df.iterrows(), total=len(df), desc="Processing recipes"):
        # Generate text embedding
        text_content = (
            f"{row['title']} {' '.join(row['ingredients'])} {row['instructions']}"
        )
        text_embedding = text_model.encode(
            [text_content], convert_to_tensor=True, device=device
        )
        text_vector = text_embedding.cpu().numpy().flatten()
        text_embeddings.append(text_vector)

        # Load and process image
        image_path = os.path.join(IMAGES_DIR, row["image_name"])
        try:
            image = Image.open(image_path).convert("RGB")

            # Convert to binary for storage
            img_buffer = io.BytesIO()
            image.save(img_buffer, format="JPEG")
            image_binary = img_buffer.getvalue()
            image_binaries.append(image_binary)

            # Generate image embedding
            inputs = image_processor(images=image, return_tensors="pt", padding=True)
            inputs = {k: v.to(device) for k, v in inputs.items()}

            with torch.no_grad():
                image_features = image_model.get_image_features(**inputs)
                image_features = image_features / image_features.norm(
                    dim=-1, keepdim=True
                )

            image_vector = image_features.cpu().numpy().flatten()
            image_embeddings.append(image_vector)

        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            # Create a zero vector as fallback
            image_embeddings.append(np.zeros(512))  # CLIP base model has 512 dims
            image_binaries.append(b"")

    print("✅ Embeddings generated successfully")
    return text_embeddings, image_embeddings, image_binaries


def create_lancedb_table(
    df: pd.DataFrame, text_embeddings, image_embeddings, image_binaries
):
    """Step 6: Create LanceDB table with all data"""
    print("💾 Step 6: Creating LanceDB table...")

    # Prepare data for LanceDB
    recipes_data = []

    for i, (_, row) in enumerate(df.iterrows()):
        recipe_data = {
            "id": row["id"],
            "title": row["title"],
            "ingredients": row["ingredients"],
            "ingredient_tags": row["ingredient_tags"],
            "instructions": row["instructions"],
            "image_name": row["image_name"],
            "text_embedding": text_embeddings[i],
            "image_embedding": image_embeddings[i],
            "image_binary": image_binaries[i],
            "num_ingredients": row["num_ingredients"],
        }
        recipes_data.append(recipe_data)

    # Connect to LanceDB
    db = lancedb.connect(LANCEDB_PATH)

    # Drop existing table if it exists
    if "recipes" in db.table_names():
        db.drop_table("recipes")

    # Create new table
    table = db.create_table("recipes", recipes_data)

    print(f"✅ LanceDB table created with {len(recipes_data):,} recipes")
    print(f"Table schema: {table.schema}")

    return table


def main():
    """Main import process"""
    print("🍳 Recipe Data Import Process")
    print("=" * 50)

    try:
        # Step 1: Load data
        df = load_data()

        # Step 2: Clean data
        df = clean_data(df)

        # Step 3: Create sample images
        create_sample_images(df)

        # Step 4: Load models
        text_model, image_model, image_processor, device = load_models()

        # Step 5: Generate embeddings
        text_embeddings, image_embeddings, image_binaries = generate_embeddings(
            df, text_model, image_model, image_processor, device
        )

        # Step 6: Create LanceDB table
        table = create_lancedb_table(
            df, text_embeddings, image_embeddings, image_binaries
        )

        print("\n🎉 Import process completed successfully!")
        print(f"📊 Total recipes imported: {len(df):,}")
        print(f"💾 Database location: {LANCEDB_PATH}")
        print(f"🖼️  Images location: {IMAGES_DIR}")

    except Exception as e:
        print(f"❌ Error during import: {e}")
        raise


if __name__ == "__main__":
    main()
