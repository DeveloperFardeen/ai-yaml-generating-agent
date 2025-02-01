# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

def init_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def prompt_to_yaml(model, prompt):
    system_prompt = """
    Convert the following requirements into a valid YAML configuration file.
    Follow these rules:
    1. Use proper YAML syntax and indentation
    2. Group related configurations
    3. Use appropriate data types (strings, numbers, boolean, lists)
    4. Add comments for clarity
    Return only the YAML content without any additional text.
    """
    
    response = model.generate_content(f"{system_prompt}\n\nRequirements:\n{prompt}")
    return response.text

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    api_key = data.get('api_key')
    prompt = data.get('prompt')
    
    if not api_key or not prompt:
        return "API Key and prompt are required", 400
    
    try:
        model = init_gemini(api_key)
        yaml_config = prompt_to_yaml(model, prompt)
        return yaml_config
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)