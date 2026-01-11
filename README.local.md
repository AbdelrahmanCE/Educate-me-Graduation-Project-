# Educate-me-Graduation-Project-
Educate Me is a full-stack web application that transforms PDF documents into interactive study materials. Users can upload academic PDFs and instantly receive an AI-generated summary, solvable multiple-choice questions, and flashcards using modern NLP pipeline techniques.

The system extracts text from PDFs, preprocesses it using NLP techniques, generates an abstractive summary, creates solvable MCQs, and produces flashcards for memorization.

The backend is implemented using Flask with JWT-based authentication and SQLAlchemy ORM, while the frontend is built with React. The NLP pipeline integrates PyMuPDF, spaCy, BART, and T5 models to generate meaningful educational outputs.



🚀 Features:

1- Upload academic PDF files

2- AI-generated abstractive summaries

3- Interactive MCQs (answers hidden until solved)

4- Automatically generated flashcards

5- Modular and scalable NLP pipeline

6- Modern React-based frontend


🛠 Tech Stack:

*Frontend*

React.js, React Router, Fetch API, CSS (custom global styling)

*Backend*

Python, Flask, Flask-JWT-Extended, Flask-CORS, SQLAlchemy ORM

*NLP & AI*

PyMuPDF for PDF text extraction, spaCy for text preprocessing and NER, BART (facebook/bart-large-cnn) for summarization, T5 (valhalla/t5-base-qg-hl) for flashcard question generation, Rule-based MCQ generation using spaCy NER

*Database*

SQLAlchemy ORM, SQLite (default) or MySQL-compatible configuration
