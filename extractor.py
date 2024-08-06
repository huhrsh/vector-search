from transformers import pipeline

# Load the pre-trained QA model
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def extract_keywords(query):
    context = (
        "We have doctors specializing in various fields like Dermatology, Cardiology, etc. "
        "They are located in different cities, including Los Angeles, New York, and more. "
        "Doctors have different ratings, experience, and prices for their services. "
    )

    # Extract information from the query
    location_answer = qa_pipeline(question="Where is the doctor located?", context=query)['answer']
    specialization_answer = qa_pipeline(question="What is the specialization?", context=query)['answer']
    rating_answer = qa_pipeline(question="What is the rating?", context=query)['answer']
    price_answer = qa_pipeline(question="What is the price?", context=query)['answer']
    
    # Prepare filters and sorting criteria
    filter_by = {}
    sort_by = {}
    
    if location_answer:
        filter_by['location'] = location_answer
    if specialization_answer:
        filter_by['specialization'] = specialization_answer
    if 'rating' in query.lower():
        if 'highest' in query.lower():
            sort_by['rating'] = -1
        elif 'lowest' in query.lower():
            sort_by['rating'] = 1
    if 'price' in query.lower():
        if 'lowest' in query.lower():
            sort_by['price'] = 1
        elif 'highest' in query.lower():
            sort_by['price'] = -1
    if 'experience' in query.lower():
        if 'most' in query.lower():
            sort_by['experience'] = -1
        elif 'least' in query.lower():
            sort_by['experience'] = 1
    
    return filter_by, sort_by
