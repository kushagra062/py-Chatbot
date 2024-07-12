import nltk
import json
import random
from fuzzywuzzy import fuzz

# Load chat patterns from the JSON file
def load_chat_patterns(json_filepath):
    try:
        with open(json_filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data['patterns']           
    except FileNotFoundError:
        print(f"The file {json_filepath} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {json_filepath}")
        return []

# Specify the path to your JSON file
json_filepath = 'chat_patterns.json'
patterns = load_chat_patterns(json_filepath)

# Convert patterns to a dictionary for fuzzy matching
qa_pairs = {pattern['pattern']: pattern['responses'] for pattern in patterns}

def fuzzy_match(user_input, qa_pairs):
    max_similarity = 0
    best_matches = []

    for pattern, _ in qa_pairs.items():
        similarity = fuzz.partial_ratio(user_input.lower(), pattern.lower())
        if similarity > max_similarity:
            max_similarity = similarity
            best_matches = [pattern]
        elif similarity == max_similarity:
            best_matches.append(pattern)

    if max_similarity >= 75:
        return random.choice(best_matches) if len(best_matches) == 1 else best_matches
    else:
        return None

def find_matching_pattern(user_input):
    for pattern in patterns:
        if nltk.re.search(pattern['pattern'], user_input.lower()):
            return random.choice(pattern['responses'])
    match = fuzzy_match(user_input, qa_pairs)
    if len(match) >=2:
        return [pattern['pattern'] for pattern in patterns if pattern['pattern'] in match]
    elif len(match) == 1:
        return [pattern['responses'] for pattern in patterns if pattern['pattern'] in match][0]
    else:
        return "I'm sorry, I don't understand that."

# Function to converse with the chatbot
def converse():
    print("Welcome to the chatbot! Type 'quit' to end the conversation.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            print("It was nice talking to you! Have a great day!")
            break
        response = find_matching_pattern(user_input)
        if isinstance(response, list):
            for option in response:
                print("ChatBot:", option)
        else:
            print("ChatBot:", response)

# Start the conversation
converse()