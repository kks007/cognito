# File: my_assistant/document_summarization/summarizer.py
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize

# Download NLTK data (run this once)
nltk.download('stopwords')
nltk.download('punkt')

def calculate_word_frequencies(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    fdist = FreqDist(filtered_words)
    return fdist

def summarize_text(text, num_sentences=None, summary_length=None):
    if num_sentences and summary_length:
        raise ValueError("Please provide either --num-sentences or --summary-length, not both.")

    sentences = sent_tokenize(text)
    word_frequencies = calculate_word_frequencies(text)
    sentence_scores = {sentence: sum(word_frequencies[word] for word in word_tokenize(sentence.lower()) if word.isalnum()) for sentence in sentences}

    if num_sentences:
        sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    else:
        sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

        word_count = 0
        summary = []
        for sentence in sorted_sentences:
            summary.append(sentence)
            word_count += len(word_tokenize(sentence))
            if summary_length and word_count >= summary_length:
                break

        return " ".join(summary)

    return " ".join(sorted_sentences)
