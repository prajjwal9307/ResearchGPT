import streamlit as st

from utils.pdf_processor import extract_text_from_pdf, save_uploaded_file


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
    st.header("About")

    st.write("""
    ResearchGPT is an AI-powered
    research assistant for scientific papers.
    """)

# File Upload

uploaded_file=st.file_uploader(
    "Upload Research Paper (PDF)",
    type=["pdf"]
)

# Process The Uploaded File
if uploaded_file is not None:
    st.success("PDF Uploaded Successfully!")
    # Save PDF
    pdf_path=save_uploaded_file(uploaded_file)

    st.write("Saved File Path:")
    st.code(pdf_path)

# Extract Text Button
if st.button("Extract Text"):
    try:
        with st.spinner("Extracting Text..."):
            extracted_text = extract_text_from_pdf(pdf_path)
        
        st.success("Text Extracted Successfully!")
        st.subheader("Extracted Text")

        st.text_area(
            label="Research Paper Content",
            value=extracted_text,
            height=500
        )
    except Exception as e:
        st.error(f"Error: {str(e)}")

    



