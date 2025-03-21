import requests

# Define the prompt to be sent
prompt = """
I need a detailed explanation on review món ăn. Please include:

Overview: Define and explain the significance of the topic
Key Points: List and explain essential factors or components of the topic
Examples: Provide examples or case studies related to the topic
Challenges: Discuss common challenges or misconceptions.
Best Practices: Outline effective strategies or tips.
Trends: Identify current trends or future directions.
Resources: Suggest additional resources for further learning.
Ensure the information is clear and concise.

Please give the answer in Vietnamese.
"""

# Enter E-mail to generate API
api_key = '210167a306e2affee74535654c4b8ed5'

# Define the default model if none is specified
default_model = 'gpt-3.5-turbo'

# Uncomment the model you want to use, and comment out the others
# model = 'gpt-4'
# model = 'gpt-4-32k'
# model = 'gpt-3.5-turbo-0125'
model = default_model

# Build the URL to call
api_url = f'http://195.179.229.119/gpt/api.php?prompt={requests.utils.quote(prompt)}&api_key={requests.utils.quote(api_key)}&model={requests.utils.quote(model)}'

try:
    # Execute the HTTP request
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an error for bad HTTP status codes

    # Parse and print the response
    data = response.json()
    print(data)

except requests.RequestException as e:
    # Print any errors
    print(f'Request Error: {e}')
