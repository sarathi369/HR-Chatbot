# HR Chatbot – RAG-Based AI Assistant

## Project Overview

The HR Chatbot is an AI-powered assistant designed to answer employee queries using the HR documents provided as its knowledge base.

It uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from HR documents and generate context-based responses using Google's Gemini model.

The chatbot aims to provide employees with quick answers to common HR-related questions while avoiding unsupported information.

## Features

- Answers employee queries using supplied HR documents.
- Retrieves relevant document chunks using semantic search.
- Generates context-aware responses using Gemini.
- Identifies questions that are not covered by the available documents.
- Provides source-document references in responses.
- Logs user questions, retrieved content and generated answers.
- Includes an evaluation system with 10 test questions.
- Provides an interactive interface using Streamlit.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Streamlit | User interface |
| Google Gemini API | AI response generation |
| Sentence Transformers | Text embeddings |
| ChromaDB | Vector database |
| python-docx | DOCX document processing |
| PyMuPDF | PDF processing support |
| JSON | Document data and evaluation questions |

## HR Documents Used

The chatbot's knowledge base contains four supplied HR documents:

1. Claims User Manual
2. Regularisation User Manual
3. Timecard User Manual
4. Five-Day Work Week Policy – Effective 15 July 2026

The chatbot is designed to answer using these documents. If information is unavailable, it informs the user rather than inventing a policy.

## System Architecture

The chatbot follows a Retrieval-Augmented Generation workflow:

1. **Document Loading:** Extracts text from the supplied HR documents.
2. **Text Splitting:** Divides the extracted content into smaller chunks while preserving paragraph context.
3. **Embedding Generation:** Uses Sentence Transformers (`all-MiniLM-L6-v2`) to convert text chunks into numerical embeddings.
4. **Vector Storage:** Stores the embeddings in ChromaDB.
5. **Retrieval:** Converts the user's question into an embedding and retrieves the five most relevant document chunks.
6. **Response Generation:** Passes the retrieved context and user question to Gemini to generate an answer.
7. **Logging:** Records the question, retrieved content and generated response.

## Project Structure

```text
HR-Chatbot/
│
├── documents/                  # Original HR documents
├── processed_documents/        # Extracted document data
├── vector_store/               # Local ChromaDB storage
├── logs/                       # Chatbot interaction logs
│
├── src/
│   ├── document_loader.py      # Document extraction
│   ├── text_splitter.py        # Text chunking
│   ├── embeddings.py           # Embedding generation
│   ├── vector_store.py         # ChromaDB storage
│   ├── retriever.py            # Relevant chunk retrieval
│   ├── rag_pipeline.py         # RAG response generation
│   └── logger.py               # Interaction logging
│
├── evaluation/
│   ├── test_questions.json     # Evaluation dataset
│   ├── evaluate.py             # Evaluation script
│   └── report.txt              # Evaluation results
│
├── app.py                      # Streamlit application
├── requirements.txt
├── .env                        # API key configuration
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sarathi369/HR-Chatbot.git
cd HR-Chatbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace the placeholder with your own Gemini API key.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## Evaluation

The chatbot was evaluated using 10 predefined questions covering:

- Timecard management
- Working-hour limits
- Attendance regularisation
- Five-day work week eligibility
- Policy effective date
- Loss of Pay (LOP)
- Claims submission
- Missing timecard tasks
- Unsupported HR policy questions

**Automated Evaluation Results**

| Metric | Result |
|---|---:|
| Total questions | 10 |
| Correct by automated keyword matching | 9 |
| Flagged for manual review | 1 |
| Automated accuracy | 90% |

**Manual Review:** The tenth response, concerning maternity leave, correctly stated that the policy was not available in the supplied documents and advised the employee to contact HR or BU HR. It was flagged by the keyword-based evaluation method despite being semantically correct.

Evaluation report: `evaluation/report.txt`

## Limitations

- The chatbot can only answer questions supported by its available HR documents.
- It does not replace official HR guidance.
- Response quality depends on document coverage and retrieval relevance.
- The current automated evaluation uses keyword matching and requires manual review.

## GitHub Repository

https://github.com/sarathi369/HR-Chatbot

## Future Improvements

- Improve evaluation using semantic similarity and required-answer criteria.
- Expand the knowledge base with additional approved HR policies.
- Improve retrieval accuracy and response relevance.
- Enhance the user interface and conversation experience.