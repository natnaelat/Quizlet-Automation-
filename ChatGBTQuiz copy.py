import openai
import time

# Function to read and parse the terms and definitions from the file
def read_terms_and_definitions(file_path):
    terms_definitions = {}  # Dictionary to store terms and their definitions

    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines from the file

    term = None
    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespace
        if line.startswith('-'):  # Check if the line starts with '-'
            term = line[1:].strip()  # Extract the term by removing '-'
        elif term and line:  # Check if there is a term and the line is not empty
            terms_definitions[term] = line  # Store the term and its definition
            term = None  # Reset term for the next entry

    return terms_definitions

# Function to write terms and definitions to an output file
def write_terms_and_definitions(output_file_path, terms_definitions):
    with open(output_file_path, 'w') as file:
        for term, definition in terms_definitions.items():
            file.write(f"Term: {term}\nDefinition: {definition}\n\n")

# Example usage
input_file_path = 'notes.txt'  # Replace with the path to your text file
output_file_path = 'input.txt'  # Replace with the path to your output file

terms_definitions = read_terms_and_definitions(input_file_path)
write_terms_and_definitions(output_file_path, terms_definitions)

# Set your OpenAI API key
openai.api_key = "PUT OPENAI API KEY HERE"

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def save_output_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    input_file_path = 'input.txt'  # Change this to your input file path
    output_file_path = 'output.txt'  # Change this to your output file path
    
    file_content = read_input_file(input_file_path)
    
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Can you change the terms into question formats and keep the defintions" + file_content},
            ]
        )

        response_content = completion.choices[0].message['content']
        print(response_content)
        
        # Save the response content to the output file
        save_output_file(output_file_path, response_content)

    except openai.error.RateLimitError as e:
        print("Rate limit exceeded. Please check your quota and billing details.")
        time.sleep(60)  # Wait for 60 seconds before retrying
    except openai.error.InvalidRequestError as e:
        print(f"Invalid request: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

