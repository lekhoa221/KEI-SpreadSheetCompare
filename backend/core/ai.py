import ollama

def generate_analysis(changes, summary):
    """
    Send the changes summary to Ollama (Gemma 3) and get a natural language explanation.
    """
    # 1. Prepare the Prompt
    # We limit the number of detailed changes to avoid overflowing context if huge
    max_details = 50
    detailed_text = ""
    for c in changes[:max_details]:
        detailed_text += f"- At Row {c['row']+1}, Col '{c['col']}': Changed from '{c['old']}' to '{c['new']}' ({c['type']})\n"
    
    if len(changes) > max_details:
        detailed_text += f"... and {len(changes) - max_details} more changes."

    prompt = f"""
    Bạn là một Chuyên gia Phân tích Dữ liệu (Data Analyst). Tôi vừa so sánh 2 phiên bản của một file Excel.
    Dưới đây là tóm tắt các thay đổi:
    - Tổng số cột quét: {summary['total_cols']}
    - Tổng số dòng quét: {summary['total_rows']}
    - Tổng số điểm khác biệt tìm thấy: {summary['changes_count']}

    Chi tiết các thay đổi (mẫu):
    {detailed_text}

    Hãy đưa ra một bản phân tích ngắn gọn nhưng sâu sắc về những thay đổi này bằng **Tiếng Việt**.
    Yêu cầu:
    1. **Tóm tắt ngắn gọn**: Mục đích chính của lần cập nhật này là gì? (Ví dụ: cập nhật giá, sửa lỗi chính tả, thay đổi trạng thái...).
    2. **Xu hướng**: Nếu có thay đổi số liệu, hãy nhận xét xu hướng (tăng/giảm).
    3. **Định dạng**: Sử dụng **Markdown** (in đậm, gạch đầu dòng) để trình bày đẹp mắt.
    4. **Ngắn gọn**: Đi thẳng vào vấn đề, không dài dòng.
    """

    # 2. Call Ollama
    try:
        response = ollama.chat(model='gemma3:4b', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error connecting to AI: {str(e)}. Make sure Ollama is running and key is correct."
