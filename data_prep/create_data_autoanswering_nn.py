import json
from pprint import pprint

#Change the category name here
cat = "Cell_Phones_and_Accessories"

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

# Iterate the json objects one by one to extract the question and item id
for eachJsonObject in data:
    itemId = eachJsonObject['asin']
    question = eachJsonObject['question']
    answer = eachJsonObject['answer']
    
    try:
        print('item:'+ itemId + 'question:' + question)
	# For each item and question, generate answer using the  top 5 relevant sentences from the reviews
        l = get_answer.review_2_sent(question, 4, itemId)
        review = str(l[0][0]) + sep + str(l[1][0]) + sep + str(l[2][0]) + sep + str(l[3][0])  + sep
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
            print('ItemId: ' + itemId.strip() + ", Question: " + question.rstrip() + ", Answer:" + answer.rstrip() + ', Review: ' + review.rstrip())
    except ValueError:
        #print("ERRORRRR")
        cnt +=1
        errorL.append([itemId, question, answer])
review_file.close()
answer_file.close()
question_file.close()
