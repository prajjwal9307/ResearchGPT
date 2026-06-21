import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="ResearchGPT",
    page_icon="📚",
    layout="wide"
)

# Title
st.title("📚 ResearchGPT")

st.write("Welcome to ResearchGPT!")

st.write("An AI Research Assistance for Scientific Papers")

# Sidebar
with st.sidebar:
    st.header("Project Information")

    st.write("Version: 1.0")

    st.write("Built using:")
    st.write("- Streamlit")
    st.write("- LangChain")
    st.write("- Groq")
    st.write("- ChromaDB")