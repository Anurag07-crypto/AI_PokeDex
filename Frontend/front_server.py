from pathlib import Path
import sys
from PIL import Image
import requests
from typing import Optional
from langchain_groq import ChatGroq
import os  
from dotenv import load_dotenv


load_dotenv()
os.getenv("GROQ_API_KEY")

rewrite_llm = ChatGroq(model="llama-3.1-8b-instant")

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from Work_dir.Cnn_model import Predict
import streamlit as st

# ===== BACKEND CONFIGURATION =====
BACKEND_URL = "http://127.0.0.1:8000"

# ===== HELPER FUNCTIONS =====
def get_pokemon_info(pokemon_name: str) -> Optional[str]:
    """
    Fetch Pokemon information from backend API
    
    Args:
        pokemon_name: Name of the Pokemon
        
    Returns:
        Pokemon information or None if request fails
    """
    try:
        response = requests.post(
            f"{BACKEND_URL}/get_info",
            json={"query": pokemon_name},
            timeout=25
        )
        response.raise_for_status()
        return response.json().get("response")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Backend connection failed: {str(e)}")
        return None

# ===== STREAMLIT UI =====
st.title("🔥 Pokémon Identifier")
st.markdown("Upload a Pokémon image to identify and learn more about it!")

with st.form(key="pokemon_search_form"):
    uploaded_image = st.file_uploader(
        "Upload your Pokemon", 
        type=["png", "jpeg", "jpg"],
        help="Upload a clear image of a Pokemon"
    )
    submitted = st.form_submit_button("🔍 Identify Pokemon")
 
if submitted: 
    if uploaded_image is not None:
        # Show loading spinner
        with st.spinner("🔮 Analyzing Pokemon..."):
            try:
                # Step 1: Predict Pokemon from image
                label, confidence_score = Predict(uploaded_image)
                
                # Step 2: Display prediction results
                col_1, col_2 = st.columns(2)
                
                with col_1: 
                    st.markdown("---")
                    st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
                    st.progress(confidence_score / 100)
                    st.write(f"**Confidence:** {confidence_score:.2f}%")
                    st.header(label.capitalize())
                    st.markdown("---")
                    
                with col_2:
                    # Step 3: Fetch additional info from backend
                    st.markdown("---")
                     
                    with st.spinner(f"Fetching details about {label}..."):
                        pokemon_info = get_pokemon_info(label)
                        
                        rewrite_prompt = f""" 
    You have just only Write this things in more representative form
    in Markdown format
    here is the context:
    {pokemon_info}
    constraints
    -make sure give me only one str output 
    -No extra messages only just do what i told above
    """

                        response = rewrite_llm.invoke(rewrite_prompt)
                        
                        if pokemon_info:
                            st.markdown(response.content)
                            st.markdown("---")
                            
                        else:
                            st.warning("⚠️ Could not fetch additional information. Backend might be offline.")
                            st.markdown("---")
                    
                    # Footer
                    st.markdown("---")
                    st.caption("✨ Created by Anurag")

            except Exception as e:
                st.error(f"❌ Prediction failed: {str(e)}")
                st.info("💡 Please try uploading a different image")
                
    else:
        st.warning("⚠️ Please upload an image to continue")