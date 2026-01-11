import fitz
import re
import math
import random
import spacy
import numpy as np
from collections import Counter
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    truncation=True
)

question_generator = pipeline(
    "text2text-generation",
    model="valhalla/t5-base-qg-hl",
    truncation=True
)

# ================== PDF PROCESSING ==================

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    pages = [page.get_text() for page in doc]
    return "\n".join(pages)


def clean_text(text):
    text = re.sub(r"Page\s*\d+", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\[[0-9]+\]", "", text)
    return text.strip()

# ================== LINGUISTIC PREPROCESSING ==================

def preprocess_sentences(text):
    doc = nlp(text)
    sentences = []
    for sent in doc.sents:
        tokens = [
            token.lemma_.lower()
            for token in sent
            if not token.is_stop and not token.is_punct
        ]
        sentences.append({
            "text": sent.text,
            "tokens": tokens,
            "entities": [ent.text for ent in sent.ents]
        })
    return sentences

# ================== SENTENCE SCORING ==================

def score_sentences(sentences):
    texts = [" ".join(s["tokens"]) for s in sentences]

    if not texts:
        return []

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(texts)

    centroid = np.asarray(tfidf_matrix.mean(axis=0))
    similarities = cosine_similarity(tfidf_matrix, centroid)

    scored = []
    total = len(sentences)

    for i, s in enumerate(sentences):
        position_score = 1 - (i / total)
        entity_score = len(s["entities"]) / 5
        tfidf_score = similarities[i][0]

        final_score = (
            0.6 * tfidf_score +
            0.2 * position_score +
            0.2 * entity_score
        )

        scored.append((final_score, s["text"]))

    scored.sort(reverse=True, key=lambda x: x[0])
    return scored


# ================== SUMMARIZATION ==================

def abstractive_summary(text):
    sentences = preprocess_sentences(text)
    ranked = score_sentences(sentences)

    extractive_text = " ".join([s[1] for s in ranked[:12]])

    chunks = []
    current = ""
    for sentence in extractive_text.split(". "):
        if len(current) + len(sentence) < 500:
            current += sentence + ". "
        else:
            chunks.append(current)
            current = sentence + ". "
    if current:
        chunks.append(current)

    summaries = []
    for chunk in chunks:
        result = summarizer(
            chunk,
            max_length=200,
            min_length=100,
            do_sample=False
        )[0]["summary_text"]
        summaries.append(result)

    final_summary = summarizer(
        " ".join(summaries),
        max_length=160,
        min_length=80,
        do_sample=False
    )[0]["summary_text"]

    return final_summary

# ================== CONCEPT EXTRACTION ==================

def extract_key_concepts(text, limit=20):
    doc = nlp(text)
    concepts = []

    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) <= 4:
            concepts.append(chunk.text.lower())

    for ent in doc.ents:
        concepts.append(ent.text.lower())

    return [c for c, _ in Counter(concepts).most_common(limit)]

# ================== MCQ GENERATION ==================

def generate_mcqs(text, num_questions=5):
    doc = nlp(text)
    entity_pool = {}

    for ent in doc.ents:
        entity_pool.setdefault(ent.label_, set()).add(ent.text)

    questions = []

    for sent in doc.sents:
        if not sent.ents:
            continue

        answer = sent.ents[0].text
        label = sent.ents[0].label_

        distractors = list(entity_pool.get(label, []))
        distractors = [d for d in distractors if d != answer]
        random.shuffle(distractors)
        distractors = distractors[:3]

        while len(distractors) < 3:
            distractors.append("None of the above")

        options = distractors + [answer]
        random.shuffle(options)

        questions.append({
            "question": sent.text.replace(answer, "_____"),
            "options": options,
            "answer": answer
        })

        if len(questions) == num_questions:
            break

    return questions

# ================== FLASHCARDS ==================

def generate_flashcards(text, limit=5):
    concepts = extract_key_concepts(text, limit)
    flashcards = []

    for concept in concepts:
        flashcards.append({
            "question": f"What is {concept}?",
            "answer": concept
        })

    return flashcards

# ================== PIPELINE ENTRY ==================

def process_pdf_file(path):
    raw_text = extract_text_from_pdf(path)
    cleaned = clean_text(raw_text)

    return {
        "summary": abstractive_summary(cleaned),
        "mcqs": generate_mcqs(cleaned),
        "flashcards": generate_flashcards(cleaned)
    }
