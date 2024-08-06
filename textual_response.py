from transformers import BartForConditionalGeneration, BartTokenizer

# Load BART model and tokenizer
model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def object_to_textual_response(query, doc):
    # Create a detailed context for each doctor
    print("Textual response: ")
    context_list = [
        f"Doctor {doc['doctor_name']} specializes in {doc['specialization']}, "
        f"has a rating of {doc['rating']}, available on {', '.join(doc['availability'])}, "
        f"charges ${doc['price']} per visit, located in {doc['location']}, "
        f"with {doc['experience']} years of experience. Contact: {doc['contact_info']}. "
        f"Description: {doc['description']}."
        # for doc in results
    ]
    context = "\n\n".join(context_list)
    
    # Create the input for the BART model with a detailed prompt
    input_text = f"Query: {query}\nContext:\n{context}\nAnswer the query based on the context provided:"
    inputs = tokenizer(input_text, return_tensors='pt', max_length=1024, truncation=True)

    # Generate response
    summary_ids = model.generate(inputs['input_ids'], max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return output
