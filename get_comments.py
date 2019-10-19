import os
import json
import requests
from argparse import ArgumentParser
headers= {'Accept': 'application/json'}
comment_ids_url = "https://api.pushshift.io/reddit/submission/comment_ids/{}"
get_all_comments_url = "https://api.pushshift.io/reddit/comment/search?ids={}"

def get_comments(filename):
    with open('./data/{}'.format(filename), 'r') as json_file:
        file_string = json_file.read()
        submission_json_all = json.loads(file_string)
        for i, submission in enumerate(submission_json_all["data"]):
            print("{} {}%".format(submission["title"], round(i/len(submission_json_all))))
            post_id = submission["id"]
            this_comment_ids_url = comment_ids_url.format(post_id)
            comments_ids_response = requests.get(this_comment_ids_url, headers=headers)
            comment_ids = json.loads(comments_ids_response.content.decode('utf-8'))["data"]
            get_all_comment_ids_url = get_all_comments_url.format(",".join(comment_ids))
            all_comments_response = requests.get(get_all_comment_ids_url, headers=headers)
            this_submissions_comments = json.loads(all_comments_response.content.decode('utf-8'))["data"]
            to_write = {'submission': submission,
                         'comments': this_submissions_comments
                         }
            with open('./data/reddit_parenting_submissions_with_comments/{}.json'.format(submission["id"]), 'wt') as _file:
                json.dump(to_write, _file)

parser = ArgumentParser()
parser.add_argument('--path', '-p')
args = parser.parse_args()

for filename in os.listdir(args.path):
    get_comments(filename)




