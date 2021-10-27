import os
from datetime import datetime

from flask import Flask, render_template, request
from gensim.models import FastText

from form_model import InputForm
from utils import find_correct_spelling, load_vocab

# create app
app = Flask(__name__)

# set url postfix
rule = '/spelling'


@app.route(rule=rule, methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        word = form.word.data.strip()
        if form.num_neighbours.data <= 0:
            message = f'Set number of neighbours to a value > 0.'
            result_str = ''
        elif form.mixed_vocab_min_freq.data < 0:
            message = f'Set minimum frequency of mixed vocab words to an integer value.'
            result_str = ''
        elif form.max_edit_distance.data < 1:
            message = f'Set max edit distance to a value >= 1.'
            result_str = ''
        else:
            out = find_correct_spelling(model=model, incorrect_word=word, num_neighbours=form.num_neighbours.data,
                                        clean_vocab_counter=clean_vocab_counter,
                                        mixed_vocab_counter=mixed_vocab_counter,
                                        mixed_vocab_min_freq=form.mixed_vocab_min_freq.data,
                                        max_edit_distance=form.max_edit_distance.data)
            message = out['message']
            result_str = f'{out["incorrect_word"]} 👉 {out["correct_word"]}' if out['correct_word'] != '' else ''
        result = {'result_str': result_str, 'message': message}
    else:
        result = None

    if result is not None and responses_path is not None:
        with open(responses_path, 'a', encoding='utf-8') as fr:
            fr.write(
                f'\n\tNEW REQUEST 🤩 @'
                f'{datetime.now().strftime("%m/%d/%Y %H:%M:%S")}\n'
                f'\t[INPUTS] Word: {form.word.data}, Number of neighbours: {form.num_neighbours.data}, Minimum frequency of a word from mixed vocab to be considered valid: {form.mixed_vocab_min_freq.data}, Maximum edit distance between incorrectly and correctly spelled words: {form.max_edit_distance.data}\n'
                f'\t[OUTPUTS] Result: {result_str}, Message: {message}\n'
            )

    return render_template(template_name + '.html', form=form, result=result)


if __name__ == '__main__':

    # set template name
    template_name = 'my_view'

    # create responses dir
    os.makedirs('responses', exist_ok=True)

    # specify responses file path
    responses_path = os.path.join('responses', f'{rule[1:]}_logs.txt')

    if responses_path is not None:
        with open(responses_path, 'a', encoding='utf-8') as f:
            f.write(
                f'\nstarting app.. '
                f'[{datetime.now().strftime("%m/%d/%Y %H:%M:%S")}]'
                f'\n'
            )

    # load fasttext vectors
    model = FastText.load(os.path.join('embeddings.txt'))

    # load clean and mixed sets of vocabulary
    clean_vocab_counter = load_vocab(os.path.join('clean_vocab_counter.json'))
    mixed_vocab_counter = load_vocab(os.path.join('mixed_vocab_counter.json'))

    # run app
    app.run(host='127.0.0.1', port=31137, debug=False)
