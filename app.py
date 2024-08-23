from flask import Flask, render_template, request, jsonify
import time
import random
import os
import re
import difflib

app = Flask(__name__)

# テンプレートを格納するディレクトリ
TEMPLATE_DIR = 'html_templates'

def load_templates():
    templates = {}
    for filename in os.listdir(TEMPLATE_DIR):
        if filename.endswith('.html'):
            with open(os.path.join(TEMPLATE_DIR, filename), 'r', encoding='utf-8') as file:
                template_name = os.path.splitext(filename)[0]
                templates[template_name] = file.read()
    return templates

HTML_TEMPLATES = load_templates()

def generate_html_from_template(prompt, current_html=''):
    if current_html:
        # 既存のHTMLを改善
        improved_html, changes = improve_existing_html(current_html, prompt)
        return improved_html, changes
    else:
        # 新しいHTMLを生成
        template_name = random.choice(list(HTML_TEMPLATES.keys()))
        template_content = HTML_TEMPLATES[template_name]

        generated_html = template_content.replace('{{prompt}}', prompt)
        generated_html = re.sub(r'\{\{random_number\}\}', lambda _: str(random.randint(1, 100)), generated_html)
        generated_html = re.sub(r'\{\{random_text\}\}', lambda _: random.choice(['興味深い', '重要な', '注目すべき']), generated_html)

        return generated_html, ["新しいHTMLを生成しました。"]

def improve_existing_html(html, prompt):
    original_html = html
    changes = []

    # プロンプトに基づいて改善を行う
    if '色を変更' in prompt:
        html = html.replace('color: black;', 'color: blue;')
        changes.append("テキストの色を黒から青に変更しました。")
    elif '要素を追加' in prompt:
        html = html.replace('</body>', f'<p>{prompt}</p></body>')
        changes.append(f"新しい段落 '{prompt}' を追加しました。")
    elif 'フォントサイズ' in prompt:
        html = html.replace('font-size: 16px;', 'font-size: 18px;')
        changes.append("フォントサイズを16pxから18pxに変更しました。")
    
    # difflib を使用して変更箇所を詳細に特定
    diff = difflib.unified_diff(original_html.splitlines(), html.splitlines(), lineterm='')
    for line in diff:
        if line.startswith('+') and not line.startswith('+++'):
            changes.append(f"追加: {line[1:]}")
        elif line.startswith('-') and not line.startswith('---'):
            changes.append(f"削除: {line[1:]}")

    return html, changes

def generate_improvement_suggestion(html):
    suggestions = [
        "色をより鮮やかにしてみてはいかがでしょうか？",
        "レイアウトを調整して、より見やすくできそうです。",
        "インタラクティブな要素を追加すると、よりユーザーを引き付けられるでしょう。",
        "フォントを変更して、読みやすさを向上させることができます。",
        "画像や図を追加すると、内容がより分かりやすくなるかもしれません。"
    ]
    return random.choice(suggestions)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        conversation_history = request.form.get('conversation_history', '').split('||')
        current_html = request.form.get('current_html', '')
        
        # APIコール遅延のシミュレーション
        time.sleep(1.5)
        
        generated_html, changes = generate_html_from_template(prompt, current_html)
        improvement_suggestion = generate_improvement_suggestion(generated_html)
        
        conversation_history.append(f"Human: {prompt}")
        conversation_history.append(f"Assistant: HTMLを生成/改善しました。")
        
        return jsonify({
            'response': generated_html,
            'conversation_history': '||'.join(conversation_history),
            'message': 'HTMLを生成/改善しました。下記のプレビューをご確認ください。',
            'improvement_suggestion': improvement_suggestion,
            'changes': changes
        })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)