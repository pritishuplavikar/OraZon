import json
from pprint import pprint
import get_answer
import sys
sys.path.insert(0, '../web')
import w2v_model
import _pickle as pickle
from w2v_model import word2vec
import numpy as np
import os
import time
import nltk
from time import gmtime, strftime



if len(sys.argv) < 2:
    print ("Error. Please enter the category as argument!")
    exit(0)
#Change the category name here
cat = sys.argv[1]

print (cat)

# Load the data from qa file for above category
data = json.load(open('../data_prep/data/' + cat+ '/' + cat + '_QA.json'))

cnt = 0
l = []
errorL = []
sep = ". "
review_file = open('../data_prep/output/' + cat + '/' + cat +  '_review_file.txt', 'w')
question_file = open('../data_prep/output/' + cat + '/' + cat +  '_question_file.txt', 'w')
answer_file = open('../data_prep/output/' + cat + '/' + cat +  '_answer_file.txt', 'w')
qc = 0
ac = 0
rc = 0

ob = word2vec()
path = "../data_prep/data/"
res = get_answer.get_dir_list(path)
print (res)
get_answer.ob = ob
driver = get_answer.Driver()
fp = open(path+"./../PR.txt", 'w')
driver.run_w2v(path+cat, fp)
fp.close()

# Iterate the json objects one by one to extract the question and item id
for eachJsonObject in data:
    itemId = eachJsonObject['asin']
    question = eachJsonObject['question']
    answer = eachJsonObject['answer']
    

    result = get_answer.review_2_sent(question, 4, itemId)
    topreviews = result['reviews']
    topsents = result['top']
    
    try:
	# For each item and question, generate answer using the  top 5 relevant sentences from the reviews
        l = topsents

        review = str(l[0]) + sep + str(l[1]) + sep + str(l[2]) + sep + str(l[3])  + sep
        review = review.strip('\n')
        review = review.replace('\n','')
        answer = answer.strip('\n')
        answer = answer.replace('\n','')
        question = question.strip('\n')
        question = question.replace('\n','')
        review = review.strip('\r')
        review = review.replace('\r','')
        answer = answer.strip('\r')
        answer = answer.replace('\r','')
        question = question.strip('\r')
        question = question.replace('\r','')
	# Write the item, question and generated answer in separate files
        if review != "" and answer  != "" and question != "":
            review_file.write(review + "\n")
            rc +=1 
            answer_file.write(answer + "\n")
            ac += 1
            question_file.write(question + "\n")
            qc += 1
    except ValueError:
        #print("ERRORRRR")
        cnt +=1
        errorL.append([itemId, question, answer])
review_file.close()
answer_file.close()
question_file.close()
