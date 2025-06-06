import streamlit as st
from data_loader import DataLoader
from aws_client import AWSClient
from search_engine import SearchEngine
import pandas as pd

st.set_page_config(page_title="Cal Poly Study Abroad Assistant", layout="wide")

# Initialize components

#
# Load program link mapping
@st.cache_data
def load_program_links():
    link_df = pd.read_csv("/Users/ethanschultz/Documents/GSB_570_GEN_AI/Code:Project/Data_current/urls.csv")
    return dict(zip(link_df['filename'].str.strip(), link_df['content'].str.strip()))

program_links = load_program_links()

#
@st.cache_resource
def initialize_app():
    """Initialize and cache app components"""
    data_loader = DataLoader()
    aws_client = AWSClient()
    program_links = load_program_links()
    search_engine = SearchEngine(aws_client, program_links)
    return data_loader, search_engine

@st.cache_data
def load_and_process_data():
    """Load and preprocess data with caching"""
    data_loader, _ = initialize_app()
    programs_df, all_majors = data_loader.initialize()
    
    # Preprocess data for faster filtering
    programs_df['areas_of_study_lower'] = programs_df['areas_of_study'].str.lower()
    
    # Create lookup dictionary for faster program filtering
    program_lookup = {}
    major_to_programs = {}
    
    for major in all_majors:
        # Handle multiple areas of study per program (comma-separated)
        major_lower = major.lower().strip()
        matching_programs = set()
        
        for idx, areas in programs_df['areas_of_study_lower'].items():
            if pd.notna(areas):
                # Split by comma and check each area
                areas_list = [area.strip() for area in str(areas).split(',')]
                if any(major_lower in area or area in major_lower for area in areas_list):
                    matching_programs.add(programs_df.loc[idx, 'filename'])
        
        program_lookup[major] = sorted(list(matching_programs))
        major_to_programs[major] = matching_programs
    
    return programs_df, all_majors, program_lookup, major_to_programs

@st.cache_data
def get_program_data(programs_df, selected_program):
    """Cache filtered program data - ensures only selected program data is returned"""
    program_data = programs_df[programs_df['filename'] == selected_program].copy()
    
    # Verify we only have the correct program
    unique_programs = program_data['filename'].unique()
    if len(unique_programs) != 1:
        st.error(f"Data integrity issue: Expected 1 program, found {len(unique_programs)}")
        return pd.DataFrame()
    
    return program_data

@st.cache_data
def prepare_search_context(program_df):
    """Prepare and cache the context data for LLM search"""
    if program_df.empty:
        return ""
    
    # Extract relevant content for the LLM (exclude embeddings for efficiency)
    context_data = program_df[['filename', 'tab_name', 'content', 'areas_of_study']].copy()
    
    # Create a structured context string if needed by your search engine
    context_summary = {
        'program_name': program_df['filename'].iloc[0],
        'areas_of_study': program_df['areas_of_study'].iloc[0],
        'total_sections': len(program_df),
        'content_sections': program_df['content'].tolist()
    }
    
    return context_data, context_summary

# Load components and data
data_loader, search_engine = initialize_app()
programs_df, all_majors, program_lookup, major_to_programs= load_and_process_data()

# === UI ===
st.title("🎓 Cal Poly Study Abroad Assistant")

with st.sidebar:
    st.header("ℹ️ How it Works")
    st.write("1. Select your major to filter relevant programs")
    st.write("2. Choose a specific program")
    st.write("3. Ask questions about that program")

st.subheader("1️⃣ Select Your Major")
selected_major = st.selectbox("Choose your area of study:", options=all_majors)

if selected_major:
    # Use precomputed program lookup for faster filtering
    available_programs = sorted(program_lookup.get(selected_major, []))
    
    if available_programs:
        st.subheader("2️⃣ Select a Study Abroad Program")
        selected_program = st.selectbox("Programs that match your major:", options=available_programs)
        
        if selected_program:
            # Get cached program data
            program_df = get_program_data(programs_df, selected_program)
            
            if program_df.empty:
                st.error("No data found for the selected program. Please try another program.")
            else:
                # Prepare search context efficiently
                context_data, context_summary = prepare_search_context(program_df)    
                
                st.subheader("3️⃣ Ask Your Question")
                query = st.text_input(
                    "What do you want to know about this program?",
                    placeholder="e.g., What are the costs? What is the location like? What should I pack for this location?",
                    key="question_input"
                )
                
                if query:
                    # Add program context to the query for better results
                    program_context_query = f"Regarding the {selected_program} study abroad program: {query.strip()}"
                    
                    with st.spinner("Generating response..."):
                        # Pass only the filtered program data to ensure LLM gets correct context
                        # Use context_data (without embeddings) for efficiency
                        answer = search_engine.search_programs(
                            program_context_query, 
                            context_data,  # Pass processed data without embeddings
                            selected_program
                        )
                        
                        st.subheader("📋 Comprehensive Answer")
                        st.write(answer)
                        
                    
    else:
        st.warning("No programs found for this major.")
else:
    st.info("👈 Start by selecting your major to see available programs.")