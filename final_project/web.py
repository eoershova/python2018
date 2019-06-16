from flask import Flask, render_template, request
import petka
app = Flask(__name__)
petka.data_base()

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        character = request.form['url']
        anec = petka.bd_parse(character)
        result = anec
        results.update({result: character})

    return render_template('index.html', errors=errors, results=results)


if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)