from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os

app = Flask(__name__, static_folder='static')

# Configure Gemini API
api_key = os.environ.get('GEMINI_API_KEY', 'AIzaSyDeHPwENAx3vZwFop1wLn3vYIpmKLxvuEc')
genai.configure(api_key=api_key)

# Initialize model
model = genai.GenerativeModel('gemini-3-pro-preview')

SYSTEM_PROMPT = """You are a versatile, friendly, and intelligent AI assistant. 

Guidelines:
1. Respond in the SAME LANGUAGE the user uses (Vietnamese → Vietnamese, English → English, etc.)
2. For code questions: Provide code in proper blocks with language tags (```python, ```javascript) and explanations
3. For general questions: Be natural, concise, and helpful
4. For creative requests: Make them engaging and imaginative
5. Maintain conversation context - refer to previous messages when relevant
6. Always be positive, safe, and encourage interaction
7. Think step-by-step for complex problems

Created by Gia Khải"""

@app.route('/')
def serve_index():
    """Serve the main HTML page"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request'}), 400
        
        user_message = data.get('message', '').strip()
        conversation_history = data.get('history', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Build full context
        full_prompt = SYSTEM_PROMPT
        if conversation_history:
            full_prompt += f"\n\n--- Conversation History ---\n{conversation_history}\n"
        full_prompt += f"\n--- Current User Request ---\n{user_message}"
        
        # Generate response
        response = model.generate_content(
            full_prompt,
            generation_config={
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
        )
        
        ai_reply = response.text
        return jsonify({'reply': ai_reply})
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Log error
        return jsonify({'error': f'Failed to process request: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Assistant...")
    print("📡 Server running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
