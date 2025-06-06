class SearchEngine:
    def __init__(self, aws_client, link_lookup):
        self.aws_client = aws_client
        self.link_lookup = link_lookup  # new: dict[filename] -> link

    def search_programs(self, query, filtered_programs_df, program_name=""):
        """Search program descriptions and generate LLM response"""
        if filtered_programs_df.empty:
            return "No matching program found."

        try:
            context = ""
            for _, row in filtered_programs_df.iterrows():
                context += f"{row['filename']}\n{row['content']}\n\n"

            response = self.aws_client.generate_answer(context, query, program_name)

            # Add program link at the bottom, if found
            link = self.link_lookup.get(program_name.strip())
            if link:
                response += f"\n\n📎 [**Click here to view the program on Cal Poly's Website**]({link})"

            return response

        except Exception as e:
            return f"Error searching programs: {str(e)}"
