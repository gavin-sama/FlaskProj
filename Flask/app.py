from flask import Flask, render_template, request
from APIservice import main as get_weather

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    data = None
    if request.method == 'POST':
        name = request.form['name']
        data = get_weather(name)
    return render_template('index.html', data=data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
