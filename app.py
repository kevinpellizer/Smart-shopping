import streamlit as st
import google.generativeai as genai
import os

# 1. Page Configuration
st.set_page_config(page_title="Slovenia Shopping Auditor", page_icon="🛒", layout="wide")

# 2. API & Search Setup
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# We use the model with 'google_search_retrieval' to get LIVE flyer data
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash', 
    tools=[{"google_search_retrieval": {}}]
)

st.title("🛒 Slovenia Smart Shopping Auditor")
st.subheader("May 2026 Edition - Live Flyer Comparison")

st.markdown("""
Enter your list in **Slovenian, English, or Serbian**. 
I will check Spar, Mercator, Lidl, and Hofer, apply coupon math (like the Spar 10% off over 30€), and find your winner.
""")

# 3. User Input
user_list = st.text_area("What do you need today?", 
    placeholder="1kg chicken\n500g mletov goveje meso\n1kg bananas\n10 eggs\n2 milk\n...",
    height=250)

if st.button("🚀 Audit Prices & Calculate Bill", type="primary"):
    if user_list:
        with st.spinner("🔍 Browsing Slovenian flyers and applying coupon logic..."):
            try:
                # The "Master Prompt" that handles all your requirements
                prompt = f"""
                You are a retail expert in Slovenia. Analyze this grocery list: {user_list}
                
                CURRENT CONTEXT: Today is Thursday, May 7, 2026. 
                
                STEPS:
                1. SEARCH: Look for live prices/flyers for Spar.si, Mercator.si, Lidl.si, and Hofer.si in Slovenia.
                2. COMPARE: Find the specific price for each item on the list at these stores. 
                3. COUPON LOGIC: 
                   - Spar: Check if the 10% off over 30€ coupon is active (usually Fri/Sat).
                   - Mercator: Check for Pika card discounts.
                   - Lidl/Hofer: Check for 'Akcija' prices.
                4. MATH: Sum up the total for each store. If a threshold like 30€ is met, apply the coupon percentage to the final bill.
                
                OUTPUT FORMAT:
                - A comparison table: | Item | Spar | Mercator | Lidl | Hofer |
                - A 'Calculated Bill' section for each store showing the Subtotal -> Coupon Applied -> Final Price.
                - A 'Winner' recommendation: 'Go to [Store] to save €X.XX'.
                
                Translate all items to Slovenian for searching, but provide the final report in English.
                """
                
                response = model.generate_content(prompt)
                
                st.success("Analysis Complete!")
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error searching flyers: {e}")
    else:
        st.warning("Please enter some items first!")
