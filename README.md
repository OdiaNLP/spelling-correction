# Odia Spelling Correction

Correct spellings of misspelled Odia words.

## Dependencies
See the dependencies in `requirements.txt`.
The code has been tested with Python 3.6.

## Overview

We use Fasttext for correcting spelling mistakes. Check out [this](https://fasttext.cc/) to get a guide 📘 to Fasttext.

- First download Odia text data with mixed vocabulary.

```shell
mkdir data
cd data

!wget https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/data/monolingual/indicnlp_v1/sentence/or.txt.gz
tar -zxvf or.txt.gz
head or

```
- Then download text with clean vocabulary from [Kaggle](https://www.kaggle.com/soumendrak/odia-structured-dictionary).
Put that inside `data` directory.
- Train Fasttext embeddings. See the notebook `fasttext.ipynb`.
- Build two sets of vocabulary, one mixed and another clean. See the notebook `vocabulary.ipynb`.
- Finally run `controller.py` to start the web app. Go to http://127.0.0.1:31137/spelling to access the web app.

```shell
# web app
python controller.py  # open http://127.0.0.1:31137/spelling in browser
```

## Snapshot of web app
<img src="/snapshot.png" width="75%" height="75%"/>

[LICENSE](https://github.com/OdiaNLP/spelling-correction/blob/main/LICENSE)
