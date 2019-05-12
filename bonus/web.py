from flask import Flask, render_template, request
import chatbot
print('Придется чуток подождать пока Маса читает книги и выписывает слова')
app = Flask(__name__)
chatbot.word_finder()


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        user_answer = request.form['url']

        sentence = chatbot.user_listener(user_answer)
        result = chatbot.answer_maker(sentence)
        print(result)
        results.update({result: user_answer})

    return render_template('index.html', errors=errors, results=results)


if __name__ == '__main__':
    app.run()