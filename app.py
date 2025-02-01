# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import google.generativeai as genai
import yaml
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Initialize Gemini API
def init_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def clean_yaml_block(yaml_text):
    lines = yaml_text.strip().split("\n")
    
    if lines[0].strip().startswith("```yaml"):
        lines.pop(0)  # Remove the first line
    
    if lines[-1].strip() == "```":
        lines.pop()  # Remove the last line
    
    return "\n".join(lines)

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
    try:
        # Validate that the response is valid YAML
        yaml_content = response.text
        # yaml.safe_load(yaml_content)  # This will raise an error if invalid
        return yaml_content
    except yaml.YAMLError as e:
        return f"Error: Generated invalid YAML configuration: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    api_key = 'AIzaSyD2Xw1zRSrsoDMCb7ATtjqvQDVRJMtFCF4'
    prompt = request.form.get('prompt')
    
    if not api_key or not prompt:
        return "API Key and prompt are required", 400
    
    try:
        model = init_gemini(api_key)
        yaml_config = prompt_to_yaml(model, prompt)
        yaml_config = clean_yaml_block(yaml_config)
        return render_template('index.html', yaml_config=yaml_config, prompt=prompt)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    # Ensure templates directory exists
    # Path("templates").mkdir(exist_ok=True)
    app.run()