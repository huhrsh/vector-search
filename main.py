import time
start_time=time.time()
from mongo_utils import search_doctors
from textual_response import object_to_textual_response

end_time = time.time()
print(f"Time taken to ask for input: {end_time - start_time} seconds")
query_sentence = input("Enter user prompt: ")
start_time=time.time()
# query_vector = get_vector(query_sentence)

results = search_doctors(query_sentence,7)

if results:
    print("Data received: ")
    for result in results:
        print(result,f"Score: {result['score']}" '\n')
    response = object_to_textual_response(query_sentence, results[0])
    # print("Search Results:")
    print(response)
    # for result in results:
    #     text_response = object_to_textual_response(query_sentence,result)
    #     print(text_response)
else:
    print("No results found.")
    
end_time = time.time()
print(f"Total execution time: {end_time - start_time} seconds")
