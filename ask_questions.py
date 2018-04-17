import question_generator as qg
import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file",help="File with candidate points to be asked")

args = parser.parse_args()
questions = qg.gen_questions(args.file)
print("Processing "+args.file) 
for user_id in questions.keys():
    print("Asking questions to "+user_id) 
    for q in questions[user_id]:
        print(json.dumps(q))
        #print(qg.push_question(q,user_id)) 



