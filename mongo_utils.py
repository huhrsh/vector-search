import os
from dotenv import load_dotenv
from pymongo import MongoClient
from vectorizer import get_vector
from extractor import extract_keywords
from filters import get_numerical_filters


load_dotenv()

# MongoDB connection string
MONGODB_URI = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client['vector_search_db']
collection = db['doctors']

def insert_vector(document, vector):
    document['vector'] = vector.tolist()  
    collection.insert_one(document)
    
def search_doctors_by_api(query, filters, top_n=1, num_candidates=100):
    # filter_by, sort_by = extract_keywords(query)
    query_vector = get_vector(query).tolist()

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index", 
                "path": "vector",
                "queryVector": query_vector,
                "numCandidates": num_candidates,
                "limit": top_n
            }
        },
        {
            "$addFields": {
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    
    # Add filters if provided
    if filters:
        pipeline.append({"$match": filters})
    
    # Project the necessary fields
    pipeline.append({
        "$project": {
            "_id": 0,
            "vector": 0
        }
    })
    
    query_results = collection.aggregate(pipeline)

    results = []
    for result in query_results:
        results.append(result)

    return results


def search_doctors(query, top_n=5, num_candidates=100):
    # filter_by, sort_by = extract_keywords(query)
    query_vector = get_vector(query).tolist()
    filters=get_numerical_filters()

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",  # Specify the name of the vector search index
                "path": "vector",
                "queryVector": query_vector,
                "numCandidates": num_candidates,
                "limit": top_n
            }
        },
        {
            "$addFields": {
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    
    # Add filters if provided
    if filters:
        pipeline.append({"$match": filters})
    
    # Project the necessary fields
    pipeline.append({
        "$project": {
            "_id": 0,
            "vector": 0
        }
    })

    query_results = collection.aggregate(pipeline)

    results = []
    for result in query_results:
        results.append(result)

    return results
