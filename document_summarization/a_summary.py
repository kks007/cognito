import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# # Download necessary NLTK data files (run this only once)
# nltk.download('punkt')
# nltk.download('stopwords')

def summarize_text(text, num_lines=None, num_words=None):
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
    if num_lines:
        summary_sentences = sorted_sentences[:num_lines]
    elif num_words:
        summary_sentences = []
        word_count = 0
        for sentence in sorted_sentences:
            word_count += len(sentence.split())
            if word_count <= num_words:
                summary_sentences.append(sentence)
            else:
                break
    else:
        num_summary_sentences = max(1, len(sentences) // 3)
        summary_sentences = sorted_sentences[:num_summary_sentences]
    
    summary = ' '.join(summary_sentences)
    return summary

# Example usage
text = """
Cows are fascinating and multifaceted creatures that have played a significant role in human civilization for thousands of years. Domesticated from wild aurochs around 10,000 years ago, they are now one of the most common and economically important animals worldwide. Cows belong to the species Bos taurus and are part of the Bovidae family, which also includes bison, buffalo, and goats.
One of the most notable characteristics of cows is their social nature. Cows are herd animals that thrive in the company of others. They communicate through vocalizations and body language, forming strong bonds with one another. In a herd, cows establish a social hierarchy, and their interactions can be quite complex. Research has shown that cows can recognize the faces of other cows and remember them for years, suggesting a level of social intelligence that often goes unrecognized.
Cows are primarily raised for their milk, meat, and hides. Dairy cows, specifically bred for milk production, can yield significant amounts of milk daily. This milk is processed into various dairy products, including cheese, yogurt, and butter, which are staples in many diets worldwide. Beef cattle, on the other hand, are raised for their meat, which is a major source of protein for millions of people. In addition to these products, cow hides are used to make leather, a material valued for its durability and versatility.
The environmental impact of cattle farming is a critical topic of discussion. Cattle contribute to greenhouse gas emissions, primarily methane, which is produced during digestion. Sustainable farming practices are being explored to mitigate these effects, such as rotational grazing and improving feed efficiency. Innovations in farming technology and practices aim to balance the demand for cattle products with the need to protect the environment.
Cows also have cultural significance in various societies. In Hinduism, for example, cows are considered sacred and are revered as symbols of non-violence and motherhood. This reverence shapes social practices and agricultural traditions in regions where Hinduism is predominant. In contrast, other cultures may have different relationships with cows, viewing them primarily as agricultural resources.
Moreover, cows are often seen as symbols of rural life and agricultural heritage. They play a vital role in traditional farming systems, where their manure is used as fertilizer, and they assist in plowing fields. The image of cows grazing peacefully in pastures evokes a sense of tranquility and connection to nature, making them beloved figures in rural landscapes.
In recent years, the rise of plant-based diets has led to a growing discussion about the ethical implications of livestock farming. Many advocate for more humane treatment of animals and sustainable farming practices that prioritize animal welfare. This movement has sparked innovations in alternative protein sources, including lab-grown meat and plant-based substitutes, which aim to reduce reliance on traditional cattle farming.
In summary, cows are integral to human society, serving as vital sources of nutrition, cultural symbols, and elements of agricultural ecosystems. Their complexity as social animals and their impact on the environment and economy make them a crucial subject of study in discussions about sustainable agriculture and food security. Whether viewed through the lens of farming, culture, or environmental science, cows continue to shape our world in profound ways.
"""

choice = input("Do you want to summarize by number of lines or number of words? (Enter 'lines' or 'words'): ").strip().lower()
if choice == 'lines':
    num_lines = int(input("Enter the number of lines for the summary: "))
    summary = summarize_text(text, num_lines=num_lines)
elif choice == 'words':
    num_words = int(input("Enter the number of words for the summary: "))
    summary = summarize_text(text, num_words=num_words)
else:
    summary = summarize_text(text)

print("Summary:")
print(summary)