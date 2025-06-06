import boto3
import json
import traceback
from langchain.chat_models import BedrockChat
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import AWS_REGION, BEDROCK_MODEL_ID, TITAN_MODEL_ID, MODEL_KWARGS

class AWSClient:
    def __init__(self):
        self.client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
        self.model = BedrockChat(
            client=self.client,
            model_id=BEDROCK_MODEL_ID,
            model_kwargs=MODEL_KWARGS
        )
    
    def get_titan_embedding(self, text):
        """Get embedding from Amazon Titan model"""
        response = self.client.invoke_model(
            modelId=TITAN_MODEL_ID,
            body=json.dumps({"inputText": text}),
            contentType="application/json"
        )
        result = json.loads(response['body'].read())
        return result['embedding']
    
    def generate_answer(self, data, question, program_name=""):
        """Generate LLM answer using Claude"""
        prompt_text = (
            "You are an expert Cal Poly study abroad advisor with extensive knowledge about international education. "
            "You have access to specific program information AND your general knowledge about study abroad.\n\n"
            
            "INSTRUCTIONS:\n"
            "1. ALWAYS prioritize the program-specific information provided below when answering questions about "
            "costs, courses, housing, requirements, deadlines, or other program details.\n"
            "2. SUPPLEMENT with your general knowledge about study abroad when:\n"
            "   - The program information doesn't fully answer the question\n"
            "   - The question involves general topics (things to do,visas, cultural adaptation, academic benefits, etc.)\n"
            "   - You can provide helpful context or additional guidance\n"
            "3. COMBINE both sources naturally - use program specifics as the foundation, then add general guidance.\n"
            "4. If program information is missing for a specific question, clearly state that and provide general guidance.\n"
            "5. Be conversational, encouraging, and comprehensive in your responses.\n"
            "6. Always prioritize student success, safety, and accurate information.\n\n"
            
            f"PROGRAM: {program_name}\n\n"
            "PROGRAM-SPECIFIC INFORMATION:\n{data}\n\n"
            "STUDENT QUESTION:\n{question}\n\n"
            "COMPREHENSIVE RESPONSE (using both program info and general knowledge):"
        )
        
        messages = [
            ("system", "You are a knowledgeable Cal Poly study abroad advisor who combines program-specific data with general expertise."), 
            ("human", prompt_text)
        ]
        
        try:
            prompt = ChatPromptTemplate.from_messages(messages)
            chain = prompt | self.model | StrOutputParser()
            return chain.invoke({"data": data, "question": question})
        except Exception as e:
            exc_type, exc_value, exc_traceback = traceback.sys.exc_info()
            return f"ERROR generating answer: {exc_type} {exc_value} on line {exc_traceback.tb_lineno}"