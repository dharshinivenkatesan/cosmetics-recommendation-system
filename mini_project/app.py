import streamlit as st
import pandas as pd

# Load the dataset (replace 'cosmetics.csv' with your actual CSV file path)
df = pd.read_csv('mini_project/cosmetics.csv')

# Define the options for product types
product_types = ['Moisturizer', 'Cleanser', 'Treatment', 'Face Mask', 'Eye cream', 'Sun protect']

# Ask the user to select the type of product
selected_product_type = st.selectbox("Select the type of product:", options=product_types)

# Filter products by the selected product type
products_for_product_type = df[df['Label'] == selected_product_type]

# Ask the user for their skin type
skin_type_options = ['Dry', 'Normal', 'Oily', 'Sensitive', 'Combination']
selected_skin_type = st.selectbox("Select your skin type:", options=skin_type_options)

# Ask the user if they want to filter by price
price_filter_selection = st.radio("Do you want to filter by price?", ('Yes', 'No'))

# Filter products based on skin type
filtered_products = products_for_product_type[products_for_product_type[selected_skin_type.capitalize()] == 1]

# Filter products by price if selected
if price_filter_selection == 'Yes':
    price_range_selection = st.radio("Select the price range:", ('Less than 70', 'More than 70'))
    if price_range_selection == 'Less than 70':
        filtered_products = filtered_products[filtered_products['Price'] < $70]
    else:
        filtered_products = filtered_products[filtered_products['Price'] > $70]

# Display recommended cosmetic if available
if not filtered_products.empty:
    recommended_cosmetic = filtered_products.sample(1)
    st.header(f"Recommended Cosmetic for {selected_skin_type} skin, under the {selected_product_type} category:")
    st.write(f"Name: {recommended_cosmetic['Name'].values[0]}")
    st.write(f"Brand: {recommended_cosmetic['Brand'].values[0]}")
    st.write(f"Price: ${recommended_cosmetic['Price'].values[0]}")  # Add dollar symbol to price
    st.write(f"Ingredients: {recommended_cosmetic['Ingredients'].values[0]}")
else:
    st.warning(f"No {selected_product_type.lower()} suitable for {selected_skin_type.lower()} skin found.")
