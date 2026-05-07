import streamlit as st
import google.generativeai as genai
import os

# 1. Page Configuration
st.set_page_config(page_title="Slovenia Shopping Auditor", page_icon="🛍️", layout="wide")

# 2. API Setup
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Using Gemini 3 Flash Preview as per your working apps
# We enable the 'google_search_retrieval' tool so it can browse Spar, Lidl, etc.
model = genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
    tools=[{"google_search_retrieval": {}}]
)

st.title("🛍️ Slovenia Smart Shopping Auditor")
st.subheader("May 2026 - Real-Time Price Comparison")

st.markdown("""
Input your list in **Slovenian, English, or Serbian**. 
I will search live flyers (Spar, Mercator, Lidl, Hofer), calculate subtotals, and apply coupon logic (like Spar's 10% off total).
""")

# 3. User Input
user_list = st.text_area("Your Groceries:", 
    placeholder="1kg chicken\n500g mletov goveje meso\n1kg bananas\n10 eggs\n...",
    height=250)

if st.button("🚀 Find Best Deals", type="primary"):
    if user_list:
        with st.spinner("🔍 Chef Gemini is checking the flyers..."):
            try:
                prompt = f"""
                You are a retail assistant in Slovenia. 
                LIST: {user_list}
                
                DATE: Today is Thursday, May 7, 2026. 
                
                INSTRUCTIONS:
                1. Search live websites: Spar.si, Mercator.si, Lidl.si, Hofer.si, and Eurospin.si.
                2. Find specific prices for these items in Slovenia.
                3. APPLY MATH: 
                   - Spar: Apply 10% discount if the subtotal is over €30.
                   - Mercator: Note 'Pika' discounts.
                   - Lidl/Hofer: Note 'Akcija' prices.
                4. CALCULATE total for each store. 
                
                OUTPUT:
                - Comparison Table: | Item | Spar | Mercator | Lidl | Hofer |
                - Discount Explanation (e.g. 'You saved €3 at Spar because you hit the €30 limit').
                - Recommended Store: Which one is the absolute cheapest for this whole basket?
                
                Understand Slovenian, English, and Serbian inputs. Provide response in English.
                """
                
                # Generate content with search grounding
                response = model.generate_content(prompt)
                
                st.success("Audit Complete!")
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Check if your API Key has 'Google Search' enabled in the Google AI Studio settings.")
    else:
        st.warning("Please enter your items first!")
