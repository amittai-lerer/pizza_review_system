# --- app.py ---
import streamlit as st
from core import get_pizza_answer
import os
import logging




os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTORCH_NO_CUDA_MEMORY_CACHING"] = "1"

logging.getLogger("streamlit").setLevel(logging.WARNING)


# --- Page Setup ---
st.set_page_config(page_title="🍕 Israeli Pizza Recommender", layout="centered")
st.title("🍕 Ask Me About Pizza in Israel!")

# --- LLM Toggle ---
use_cloud = st.sidebar.checkbox("Use Fireworks AI (cloud LLM)", value=False)

# --- Question Input ---
with st.form("pizza_query_form", clear_on_submit=False):
    question = st.text_input("What's your pizza craving today?")
    submit = st.form_submit_button("🔥 Get Recommendation")

# --- On Submit ---
if submit and question:
    with st.spinner("Thinking about your perfect slice..."):
        try:
            # 👉 Pass the toggle as a parameter
            answer, docs = get_pizza_answer(question, use_cloud_llm=use_cloud)

            st.success("Here's what we found!")
            st.markdown("_🧠 Using: **Local LLaMA 3.2**_" if not use_cloud else "_☁️ Using: **Fireworks Cloud LLM**_")

            st.markdown(
                f"""
                <div style="background-color:#d4edda; padding:20px; border-radius:10px;">
                    <strong>Answer:</strong> {answer}
                </div>
                """,
                unsafe_allow_html=True
            )

            if docs:
                with st.expander("📖 Show the reviews we used"):
                    for i, doc in enumerate(docs):
                        st.markdown(f"""
                        **Review {i+1}**  
                        🏠 *{doc.metadata.get('restaurant', 'N/A')}*  
                        🌇 {doc.metadata.get('city', 'N/A')}  
                        ⭐ {doc.metadata.get('rating', 'N/A')} | 🗓 {doc.metadata.get('date', 'N/A')}  

                        **Review:**  
                        {doc.page_content}

                        ---
                        """)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
