import os
from dotenv import load_dotenv
from pymongo import MongoClient
from vectorizer import get_vector
from extractor import extract_keywords

load_dotenv()

# MongoDB connection string
MONGODB_URI = os.getenv("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client['vector_search_db']
collection = db['doctors']

def insert_vector(document, vector):
    document['vector'] = vector.tolist()  # Convert numpy array to list for JSON serialization
    collection.insert_one(document)

def search_doctors(query, top_n=5, num_candidates=100):
    filter_by, sort_by = extract_keywords(query)
    query_vector = get_vector(query).tolist()

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
    if filter_by:
        pipeline.append({"$match": filter_by})
    
    # Project the necessary fields
    pipeline.append({
        "$project": {
            "_id": 0,
            "vector": 0
        }
    })
    
    # Add sorting if provided
    if sort_by:
        pipeline.append({"$sort": sort_by})

    query_results = collection.aggregate(pipeline)

    results = []
    for result in query_results:
        results.append(result)

    return results
