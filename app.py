import streamlit as st
from google import genai
from google.genai import types
import os

# 1. Page Configuration
st.set_page_config(page_title="Slovenia Shopping Auditor", page_icon="🛍️", layout="wide")

# 2. Modern API Setup (New for 2026)
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

st.title("🛍️ Slovenia Smart Shopping Auditor")
st.subheader("May 2026 - Live Price Comparison")

st.markdown("""
Input your list in **Slovenian, English, or Serbian**. 
I will search live flyers (Spar, Mercator, Lidl, Hofer), apply coupon math (like Spar's 10% off total).
""")

# 3. User Input
user_list = st.text_area("Your Groceries:", 
    placeholder="1kg piletine\n500g mletov goveje meso\n1kg bananas\n10 jajc\n...",
    height=250)

if st.button("🚀 Find Best Deals", type="primary"):
    if user_list:
        with st.spinner("🔍 Browsing Slovenian retail websites..."):
            try:
                # The instructions for the AI
                sys_instruct = "You are a shopping expert in Slovenia. Use Google Search to find real-time flyer prices for May 2026."
                
                # The search-grounded prompt
                prompt = f"""
                Analyze this grocery list: {user_list}
                
                1. Search live sites: Spar.si, Mercator.si, Lidl.si, Hofer.si.
                2. Apply math: If Spar total > 30€, subtract 10%. Note Pika/Lidl Plus deals.
                3. Compare totals and recommend the cheapest store.
                
                Output a clean table. Understand Slo/Eng/Srb. Response in English.
                """
                
                # THE FIX: This is the new way to enable Google Search
                response = client.models.generate_content(
                    model='gemini-3-flash', # Or 'gemini-3-flash-preview'
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=sys_instruct,
                        tools=[types.Tool(google_search=types.GoogleSearch())]
                    )
                )
                
                st.success("Audit Complete!")
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Ensure 'Google Search' is enabled in your API settings in Google AI Studio.")
    else:
        st.warning("Please enter your items first!")
