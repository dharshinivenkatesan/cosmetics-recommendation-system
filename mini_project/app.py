import streamlit as st
import pandas as pd
import urllib.parse

# Load the dataset
df = pd.read_csv('mini_project/cosmetics.csv')

# Define the options for product types
product_types = ['Moisturizer', 'Cleanser', 'Treatment', 'Face Mask', 'Eye cream', 'Sun protect']

# Get skin type from query parameter
query_params = st.experimental_get_query_params()
skin_type = query_params.get("skin_type", ["Combination"])[0]  # Default to 'Combination' if not provided

# Display skin type
st.write(f"Detected Skin Type: {skin_type}")

# Ask the user to select the type of product
selected_product_type = st.selectbox("Select the type of product:", options=product_types)

# Filter products by the selected product type
products_for_product_type = df[df['Label'] == selected_product_type]

# Ask the user if they want to filter by price
price_filter_selection = st.radio("Please select one to filter by price:", ('Less than $70', 'More than $70'))

# Extract price range based on user selection
if price_filter_selection == 'Less than $70':
    filtered_products = products_for_product_type[products_for_product_type['Price'] < 70]
else:
    filtered_products = products_for_product_type[products_for_product_type['Price'] > 70]

# Filter by skin type
filtered_products = filtered_products[filtered_products[skin_type] == 1]

# Display recommended cosmetic if available
if not filtered_products.empty:
    recommended_cosmetic = filtered_products.sample(1)
    st.header(f"Recommended Cosmetic for {skin_type} skin, under the {selected_product_type} category:")
    st.write(f"Name: {recommended_cosmetic['Name'].values[0]}")
    st.write(f"Brand: {recommended_cosmetic['Brand'].values[0]}")
    st.write(f"Price: ${int(recommended_cosmetic['Price'].values[0])}")  # Format price as integer with dollar symbol
    st.write(f"Ingredients: {recommended_cosmetic['Ingredients'].values[0]}")
else:
    st.warning(f"No {selected_product_type.lower()} suitable for {skin_type.lower()} skin found.")
