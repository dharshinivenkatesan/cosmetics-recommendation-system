import streamlit as st
import pandas as pd
import pickle
import urllib.parse

# Load the dataset
df = pd.read_csv('mini_project/cosmetics.csv')

# Define the options for product types
product_types = ['Moisturizer', 'Cleanser', 'Treatment', 'Face Mask', 'Eye cream', 'Sun protect']

# Extract skin type from URL query parameters
query_params = st.experimental_get_query_params()
skin_type = query_params.get("skin_type", ["Combination"])[0]

# Display skin type from the URL
st.write(f"Detected Skin Type: {skin_type}")

# Render the HTML skin type quiz
st.markdown(open("skin_type_quiz.html", "r").read(), unsafe_allow_html=True)

# Get skin type from the quiz result
skin_type_from_quiz = st.empty()

# Check if the quiz has been submitted
if st.button("Submit"):
    # Get skin type from the quiz
    skin_type_from_quiz = skin_type_from_quiz.text
    # Filter products by the selected skin type
    filtered_products = df[df[skin_type_from_quiz] == 1]

    # Ask the user to select the type of product
    selected_product_type = st.selectbox("Select the type of product:", options=product_types)

    # Filter products by the selected product type
    products_for_product_type = filtered_products[filtered_products['Label'] == selected_product_type]

    # Display recommended cosmetic if available
    if not products_for_product_type.empty:
        # Load pre-trained model
        with open('pretrained_model.pkl', 'rb') as f:
            model = pickle.load(f)

        # Predict recommended cosmetic
        input_features = [1 if skin_type_from_quiz == label else 0 for label in ['Oily', 'Dry', 'Normal', 'Sensitive', 'Combination']]
        input_features += [1 if selected_product_type == label else 0 for label in ['Moisturizer', 'Cleanser', 'Treatment', 'Face Mask', 'Eye cream', 'Sun protect']]
        input_features = [input_features]
        recommended_product = model.predict(input_features)[0]

        st.header(f"Recommended Cosmetic for {skin_type_from_quiz} skin, under the {selected_product_type} category:")
        st.write(f"Product Type: {recommended_product}")
    else:
        st.warning(f"No {selected_product_type.lower()} suitable for {skin_type_from_quiz.lower()} skin found.")
