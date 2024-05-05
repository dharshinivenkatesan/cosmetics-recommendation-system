import pandas as pd

# Load the dataset (replace 'cosmetics.csv' with your actual CSV file path)
df = pd.read_csv('mini_project/cosmetics.csv')

# Define the options for product types
product_types = ['Moisturizer', 'Cleanser', 'Treatment', 'Face Mask', 'Eye cream', 'Sun protect']

# Ask the user to select the type of product
print("Please select the type of product:")
for i, product_type in enumerate(product_types, 1):
    print(f"{i}. {product_type}")

# Validate user input for product type
while True:
    try:
        selection = int(input("Enter the number corresponding to your choice: "))
        if selection < 1 or selection > len(product_types):
            raise ValueError
        break
    except ValueError:
        print("Invalid input. Please enter a number between 1 and", len(product_types))

# Get the selected product type
selected_product_type = product_types[selection - 1]

# Filter products by the selected product type
products_for_product_type = df[df['Label'] == selected_product_type]

# Ask the user for their skin type
skin_type_options = ['Dry', 'Normal', 'Oily', 'Sensitive', 'Combination']
print("\nPlease select your skin type:")
for i, skin_type_option in enumerate(skin_type_options, 1):
    print(f"{i}. {skin_type_option}")

# Validate user input for skin type
while True:
    try:
        skin_type_selection = int(input("Enter the number corresponding to your choice: "))
        if skin_type_selection < 1 or skin_type_selection > len(skin_type_options):
            raise ValueError
        break
    except ValueError:
        print("Invalid input. Please enter a number between 1 and", len(skin_type_options))

# Get the selected skin type
selected_skin_type = skin_type_options[skin_type_selection - 1]

# Ask the user if they want to filter by price
print("\nDo you want to filter by price?")
print("1. Yes")
print("2. No")

# Validate user input for filtering by price
while True:
    try:
        price_filter_selection = int(input("Enter the number corresponding to your choice: "))
        if price_filter_selection not in [1, 2]:
            raise ValueError
        break
    except ValueError:
        print("Invalid input. Please enter 1 for Yes or 2 for No.")

# Filter products based on skin type
filtered_products = products_for_product_type[products_for_product_type[selected_skin_type.capitalize()] == 1]

# If user wants to filter by price
if price_filter_selection == 1:
    print("\nPlease select the price range:")
    print("1. Less than 70")
    print("2. More than 70")

    # Validate user input for price range
    while True:
        try:
            price_range_selection = int(input("Enter the number corresponding to your choice: "))
            if price_range_selection not in [1, 2]:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter 1 for Less than 70 or 2 for More than 70.")

    # Filter products by the selected price range
    if price_range_selection == 1:
        filtered_products = filtered_products[filtered_products['Price'] < 70]
    else:
        filtered_products = filtered_products[filtered_products['Price'] > 70]

# Recommend a cosmetic based on filtered criteria
if not filtered_products.empty:
    recommended_cosmetic = filtered_products.sample(1)
    print(f"\nRecommended Cosmetic for {selected_skin_type} skin, under the {selected_product_type} category:")
    print(f"Name: {recommended_cosmetic['Name'].values[0]}")
    print(f"Brand: {recommended_cosmetic['Brand'].values[0]}")
    print(f"Price: {recommended_cosmetic['Price'].values[0]}")
    print(f"Ingredients: {recommended_cosmetic['Ingredients'].values[0]}")
else:
    print(f"Sorry, no {selected_product_type.lower()} suitable for {selected_skin_type.lower()} skin found.")
