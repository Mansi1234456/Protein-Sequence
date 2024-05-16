import streamlit as st
import webbrowser
import os

# Function to handle button click
def button_click(tool_name, file_path, html_file_path):
    if os.path.exists(file_path):
        os.system(f"streamlit run {file_path}")
    else:
        st.error(f"File {file_path} does not exist.")

    if html_file_path:
        webbrowser.open_new_tab(html_file_path)

# Main function
def main():
    st.set_page_config(
        page_title='ProteinVista', 
        page_icon="🧬", 
        layout='wide', 
        initial_sidebar_state='auto'
    )

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
        .tool-card {
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("ProteinVista")

    # Create buttons for tools
    tool_files = {
        "VISUALIZE AMINO ACIDS": (r"C:\Users\Dell\OneDrive\Desktop\MICROPRJ\ProteinVista.app.py", r"C:\Users\Dell\OneDrive\Desktop\MICROPRJ\custom_html_1.html", "This tool enables users to create vivid graphical representations of amino acids, fostering a better understanding of their molecular structures and interactions within proteins."),
        "READ PDB": (r"C:\Users\Dell\OneDrive\Desktop\MICROPRJ\StructureVis.app.py", None, "As the name suggests, this application specializes in efficiently fetching comprehensive protein data, streamlining research efforts by providing quick access to valuable information for scientific analysis and exploration."),
        "IDENTIFY LIGAND": (r"C:\Users\Dell\OneDrive\Desktop\MICROPRJ\visualizePDB.app.py", None, "Identify ligands or the binding sites and also identify their x,y,z co ordinates"),
        "COMPARE PDBs": (r"C:\Users\Dell\OneDrive\Desktop\MICROPRJ\Compare.app.py", None, "This tool facilitates the systematic comparison of Protein Data Bank (PDB) files, enabling scientists and analysts to discern structural variations and similarities between different protein structures, essential for detailed molecular analysis."),
    }

    for tool_name, (file_path, html_file_path, description) in tool_files.items():
        st.markdown("---", unsafe_allow_html=True)
        st.markdown(f"## {tool_name}", unsafe_allow_html=True)
        st.markdown(description)
        # Assign a unique key based on the tool name
        if st.button(f"🐍 {tool_name}", key=f"{tool_name}"):
            button_click(tool_name, file_path, html_file_path)

    


if __name__ == "__main__":
    main()
