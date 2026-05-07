import streamlit as st
import google.generativeai as genai
import os

# 1. Page Configuration
st.set_page_config(page_title="Slovenia Shopping Auditor", page_icon="🛍️", layout="wide")

# 2. API Setup
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# THE FIX: Changed 'google_search_retrieval' to 'google_search' 
# and verified 'gemini-3-flash-preview' for 2026.
model = genai.GenerativeModel(
    model_name='gemini-3-flash-preview',
    tools=[{"google_search": {}}]
)

st.title("🛍️ Slovenia Smart Shopping Auditor")
st.subheader("May 2026 - Live Price Comparison")

st.markdown("""
Input your list in **Slovenian, English, or Serbian**. 
I will search live flyers (Spar, Mercator, Lidl, Hofer), calculate subtotals, and apply coupon logic (like Spar's 10% off total).
""")

# 3. User Input
user_list = st.text_area("Your Groceries:", 
    placeholder="1kg piletine\n500g mletov goveje meso\n1kg bananas\n10 jajc\n...",
    height=250)

if st.button("🚀 Find Best Deals", type="primary"):
    if user_list:
        with st.spinner("🔍 Checking flyers and calculating discounts..."):
            try:
                # We mention the current date (May 7, 2026) to help the AI find the right catalogs
                prompt = f"""
                Today is Thursday, May 7, 2026. 
                Search live Slovenian retail sites (Spar.si, Mercator.si, Lidl.si, Hofer.si).
                
                For this list: {user_list}
                
                1. Identify prices for each item.
                2. Apply 'Total Bill' logic:
                   - Spar: If total > 30€, subtract 10%.
                   - Mercator: Note any 'Pika' member discounts.
                3. Compare the final totals between all stores.
                
                Format as a clean table and recommend the single best store to visit.
                Understand Slo/Eng/Srb mixed inputs. Response in English.
                """
                
                response = model.generate_content(prompt)
                
                st.success("Audit Complete!")
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                # This will capture any further tool name mismatches
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter your items first!")
