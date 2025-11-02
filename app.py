from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os

app = Flask(__name__, static_folder='static')

genai.configure(api_key=os.environ.get('GEMINI_API_KEY', 'AIzaSyDeHPwENAx3vZwFop1wLn3vYIpmKLxvuEc'))

model = genai.GenerativeModel('gemini-2.5-flash')

GENERAL_PROMPT = """
Bạn là trợ lý AI đa năng, thân thiện và thông minh. Khi trả lời:
1. Hiểu rõ ngữ cảnh và trả lời ngắn gọn, hữu ích bằng tiếng Việt.
2. Nếu hỏi về code/lập trình, trả code trong khối ```python (hoặc ngôn ngữ khác), kèm giải thích.
3. Nếu hỏi chung (tin tức, giải trí, tư vấn), trả lời tự nhiên, thêm ví dụ nếu cần.
4. Nếu yêu cầu sáng tạo (câu chuyện, ý tưởng), làm cho hấp dẫn, sáng tạo.
5. Hỗ trợ multimodal nếu cần (mô tả ảnh, phân tích ý tưởng), và suy nghĩ từng bước nếu phức tạp.
6. Luôn tích cực, an toàn, và khuyến khích tương tác.
7. Admin Tạo Ra Là Gia Khải
"""

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({'error': 'Vui lòng nhập tin nhắn'}), 400

        response = model.generate_content(GENERAL_PROMPT + "\nYêu cầu: " + user_message)
        ai_reply = response.text
        return jsonify({'reply': ai_reply})
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
