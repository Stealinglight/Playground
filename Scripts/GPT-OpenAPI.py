import requests

# Set the API endpoint
api_endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"

# Set the API key
api_key = "YOUR_API_KEY"

# Set the prompt
prompt = "What is the capital of France?"

# Set the parameters
parameters = {
  "prompt": prompt,
  "max_tokens": 50
}

# Send the request
response = requests.post(api_endpoint, json=parameters, headers={"Authorization": f"Bearer {api_key}"})

# Print the response
print(response.json())




#git clone https://github.com/openai/openai-quickstart-python.git

#cd openai-quickstart-python
#cp .env.example .env

# python -m venv venv
# . venv/bin/activate
# pip install -r requirements.txt
# flask run

# One limitation to keep in mind is that, for most models, 
# a single API request can only process up to 2,048 tokens (roughly 1,500 words) 
# between your prompt and completion.

#$ pip install openai

# import os
# import openai

# # Load your API key from an environment variable or secret management service
# openai.api_key = os.getenv("OPENAI_API_KEY")

# response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)


#$ openai api completions.create -m text-davinci-003 -p "Say this is a test" -t 0 -M 7 --stream

