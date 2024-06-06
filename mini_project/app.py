import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_csv('mini_project/cosmetics.csv')

# Preprocessing
label_encoders = {}
for column in ['Brand', 'Name']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Encode 'Label' column (product type) as well
df['Label'] = LabelEncoder().fit_transform(df['Label'])

# Extract features and target
features = df.drop(columns=['Price', 'Rank', 'Ingredients'])
targets = df[['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

# Train a model for each skin type
models = {}
for skin_type in targets.columns:
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train[skin_type])
    models[skin_type] = model

# Streamlit app
st.title("Cosmetics Recommendation System")

# Get skin type from query parameter
query_params = st.experimental_get_query_params()
skin_type = query_params.get("skin_type", ["Combination"])[0]  # Default to 'Combination' if not provided

# Display skin type
st.write(f"Detected Skin Type: {skin_type}")

# Ask the user to select the type of product
product_types = LabelEncoder().fit(df['Label']).classes_
product_types = [ptype.title() for ptype in product_types]
selected_product_type = st.selectbox("Select the type of product:", options=product_types)

# Filter products by the selected product type
selected_product_type_encoded = LabelEncoder().fit(df['Label']).transform([selected_product_type.lower()])[0]
products_for_product_type = df[df['Label'] == selected_product_type_encoded]

# Ask the user if they want to filter by price
price_filter_selection = st.radio("Please select one to filter by price:", ('Less than $70', 'More than $70'))

# Extract price range based on user selection
if price_filter_selection == 'Less than $70':
    products_for_product_type = products_for_product_type[products_for_product_type['Price'] < 70]
else:
    products_for_product_type = products_for_product_type[products_for_product_type['Price'] > 70]

# Predict suitability using the trained model
model = models[skin_type]
X_product_features = products_for_product_type.drop(columns=['Price', 'Rank', 'Ingredients'])
product_predictions = model.predict(X_product_features)

# Filter products based on prediction
recommended_products = products_for_product_type[product_predictions == 1]

# Display recommended cosmetic if available
if not recommended_products.empty:
    recommended_cosmetic = recommended_products.sample(1)
    st.header(f"Recommended Cosmetic for {skin_type} skin, under the {selected_product_type} category:")
    st.write(f"Name: {label_encoders['Name'].inverse_transform([recommended_cosmetic['Name'].values[0]])[0]}")
    st.write(f"Brand: {label_encoders['Brand'].inverse_transform([recommended_cosmetic['Brand'].values[0]])[0]}")
    st.write(f"Price: ${int(recommended_cosmetic['Price'].values[0])}")  # Format price as integer with dollar symbol
    st.write(f"Ingredients: {recommended_cosmetic['Ingredients'].values[0]}")
else:
    st.warning(f"No {selected_product_type.lower()} suitable for {skin_type.lower()} skin found.")
