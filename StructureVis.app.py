import streamlit as st
from io import StringIO

st.set_page_config(
    page_title='ProteinVista', 
    page_icon="🧬", 
    layout='wide', 
    initial_sidebar_state='auto'
)

# Sidebar title and file uploader
st.sidebar.title('Upload PDB File')
uploaded_file = st.sidebar.file_uploader("Choose a PDB file", type=['pdb'])

st.markdown(
    r"""
    <style>
    .stDeployButton {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stMultiSelect.clearable div[role="option"]:first-child,
    .stMultiSelect.clearable div[role="option"]:last-child {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if uploaded_file is not None:
    # Read the contents of the uploaded PDB file
    pdb_string = uploaded_file.read().decode('utf-8')

    # Display the raw text of the PDB file
    st.subheader('PDB File Contents')
    st.code(pdb_string)
