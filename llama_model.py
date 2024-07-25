from langchain.llms import CTransformers
import streamlit as st
import torch


@st.cache_resource
def load_model():
    model_path = "llama-2-7b-chat.Q4_0.gguf-GGML/llama-2-7b-chat.Q4_0.gguf"
    llm = CTransformers(
        model=model_path,
        model_type="llama",
        config={
                'max_new_tokens': 1024,
                'temperature': 0.8,
                'top_p': 0.95,
                'top_k': 40,
                'repetition_penalty': 1.1,
                },
        device='cuda' if torch.cuda.is_available() else 'cpu'
    )
    return llm


def generate_dish_name(model, ingredients):
    prompt = f"Create a dish name using the following ingredients: {', '.join(ingredients)}.\nDish Name:"
    response = model(prompt)
    dish_name = response.strip().split('Dish Name:')[-1].split('\n')[0].strip()
    return dish_name


def generate_recipe(model, ingredients):
    dish_name = generate_dish_name(model, ingredients)
    prompt = f"Create a simple recipe for {dish_name} using the following ingredients: {', '.join(ingredients)}.\n\nIngredients:\n- {', '.join(ingredients)}\n\nInstructions:\n"
    response = model(prompt)
    recipe_lines = response.strip().split('\n')
    formatted_recipe = '\n'.join(line.strip() for line in recipe_lines if line.strip())
    # recipe = response.strip()
    return dish_name, formatted_recipe


def main():
    st.title("Cooking Assistant")
    st.write("Enter ingredients to get a dish name and recipe suggestion.")

    ingredients_input = st.text_input("Enter ingredients separated by commas")
    if st.button("Generate Recipe"):
        ingredients = [ingredient.strip() for ingredient in ingredients_input.split(',')]
        model = load_model()
        dish_name, recipe = generate_recipe(model, ingredients)

        st.subheader("Dish Name")
        st.write(dish_name)

        st.subheader("Generated Recipe")
        st.write(recipe)


if __name__ == "__main__":
    main()
