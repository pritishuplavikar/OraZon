import _pickle as pickle
import sys  
sys.path.insert(0, '../src')
import get_answer
from w2v_model import word2vec
import numpy as np
import os
import time
import nltk
from time import gmtime, strftime
import random
import demo
from nltk.translate.bleu_score import sentence_bleu
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def  predict(productId, question, category, no_of_ans = 4):
	ob = word2vec()
	path = "../data_prep/data/"
	res = get_answer.get_dir_list(path)
	print (res)
	get_answer.ob = ob
	driver = get_answer.Driver()
	fp = open(path+"./../PR.txt", 'w')
	driver.run_w2v(path+category, fp)
	fp.close()

	result = get_answer.review_2_sent(question, no_of_ans, productId)
	top5reviews = result['reviews']
	top5sents = result['top']
	return top5reviews, top5sents


def gen_answer(question, top5sents, category):
	review = ""
	for s in top5sents:
		review += s + ". "
	d = demo.Demo(category)
	res = d.predict(question, review)
	return res
#predict('B0002F58TG', 'How is the quality of the guitar ?', 'Musical_Instruments')
