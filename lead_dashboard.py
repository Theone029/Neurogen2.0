from flask import Flask, jsonify, render_template_string
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    try:
        with open('leads.json', 'r') as f:
            leads = json.load(f)
    except Exception as e:
        leads = []
    html = """
    <h1>Lead Dashboard</h1>
    <ul>
    {% for lead in leads %}
        <li>{{ lead }}</li>
    {% endfor %}
    </ul>
    """
    return render_template_string(html, leads=leads)

if __name__ == '__main__':
    app.run(port=5000)
