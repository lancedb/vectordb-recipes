#!/usr/bin/env python3
"""
Streamlit Recipe Chat App

A complete Streamlit chat application for recipe search using the multimodal agent.
"""

import io
from typing import Any, Dict

import streamlit as st
from agent import agent
from PIL import Image

# Page config
st.set_page_config(page_title="Multimodal Recipe Chat", page_icon="🍳", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None


def display_image(image_binary: bytes) -> None:
    """Display image from binary data"""
    if image_binary:
        try:
            image = Image.open(io.BytesIO(image_binary))
            st.image(image, width=200)
        except Exception as e:
            st.error(f"Error displaying image: {e}")
    else:
        st.info("No image available")


def display_recipe(recipe: Dict[str, Any]) -> None:
    """Display a single recipe in chat"""
    with st.container():
        col1, col2 = st.columns([1, 3])

        with col1:
            if recipe.get("image_binary"):
                display_image(recipe["image_binary"])
            else:
                st.info("No image")

        with col2:
            st.write(f"**{recipe['title']}**")
            st.write(f"*{recipe['num_ingredients']} ingredients*")

            # Show ingredient tags
            if recipe.get("ingredient_tags"):
                tags = ", ".join(recipe["ingredient_tags"][:8])
                if len(recipe["ingredient_tags"]) > 8:
                    tags += "..."
                st.write(f"*Ingredients: {tags}*")

            # Show instructions preview
            if recipe.get("instructions"):
                instructions = recipe["instructions"]
                if len(instructions) > 150:
                    instructions = instructions[:150] + "..."
                st.write(f"*Instructions: {instructions}*")


def replace_image_placeholders(response: str) -> str:
    """Replace recipe ID placeholders with actual base64 encoded images"""
    import re

    # Pattern to match ![any text](recipe_id) where recipe_id starts with "recipe_"
    placeholder_pattern = r"!\[.*?\]\((recipe_[^)]+)\)"

    def replace_placeholder(match):
        recipe_id = match.group(1)
        try:
            # Get base64 image data for this recipe
            from agent import tools_instance

            image_base64 = tools_instance.get_recipe_image_base64_from_binary(recipe_id)
            if image_base64:
                return f"data:image/jpeg;base64,{image_base64}"
            else:
                return "*No image available*"
        except Exception as e:
            print(f"Error loading image for recipe {recipe_id}: {e}")
            return "*No image available*"

    return re.sub(placeholder_pattern, replace_placeholder, response)


def display_enhanced_response(response: str) -> None:
    """Display agent response with enhanced formatting and image support"""
    import re

    # First replace placeholders with actual base64 images
    response = replace_image_placeholders(response)

    # Look for base64 image patterns in the response
    base64_pattern = r"data:image/[^;]+;base64,([A-Za-z0-9+/=]+)"
    matches = re.findall(base64_pattern, response)

    # Debug: Check if there are placeholder images that need to be removed
    placeholder_pattern = r"data:image/[^;]+;base64,\{base64_encoded_image\}"
    if re.search(placeholder_pattern, response):
        st.warning(
            "⚠️ Agent included placeholder image text instead of actual base64 data. This is a known issue."
        )
        # Remove the placeholder image text
        response = re.sub(placeholder_pattern, "", response)

    if matches:
        # If there are base64 images, process them
        parts = re.split(base64_pattern, response)

        for i, part in enumerate(parts):
            if i % 2 == 0:  # Text parts
                if part.strip():
                    st.markdown(part)
            else:  # Base64 image parts
                try:
                    # Decode base64 image
                    import base64

                    image_data = base64.b64decode(part)
                    image = Image.open(io.BytesIO(image_data))
                    st.image(image, width=300)
                except Exception as e:
                    st.error(f"Error displaying image: {e}")
    else:
        # No images, just display as markdown
        st.markdown(response)


def main():
    """Main app function"""
    st.title("🍳 Multimodal Recipe Chat")
    st.write("Chat with the recipe assistant to find recipes!")

    # Sidebar for image upload
    with st.sidebar:
        st.header("Upload Image")
        uploaded_file = st.file_uploader(
            "Upload an image for recipe search",
            type=["jpg", "jpeg", "png"],
            help="Upload an image to search for similar recipes",
        )

        if uploaded_file:
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.uploaded_image = temp_path

            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                display_enhanced_response(message["content"])
            else:
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about recipes..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # If there's an uploaded image, pass the image path to the agent
                    context = prompt
                    if st.session_state.uploaded_image:
                        context = f"{prompt} (I have uploaded an image at path: {st.session_state.uploaded_image})"

                    # Prepare conversation history for the agent using PydanticAI message types
                    from pydantic_ai.messages import (
                        ModelRequest,
                        ModelResponse,
                        TextPart,
                        UserPromptPart,
                    )

                    message_history = []
                    for msg in st.session_state.messages:
                        if msg["role"] == "user":
                            # Create a ModelRequest for user messages
                            user_request = ModelRequest.user_text_prompt(msg["content"])
                            message_history.append(user_request)
                        elif msg["role"] == "assistant":
                            # Create a ModelResponse for assistant messages
                            assistant_response = ModelResponse(
                                parts=[TextPart(content=msg["content"])]
                            )
                            message_history.append(assistant_response)

                    # Get response from agent with conversation history
                    result = agent.run_sync(context, message_history=message_history)

                    # Extract the actual response text from AgentRunResult
                    response = result.output

                    # Display the response with enhanced formatting
                    display_enhanced_response(response)

                    # Add assistant response to chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )

                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )

    # Clear chat button in sidebar
    with st.sidebar:
        st.header("Chat Controls")
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.uploaded_image = None
            st.rerun()


if __name__ == "__main__":
    main()
