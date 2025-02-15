import streamlit as st

st.markdown(
    """
    Thank you for choosing us! Welcome to Agent User Guide 👋

    Here’s how you can use this chat:

    💁‍♀️ Get Help with Services:
    - Give me list categories
    - Give me list policies
    - Do you allow return product?
    - What is your privacy policy?
    - Do you offer free shipping?

    💁‍♀️ Inquire About Products in Store:
    - Give me product "Dreamy Styled Collar Shirts"
    - Compare "Straight Cut Button-down Collar Shirt" with "DIVAS Polo T-shirt"
    - Is "Magnolia Tuytsi Blazer" in stock?
    - Do you have "Magnolia Tuytsi Blazer" in size L?
    - Give me some products in category "jacket".

    💁‍♀️ Find FAQs Quickly:
    - How can I change the delivery address for my order?
    - How can I maintain the shape of my clothing?

    💁‍♀️ Create support ticket:
    - I want to create a support ticket.
    - Help me create a support ticket with below details:
        - Name: "John Doe"
        - Email: "john.doe@gmail.com"
        - Subject: "I have a problem with my order"
        - Description: "I received the wrong item in my order. Help me resolve this issue."

    ---

    🎯 Tip:
    - Use example to get started easily.
    - Be as short and specific as possible.
    ---
    """
)

# expander = st.expander("🎁 Best-seller products:")
# expander.markdown(
#     """
# 👚 Shirts
# - Lucille Silk Collared Shirt
# - SAPPHIRE Cotton Shirt
# - Long Sleeves Tencel Shirt
# - French Style Vest (with Croptop)
# - Tencel Silk Shirt with Ruffled Detail
# - Sleeves Style Shirt
# - Short-Sleeve Office Blazer
# - Straight-Leg Jeans in Slate Blue

# 👗 Dresses
# - Viscose Printed Dress Set
# - Pauline Neckline Fitted Dress

# 🧥 Coats
# - Queen Style Pleated T-shirt
# - Short-Sleeve Office Blazer

# 👖 Pants
# - Serge Checkered Wide-Leg Pants
# - Straight-Leg Jeans in Slate Blue
# - Skort Design Shorts

# 👕 T-shirt
# - Dinosaur T-shirt
# - Cloud T-shirt Set
# """
# )
st.markdown("---")

st.page_link("pages/agent.py", label="Let’s get started!", icon="🛍️")
