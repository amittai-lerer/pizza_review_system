# 
import streamlit as st
from core import get_pizza_answer
from llm_loader import is_running_in_docker

# st.set_option("server.fileWatcherType", "none")

# --- Page Setup ---
st.set_page_config(page_title="🍕 Israeli Pizza Recommender", layout="centered")
st.title("🍕 Ask Me About Pizza in Israel!")

# --- Question Input in a Form ---
with st.form("pizza_query_form", clear_on_submit=False):
    question = st.text_input("What's your pizza craving today?")
    submit = st.form_submit_button("🔥 Get Recommendation")

# --- Environment Display ---
host = "ollama" if is_running_in_docker() else "localhost"
source = "Docker" if is_running_in_docker() else "Mac"
st.caption(f"🧠 Using Local LLM (Ollama) at: `{host}`")
st.caption(f"💻 Running from: **{source}**")

# --- On Submit ---
if submit and question:
    with st.spinner("Thinking about your perfect slice..."):
        try:
            # Get response from core logic (uses get_llm_response internally)
            answer, docs, _ = get_pizza_answer(question, mode="local")
            st.success("Here's what we found!")

            # Show LLM info
            st.markdown("_🧠 Using: **Local LLaMA 3**_")

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
        except ConnectionError as e:
            st.error(str(e))
            st.info("Please make sure Ollama is running and the LLaMA model is installed. You can install it by running: `ollama pull llama3:latest`")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
