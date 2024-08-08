import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")  # Replace with a larger model for better accuracy

def extract_keywords(query):
    doc = nlp(query)

    # Extract named entities for potential filters
    entities = [(entity.text, entity.label_) for entity in doc.ents]

    # Extract keywords using spaCy's keyword extraction
    keywords = [token.text for token in doc.noun_chunks]

    print(f"keywords and entities are {keywords} and {entities}")
    # Define filter and sorting keywords
    filter_keywords = {"location": ["location", "city"],
                      "specialization": ["specialization", "field"],
                      "rating": ["rating", "stars"],
                      "price": ["price", "cost"],
                      "experience": ["experience", "years"]}
    sort_keywords = {"highest": ["highest", "best"],
                     "lowest": ["lowest", "worst"]}

    # Create filter and sort dictionaries
    filter_by = {}
    sort_by = {}

    for keyword in keywords + [entity[0] for entity in entities]:
        for filter_type, keywords_list in filter_keywords.items():
            if keyword.lower() in keywords_list:
                filter_by[filter_type] = keyword
                break
        for sort_type, keywords_list in sort_keywords.items():
            if keyword.lower() in keywords_list:
                sort_by[sort_type] = keyword

    return filter_by, sort_by
