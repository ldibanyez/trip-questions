import json
import datetime
import requests

question_template = "stop.points.json"
points_file = "single_example.json"
ilog = "http://streambase1.disi.unitn.it:8091/user/newtask"
#last_id_file = "last_id"

def gen_questions(points_file):
    with open(points_file) as points_f:
        trips = json.load(points_f)
    question_dict = {}
    for t in trips:
        question_dict[t['uuid']] = []
    for t in trips:
        question_dict[t['uuid']].append(gen_question(question_template,t['points'][1]))
        #for q in p['points']: 
        #    question_dict[p['uuid']].append(gen_question(question_template,q))
    return question_dict

def gen_question(q_template,point):
    with open(q_template) as template_f:
        q_json = json.load(template_f)
    q_json = set_coordinates(q_json,point['point'])
    dt = datetime.datetime.strptime(point['datetime'],"%Y-%m-%d %H:%M:%S.%f")
    point['datetime'] = dt.strftime("%d-%m at %H:%M")
    q_json = set_stop_question(q_json,point)
    # No need to parameterise this anymore
    #q_json = set_mode_question(q_json,point)
    #q_json = set_change_question(q_json,point)
    return q_json

def set_coordinates(q_json,point):
    q_json[0]['q']['l']['lat'] = point[1]
    q_json[0]['q']['l']['lon'] = point[0]
    return q_json

def set_stop_question(q_json,point):
    q_json[0]['q']['p'][0]['t'] = q_json[0]['q']['p'][0]['t'].format(p=point)
    q_json[0]['q']['p'][1]['t'] = q_json[0]['q']['p'][1]['t'].format(p=point)
    return q_json

def set_mode_question(q_json,point):
    q_json[1]['q']['p'][0]['t'] = q_json[1]['q']['p'][0]['t'].format(p=point)
    q_json[1]['q']['p'][1]['t'] = q_json[1]['q']['p'][1]['t'].format(p=point)
    return q_json

def set_change_question(q_json,point):
    print(q_json[2]['q']['p'][0]['t'])
    print(q_json[2]['q']['p'][1]['t'])
    print(point)
    en_question = q_json[2]['q']['p'][0]['t'].format(p=point)
    it_question = q_json[2]['q']['p'][1]['t'].format(p=point)
    q_json[2]['q']['p'][0]['t'] = en_question
    #q_json[2]['q']['p'][1]['t'] = it_question
    return q_json

def push_question(q_json,user_id):
    headers = {
            'cache-control' : 'no-cache' ,
            'content' : json.dumps(q_json) ,
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' ,
            'email': 'soton@soton.co.uk' , 
            'password': '202c653a505f6815357bfa5d067ca5af0a742a839d764582e686d826554b52ad' ,
            'postman-token': 'e04fd2ac-9bab-b4e9-4b86-5001112099a8' , 
            't_title': 'Task' ,
            't_until': '864000' ,
            'usersalt': user_id 
            }
    r = requests.get(ilog,headers=headers)
    return r
    

def main():
    #with open(last_id_file) as infile:
    #    last = json.load(infile)
    #last_id = last['last_id']
    questions = gen_questions(points_file)
    for user_id in questions.keys():
        #print(user_id)
        for q in questions[user_id]:
            print(push_question(q,user_id))
            #print(json.dumps(q))
            print("----------------------------------")
    #last['last_id'] = questions[1]
    #with open(last_id_file,'w') as outfile:
    #    json.dump(last,outfile)
    
    
if __name__ == "__main__": main()
