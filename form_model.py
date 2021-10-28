from wtforms import Form, validators, StringField, IntegerField


class InputForm(Form):
    """Input form class"""
    word = StringField(label='Odia word', default="ସାପ୍ତାହୀକ", validators=[validators.InputRequired()])
    num_neighbours = IntegerField(label='Number of neighbours', default=10, validators=[validators.InputRequired()])
    mixed_vocab_min_freq = IntegerField(label='Minimum frequency of a word from mixed vocab to be considered valid',
                                        default=50, validators=[validators.InputRequired()])
    max_edit_distance = IntegerField(label='Maximum edit distance between incorrectly and correctly spelled words',
                                     default=2, validators=[validators.InputRequired()])
