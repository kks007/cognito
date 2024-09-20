import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from gensim.corpora import Dictionary
from gensim.models import LdaModel

# Ensure the necessary NLTK resources are downloaded once (you can run these once in a separate setup script)
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

def calculate_word_frequencies(text):
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text.lower())
    filtered_words = [lemmatizer.lemmatize(word) for word in words if word.isalnum() and word not in stop_words]
    fdist = FreqDist(filtered_words)
    return fdist

def apply_lda(text, lda_model=None):
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in word_tokenize(text.lower()) if word.isalnum() and word not in stop_words]
    dictionary = Dictionary([words])
    corpus = [dictionary.doc2bow(text) for text in [words]]
    if lda_model is None:
        lda_model = LdaModel(corpus, num_topics=10, id2word=dictionary, passes=2)
    topics = lda_model.get_document_topics(corpus[0])
    return sum([weight for id, weight in topics])

def preprocess_documents(documents):
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    return [[lemmatizer.lemmatize(word) for word in word_tokenize(doc.lower()) if word.isalnum() and word not in stop_words] for doc in documents]

def train_lda(documents, num_topics=10, passes=2):
    preprocessed_documents = preprocess_documents(documents)
    dictionary = Dictionary(preprocessed_documents)
    corpus = [dictionary.doc2bow(doc) for doc in preprocessed_documents]
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
    return lda_model

def summarize_text(text, num_sentences=None, summary_length=None, lda_model=None):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize the words and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    
    # Calculate word frequencies
    word_frequencies = {}
    for word in words:
        if word.isalnum() and word not in stop_words:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # Normalize word frequencies
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word] / max_frequency

    # Score sentences based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if len(sentence.split(' ')) < 30:  # Only consider shorter sentences
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]

    # Sort sentences by score
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    
    # Select top sentences based on user input
    if num_sentences:
        summary_sentences = sorted_sentences[:num_sentences]
    elif summary_length:
        summary_sentences = []
        word_count = 0
        for sentence in sorted_sentences:
            word_count += len(sentence.split())
            if word_count <= summary_length:
                summary_sentences.append(sentence)
            else:
                break
    else:
        num_summary_sentences = max(1, len(sentences) // 3)
        summary_sentences = sorted_sentences[:num_summary_sentences]
    
    summary = ' '.join(summary_sentences)
    return summary
