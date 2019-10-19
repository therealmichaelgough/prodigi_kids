from argparse import ArgumentParser
import json
import os
import gensim
import gensim.corpora as corpora
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from collections import Counter

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords

import re
import string
import collections


def get_tokens(word_string):
    tokens = []
    pos = []
    nltk_tokens = nltk.word_tokenize(word_string)
    for token in nltk_tokens:
        for garbage in ['\u200b', '_',"\"", "\'", "-", '`', '.', ',', '/']:
            token = token.replace(garbage, ' ')
        for split_token in token.split(' '):
            if not split_token or len(split_token) <=1:
                continue
            # remove punctuation and symbols
            if (not re.fullmatch('\W', split_token)):
                tokens.append(split_token.lower())
    pos.append(nltk.pos_tag(nltk_tokens))
    return {"tokens": tokens, "pos": pos}


def create_bow(filename):
    open_path = "./data/reddit_parenting_submissions_with_comments/{}".format(filename)
    with open(open_path, 'r') as json_file:
        json_contents = json.load(json_file)
        try:
            title = json_contents["submission"]["title"]
            post_body = json_contents["submission"]["selftext"]
            full_body_list = [title, post_body]

            for comment in json_contents["comments"]:
                full_body_list.append(comment["body"])

            tokenized_string = get_tokens(" ".join(full_body_list))
            write_filename = "./data/bow/{}-bow.json".format(filename.replace(".json", ""))
            to_write = {
                "bow": " ".join(tokenized_string["tokens"]),
                "pos": tokenized_string["pos"],
                "id": json_contents["submission"]["id"],
                "word_counts": Counter(tokenized_string["tokens"])
            }

            with open(write_filename, 'wt') as _file:
                json.dump(to_write, _file)
        except Exception as e:
            print("error {} on {}".format(e, open_path))


parser = ArgumentParser()
parser.add_argument('--path', '-p')
args = parser.parse_args()

total = len(os.listdir(args.path))
for i, filename in enumerate(os.listdir(args.path)):
    print("{}/{}: {}".format(i+1, total, filename))
    create_bow(filename)