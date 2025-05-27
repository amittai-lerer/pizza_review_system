# 
import streamlit as st
from core import get_pizza_answer
from llm_loader import is_running_in_docker

# --- Page Setup ---
st.set_page_config(page_title="🍕 Israeli Pizza Recommender", layout="centered")
st.title("🍕 Ask Me About Pizza in Israel!")

# --- LLM Mode Selection ---
llm_mode = st.radio("LLM Mode:", ["auto", "local", "cloud"], index=0, horizontal=True)

# --- Question Input in a Form ---
with st.form("pizza_query_form", clear_on_submit=False):
    question = st.text_input("What's your pizza craving today?")
    submit = st.form_submit_button("🔥 Get Recommendation")

# --- Environment Display ---
host = "ollama" if is_running_in_docker() else "localhost"
source = "Docker" if is_running_in_docker() else "Mac"
st.caption(f"🧠 LLM Host: `{host}`")
st.caption(f"💻 Running from: **{source}**, LLM Mode: `{llm_mode}`")

# --- On Submit ---
if submit and question:
    with st.spinner("Thinking about your perfect slice..."):
        # Get response from core logic (uses get_llm_response internally)
        answer, docs, used_mode = get_pizza_answer(question, mode=llm_mode)
        st.success("Here's what we found!")

        # Show LLM mode used
        mode_labels = {
            "local": "🧠 Using: **Local LLaMA 3.2**",
            "cloud": "☁️ Using: **Cloud LLaMA via Hugging Face**"
        }
        st.markdown(f"_{mode_labels.get(used_mode, '🤖 Using: Unknown')}_")

        # --- Display the Answer ---
        st.markdown(
            f"""
            <div style="background-color:#d4edda; padding:20px; border-radius:10px;">
                <strong>Answer:</strong> {answer}
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- Show supporting reviews (if any) ---
        if docs:
            with st.expander("📖 Show the reviews we used"):
                for i, doc in enumerate(docs):
                    restaurant = doc.metadata.get("restaurant", "N/A")
                    city = doc.metadata.get("city", "N/A")
                    state = doc.metadata.get("state", "")
                    rating = doc.metadata.get("rating", "N/A")
                    date = doc.metadata.get("date", "N/A")
                    review_text = doc.page_content

                    st.markdown(f"""
                    **Review {i+1}**  
                    🏠 *{restaurant}*  
                    🏙️ {city}{', ' + state if state else ''}  
                    ⭐ {rating} | 🗓 {date}  

                    **Review:**  
                    {review_text}

                    ---
                    """)
