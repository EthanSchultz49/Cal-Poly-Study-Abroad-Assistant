# Cal Poly Study Abroad Assistant 🌍✈️

This app is an interactive AI-powered assistant designed to help students explore Cal Poly’s study abroad programs more efficiently. By leveraging a custom knowledge base and retrieval-augmented generation (RAG), it answers student questions about different programs based on their major and selected interest.

## 💡 What It Does

- Students enter their **major** to filter programs most relevant to them.
- They can **select a specific program** from a dropdown menu.
- The assistant answers natural language questions based on the selected program.
- The student then has access to the answer of their question and a link to that programs page on Cal Poly's Website

Example questions:
- "What is the minimum GPA for this program?"
- "Are there any internship opportunities?"
- "How much does it cost?"
- "What us the location like"

## 🚀 How to Use

1. **Set Up Your Environment**
   - Clone the repo
   - Create a `.env` file and set your AWS credentials locally to access the Bedrock LLM API.

2. **Run the App**
   ```bash
   streamlit run app.py
   ```

3. **Interact With the App**
   - Enter your **major**
   - Choose a **study abroad program**
   - Ask your questions in the chat box

4. **Note:** AWS credentials are not provided in this repo. You must configure your own access to the Bedrock LLM in order to use the app.

## 🧠 Tech Stack

- **Streamlit** for front-end UI
- **LangChain** for RAG pipeline
- **AWS Bedrock** for LLM inference
- **Custom CSV knowledge base**

## 🔐 Credentials & Security

To run the app, you must:
- Create an `.env` file in the project root
- Add the following variables:
  ```
  AWS_ACCESS_KEY_ID=your_access_key
  AWS_SECRET_ACCESS_KEY=your_secret_key
  AWS_REGION=us-west-2
  ```
## 🎥 Demo Video

[![Watch the demo](https://youtu.be/98NF0skjAD8)
