import streamlit as st
from difflib import SequenceMatcher

st.set_page_config(
    page_title='ProteinVista', 
    page_icon="🧬", 
    layout='wide', 
    initial_sidebar_state='auto'
)

# CSS to hide the Deploy button
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

# CSS to remove first and last options from the multi-select widget
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


def compare_pdb_files(file1, file2):
    content1 = file1.read()
    content2 = file2.read()

    lines1 = content1.decode("utf-8").split('\n')
    lines2 = content2.decode("utf-8").split('\n')

    # Calculate the similarity using the Ratcliff/Obershelp algorithm
    matcher = SequenceMatcher(None, lines1, lines2)
    similarity_ratio = matcher.ratio()
    similarity_percent = similarity_ratio * 100

    # Generate a list of differences
    differences = list(matcher.get_opcodes())

    return similarity_percent, differences

def main():
    st.title("PDB File Comparator")

    st.sidebar.title("Upload PDB Files")
    uploaded_file1 = st.sidebar.file_uploader("Upload PDB File 1", type="pdb")
    uploaded_file2 = st.sidebar.file_uploader("Upload PDB File 2", type="pdb")

    if uploaded_file1 and uploaded_file2:
        st.subheader("Uploaded PDB Files")
        st.write("PDB File 1:", uploaded_file1.name)
        st.write("PDB File 2:", uploaded_file2.name)

        similarity_percent, differences = compare_pdb_files(uploaded_file1, uploaded_file2)
        
        st.subheader("Similarity Percentage")
        st.write(f"The files match {similarity_percent:.2f}%")

        if differences:
            st.subheader("Differences Found")
            st.write("Index", "Operation", "File 1", "File 2")
            lines1 = uploaded_file1.getvalue().decode("utf-8").split('\n')
            lines2 = uploaded_file2.getvalue().decode("utf-8").split('\n')
            for diff in differences:
                operation, start1, end1, start2, end2 = diff
                if operation != 'equal':
                    st.write(start1, operation, lines1[start1:end1], lines2[start2:end2])

        else:
            st.subheader("No Differences Found")

if __name__ == "__main__":
    main()
