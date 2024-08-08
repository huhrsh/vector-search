from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from vectorizer import get_vector
from mongo_utils import insert_vector, search_doctors_by_api
from textual_response import object_to_textual_response_for_api

app = FastAPI()

class Doctor(BaseModel):
    doctor_name: str
    specialization: str
    availability: List[str]
    price:int
    rating:float
    location: str
    experience:int
    contact_info: str
    description: str

class SearchQuery(BaseModel):
    query: str
    number_of_results: Optional[int]=1
    min_price: Optional[float] = -1
    max_price: Optional[float] = -1
    min_rating: Optional[float] = -1
    max_rating: Optional[float] = -1
    min_experience: Optional[float] = -1
    max_experience: Optional[float] = -1

@app.post("/add-doctor/")
def add_doctor(doctor: Doctor):
    combined_text = combine_doctor_fields(doctor.model_dump())
    vector = get_vector(combined_text)
    insert_vector(doctor.model_dump(), vector)
    return {"message": "Doctor added successfully"}

@app.post("/search-doctors/")
def search_doctors_endpoint(query: SearchQuery):
    filters = {}

    # Process price filter
    if query.min_price != -1 or query.max_price != -1:
        price_filter = {}
        if query.min_price != -1:
            price_filter['$gte'] = query.min_price
        if query.max_price != -1:
            price_filter['$lte'] = query.max_price
        filters['price'] = price_filter

    # Process rating filter
    if query.min_rating != -1 or query.max_rating != -1:
        rating_filter = {}
        if query.min_rating != -1:
            rating_filter['$gte'] = query.min_rating
        if query.max_rating != -1:
            rating_filter['$lte'] = query.max_rating
        filters['rating'] = rating_filter

    # Process experience filter
    if query.min_experience != -1 or query.max_experience != -1:
        experience_filter = {}
        if query.min_experience != -1:
            experience_filter['$gte'] = query.min_experience
        if query.max_experience != -1:
            experience_filter['$lte'] = query.max_experience
        filters['experience'] = experience_filter

    # Perform the search with the filters
    results = search_doctors_by_api(query.query, filters, query.number_of_results)
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    
    response = object_to_textual_response_for_api(query.query, results[0:query.number_of_results])
    # return {"textual response": response}
    return {"textual response": response, "all_results": results}

def combine_doctor_fields(doctor):
    combined_text = (
        f"Doctor {doctor['doctor_name']} specializes in {doctor['specialization']}. "
        f"They are available on {', '.join(doctor['availability'])}. "
        f"They are located in {doctor['location']}. "
        f"Contact them at {doctor['contact_info']}. "
        f"They can be described as {doctor['description']}"
    )
    return combined_text
