# RAG with LangChain & Gemini (Streamlit)

A Retrieval-Augmented Generation (RAG) knowledge assistant using Google Gemini and LangChain, with a Streamlit UI. Upload your PDF, TXT, or DOCX files and ask questions to get context-aware answers with source references.

## Features

- Upload PDF, TXT, or DOCX files
- Automatic text chunking and embedding
- FAISS vector store for fast retrieval
- Google Gemini (via LangChain) for answering questions
- Source document metadata display

## Quickstart

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd RAG-App-With-LangChain
```

### 2. Set up environment

```bash
python -m venv env
./env/Scripts/activate  # On Windows
# Or
source env/bin/activate  # On Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_google_api_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

### 6. Usage

- Upload a PDF, TXT, or DOCX file
- Ask questions in the input box
- View answers and source metadata

## Deployment on Streamlit Cloud

You can deploy this app for free on [Streamlit Cloud](https://streamlit.io/cloud):

1. Push your code to a public GitHub repository.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and connect your GitHub account.
3. Click "New app" and select your repo and `app.py` as the entry point.
4. Add your API key in the Streamlit Cloud secrets:
   - Go to "App settings" > "Secrets" and add:
     ```toml
     GOOGLE_API_KEY = "your_google_api_key_here"
     ```
   - Or, edit `.streamlit/secrets.toml` locally and push (for local testing only).
5. Click "Deploy".

**Note:** On Streamlit Cloud, environment variables from `.env` are not used. Use `secrets.toml` as shown above.

## Project Structure

```
RAG-App-With-LangChain/
├── app.py
├── requirements.txt
├── .env.example
├── .streamlit/
│   └── secrets.toml
├── README.md
├── env/ (virtual environment)
```

## License

MIT
