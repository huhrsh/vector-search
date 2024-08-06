from vectorizer import get_vector
from mongo_utils import insert_vector

def combine_doctor_fields(doctor):
    # combined_text = (
    #     f"Doctor {doctor['doctor_name']} specializes in {doctor['specialization']}. "
    #     f"They are available on {', '.join(doctor['availability'])}. "
    #     f"They charge ${doctor['price']} per visit and are located in {doctor['location']}. "
    #     f"They have {doctor['experience']} years of experience. "
    #     f"They have a rating of {doctor['rating']} stars. Contact them at {doctor['contact_info']}. "
    #     f"They can be described as {doctor['description']}"
    # )
    combined_text = (
        f"Doctor {doctor['doctor_name']} specializes in {doctor['specialization']}. "
        f"They are available on {', '.join(doctor['availability'])}. "
        f"They are located in {doctor['location']}. "
        f"Contact them at {doctor['contact_info']}. "
        f"They can be described as {doctor['description']}"
    )
    return combined_text


doctors = [
    {
        "doctor_name": "Dr. John Smith",
        "specialization": "Cardiology",
        "availability": ["Monday 9am-11am", "Wednesday 1pm-3pm", "Friday 10am-12pm"],
        "price": 150,
        "rating": 4.5,
        "location": "New York",
        "experience": 10,
        "contact_info": "john.smith@example.com",
        "description": "Experienced cardiologist with a focus on preventive care."
    },
    {
        "doctor_name": "Dr. Emily Brown",
        "specialization": "Dermatology",
        "availability": ["Tuesday 10am-12pm", "Thursday 2pm-4pm"],
        "price": 100,
        "rating": 4.7,
        "location": "Los Angeles",
        "experience": 8,
        "contact_info": "emily.brown@example.com",
        "description": "Specialist in skin diseases and cosmetic dermatology."
    },
    {
        "doctor_name": "Dr. Sarah Lee",
        "specialization": "Pediatrics",
        "availability": ["Monday 8am-12pm", "Wednesday 9am-1pm", "Friday 11am-3pm"],
        "price": 120,
        "rating": 4.8,
        "location": "Chicago",
        "experience": 12,
        "contact_info": "sarah.lee@example.com",
        "description": "Pediatrician with extensive experience in child health and development."
    },
    {
        "doctor_name": "Dr. Michael Johnson",
        "specialization": "Orthopedics",
        "availability": ["Tuesday 9am-1pm", "Thursday 10am-2pm"],
        "price": 200,
        "rating": 4.6,
        "location": "Houston",
        "experience": 15,
        "contact_info": "michael.johnson@example.com",
        "description": "Orthopedic surgeon specializing in sports injuries and joint replacements."
    },
    {
        "doctor_name": "Dr. Olivia Martinez",
        "specialization": "Neurology",
        "availability": ["Monday 2pm-4pm", "Wednesday 10am-12pm", "Friday 1pm-3pm"],
        "price": 180,
        "rating": 4.9,
        "location": "San Francisco",
        "experience": 20,
        "contact_info": "olivia.martinez@example.com",
        "description": "Neurologist with a focus on neurodegenerative diseases and brain disorders."
    },
    {
        "doctor_name": "Dr. Daniel Kim",
        "specialization": "Gastroenterology",
        "availability": ["Tuesday 11am-2pm", "Thursday 1pm-4pm"],
        "price": 160,
        "rating": 4.7,
        "location": "Boston",
        "experience": 14,
        "contact_info": "daniel.kim@example.com",
        "description": "Expert in digestive system disorders and liver diseases."
    },
    {
        "doctor_name": "Dr. Jessica Wong",
        "specialization": "Endocrinology",
        "availability": ["Monday 10am-1pm", "Wednesday 2pm-4pm", "Friday 9am-12pm"],
        "price": 140,
        "rating": 4.8,
        "location": "Seattle",
        "experience": 9,
        "contact_info": "jessica.wong@example.com",
        "description": "Specializes in hormone-related disorders and diabetes management."
    }
]

for doctor in doctors:
    combined_text = combine_doctor_fields(doctor)
    vector = get_vector(combined_text)
    insert_vector(doctor, vector)
print("Sample data inserted successfully.")