import streamlit as st
from stmol import showmol
import py3Dmol
import requests
from Bio.PDB import PDBParser

st.set_page_config(
    page_title='ProteinVista', 
    page_icon="🧬", 
    layout='wide', 
    initial_sidebar_state='auto'
)

# Your Streamlit app code here
st.sidebar.title('ProteinVista: Structure Spin & PDB Sync')
st.sidebar.write('''With our innovative protein visualization app,
Input your structure, see it vividly unwrap,
Interact with the model, explore and spin,
Download the PDB file, where discoveries begin!''')
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

# stmol
def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb, 'pdb')
    pdbview.setStyle({'cartoon': {'color': 'spectrum'}})
    pdbview.setBackgroundColor('white')
    pdbview.zoomTo()
    pdbview.zoom(2, 800)
    pdbview.spin(True)
    showmol(pdbview, height=500, width=800)

# Protein sequence input
DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
txt = st.sidebar.text_area('Input sequence', DEFAULT_SEQ, height=275)



# ESMfold
def update(sequence=txt):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=sequence, verify=False)

    name = sequence[:3] + sequence[-3:]
    pdb_string = response.content.decode('utf-8')

    with open('predicted.pdb', 'w') as f:
        f.write(pdb_string)

    parser = PDBParser()
    struct = parser.get_structure('predicted', 'predicted.pdb')
    atoms_list = list(struct.get_atoms())
    b_value = round(sum(atom.get_bfactor() for atom in atoms_list) / len(atoms_list), 4)


    # Display protein structure
    st.subheader('Visualization of predicted protein structure')
    render_mol(pdb_string)

    # plDDT value is stored in the B-factor field
    st.subheader('plDDT')
    st.write('plDDT is a per-residue estimate of the confidence in prediction')
    st.info(f'plDDT: {b_value}')

    st.download_button(
        label="Download PDB",
        data=pdb_string,
        file_name='predicted.pdb',
        mime='text/plain',
    )

predict = st.sidebar.button('Predict', on_click=update)


if not predict:
    st.warning('Please input protein sequence data.')
