import pandas as pd
import ast
import streamlit as st
from config import CSV_PATH

class DataLoader:
    def init(self):
        self.programs_df = None
        self.all_majors = None

    @st.cache_data
    def load_programs(_self):
        """Load programs dataframe from CSV"""
        programs_df = pd.read_csv(CSV_PATH)
        programs_df['embedding'] = programs_df['embedding'].apply(ast.literal_eval)
        return programs_df

    @st.cache_data
    def get_unique_majors(_self, programs_df):
        """Extract unique majors from programs dataframe"""
        program_majors = programs_df['areas_of_study'].dropna().astype(str).str.split(',|\n|;')
        all_majors = [m.strip() for sublist in program_majors for m in sublist if m.strip()]
        return sorted(set(all_majors))

    def initialize(self):
        """Initialize and return programs dataframe and majors list"""
        self.programs_df = self.load_programs()
        self.all_majors = self.get_unique_majors(self.programs_df)
        return self.programs_df, self.all_majors