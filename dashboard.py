import streamlit as st
from main import get_pizza_answer

st.set_page_config(page_title="🍕 Israeli Pizza Recommender", layout="centered")
st.title("🍕 Israeli Pizza Advisor")
st.markdown("Ask anything about pizza in Israeli cities:")

question = st.text_input("Your pizza-related question:")

if question:
    with st.spinner("Retrieving tasty insights..."):
        answer, city, rewritten, reviews = get_pizza_answer(question)
        st.markdown("### ✅ Answer")
        st.success(answer)

        with st.expander("📄 See matched reviews"):
            st.code(reviews, language="markdown")
