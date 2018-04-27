import json
import sys
import re
import nltk
import _pickle as pickle
from nltk.corpus import stopwords
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
import gensim, logging
from scipy import spatial
import heapq
from utils import modelutils
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class word2vec:
	word_dict = set([])
	stop = None
	model = None
	# based on product id
	json_object_wordvec = {}
	test_questions = {}
	word_type = {}
	accuracy = 0.0
	total_valid_values = 0.0
	precison_matrix = None
	def __init__(self):
		self.precison_matrix = [[0 for x in range(2)] for y in range(2)] 
		self.set_zero(self.precison_matrix)
		nltk.download('averaged_perceptron_tagger')
		nltk.download('sentiwordnet')
		nltk.download('wordnet')
		nltk.download('punkt')
		self.stop = set(stopwords.words('english'))
		self.init_word_type()


	def init_word_type(self):
		# adjective
		self.word_type['JJ'] = 'a'
		self.word_type['JJR'] = 'a'
		self.word_type['JJS'] = 'a'
		self.word_type['NN'] = 'n'
		self.word_type['NNS'] = 'n'
		self.word_type['NNP'] = 'n'
		self.word_type['NNPS'] = 'n'
		self.word_type['RB'] = 'r'
		self.word_type['RBR'] = 'r'
		self.word_type['RBS'] = 'r'
		self.word_type['VB'] = 'v'
		self.word_type['VBD'] = 'v'
		self.word_type['VBG'] = 'v'
		self.word_type['VBN'] = 'v'
		self.word_type['VBP'] = 'v'
		self.word_type['VBZ'] = 'v'


	def read_file_review(self,file_name):
		with open(file_name) as f:
			for line in f:
				while True:
					try:
						jfile = json.loads(line)
						for product_id in jfile:
							for each_review in jfile[product_id]:
								word = each_review['reviewText']
								word = re.split('\W+',word)
								word = self.remove_stop_words(word)
								# remove stop words
								for each_word in word:
									self.word_dict.add(each_word)

						break
					except ValueError:
						line += next(f)


	def read_file_question(self,file_name):
		with open(file_name) as f:
			for line in f:
				while True:
					try:
						jfile = json.loads(line)
						for json_object in jfile:
							product_id = json_object['asin']
							if product_id in self.test_questions.keys():
								self.test_questions[product_id].append(json_object)
							else:
								dummy = []
								dummy.append(json_object)
								self.test_questions[product_id]=dummy
							question = json_object['question']
							question = re.split('\W+',question)
							question = self.remove_stop_words(question)
							for term in question:
								# remove stop words, need to add
								self.word_dict.add(term)
						break
					except ValueError:
						line+=next(f)


	def init_word2vect(self,reload):
		sentence = []
		sentence.append(self.word_dict)
		if reload:
			self.model = gensim.models.Word2Vec(sentence, min_count=1)


	def get_review_dump(self,file_name):
		with open(file_name) as f:
			for line in f:
				while True:
					try:
						jfile = json.loads(line)
						for product_id in jfile:
							rev_vect = []
							rev_vect_act = []
							for each_review in jfile[product_id]:
								rev_vect_lcl = []
								word = each_review['reviewText']
								word = re.split('\W+',word)
								# remove stop words
								word = self.remove_stop_words(word)
								unique_words = set()
								for each_word in word:
									unique_words.add(each_word)
								# for each word there is word vec
								for term in unique_words:
									if term in self.model.wv.vocab:
										rev_vect_lcl.append(self.model[term])
								rev_vect_lcl = self.compute_centroid(rev_vect_lcl)
								rev_vect.append(rev_vect_lcl)
								rev_vect_act.append(each_review['reviewText'])
							details = {}
							details['vector'] = rev_vect
							details['actual'] = rev_vect_act
							self.json_object_wordvec[product_id] = details
						break
					except ValueError:
						line+=next(f)
	

	def dump_data(self, dict_file_name, wordvec_file_name, model_file_name):
		with open(dict_file_name, 'wb') as f:
			pickle.dump(self.word_dict, f)
		with open(wordvec_file_name, 'wb') as f:
			pickle.dump(self.json_object_wordvec, f)
		with open(model_file_name, 'wb') as f:
			pickle.dump(self.model, f)



	def read_data(self, dict_file_name, wordvec_file_name, model_file_name):
		with open(dict_file_name, 'rb') as f:
			print("reading dict")
			self.word_dict = pickle.load(f)
		with open(wordvec_file_name, 'rb') as f:
			print("reading word vec")
			self.json_object_wordvec = pickle.load(f)
		with open(model_file_name, 'rb') as f:
			print("reading model")
			self.model = pickle.load(f)
		print("done")

	def test_code(self,fp):
		product_precision = 0.0
		product_accuracy = 0.0
		product_recall = 0.0
		count = 1
		tot_prods = len(self.test_questions)
		for product_id in self.test_questions:
			'''
			print count
			sys.stdout.write("\033[F")
			count += 1
			'''
			for question in self.test_questions[product_id]:
				answer_type = question['answerType']
				if answer_type == "Y" or answer_type == "N":
					review_score_heap = self.get_relevant_reviews(product_id,question['question'])
					self.get_precision_recall(review_score_heap, product_id, answer_type)
			# Print Statistics
			if self.total_valid_values != 0:
				product_precision +=  (self.precison_matrix[0][0]/self.total_valid_values)
				product_recall +=  (self.precison_matrix[1][0]/self.total_valid_values)
				product_accuracy += (self.accuracy/self.total_valid_values)
			self.accuracy = 0.0
			self.total_valid_values = 0.0
			self.set_zero(self.precison_matrix)
		
		prc = str((product_precision/tot_prods)*100.0)
		rcl = str((product_recall/tot_prods)*100.0)
		acc = str((product_accuracy/tot_prods)*100.0)
		
		fp.write("Category Precision : "+prc+"\n")
		fp.write("Category Recall : "+rcl+"\n")
		fp.write("#######################\n")
		
		print ("Category Precision : "+prc+"\n")
		print ("Category Recall : "+rcl+"\n")
		print ("#######################\n")

	
	def predict(self, question, k, top_reviews, product_id):
		ranked_reviews = self.get_relevant_reviews(product_id, question)
		expert_scores = []
		expert_votes = []
		for i in range(min(5,len(ranked_reviews))):
			val = ranked_reviews[i]
			if len(val[1]) == 0:
				continue
			expert_scores.append(val[0])
			vote = self.binary_voting_function(val[1])
			#print (val[1], val[0], vote)
			expert_votes.append(vote)
			polarity = "No"
			if vote >= 0.5:
				polarity = "Yes"
			if k > 0:
				top_reviews.append([val[1], polarity])
			k = k - 1
		#print "top reviews" , top_reviews
		#print "expert scores" , expert_scores
		#print "expert votes" , expert_votes
		classification = modelutils.mixture_of_experts(expert_scores, expert_votes)
		return classification,expert_scores,expert_votes,top_reviews


	def get_relevant_reviews(self,product_id,question):
		text = question
		text = re.split('\W+',text)
		unique_words = set()
		for term in text:
			unique_words.add(term)
		qa_vec_lcl = []
		for term in unique_words:
			if term in self.model.wv.vocab:
				qa_vec_lcl.append(self.model[term])
		qa_vec_lcl = self.compute_centroid(qa_vec_lcl)
		review_score_heap = self.relevance_scoring_function(qa_vec_lcl,self.json_object_wordvec[product_id])
		return review_score_heap


	def relevance_scoring_function(self,qa_vec_lcl,reviews):
		vector = reviews['vector']
		actual = reviews['actual']
		len_val = len(vector)
		heap1 = []
		assert len(vector) == len(actual)
		for i in range(0,len_val):
			if len(qa_vec_lcl) == len(vector[i]):
				result = 1 - spatial.distance.cosine(qa_vec_lcl,vector[i])
				heap1.append([result,actual[i]])
		heap1.sort(reverse=True)
		return heap1

	# Returns the probability of review saying Yes
	def binary_voting_function(self,text):
		token = nltk.word_tokenize(text)
		token = self.remove_stop_words(token)
		tagged = nltk.pos_tag(token)
		positive_score = 0.0
		negative_score = 0.0
		for each_tagged in tagged:
			term = each_tagged[0]
			tag_type = each_tagged[1]
			if tag_type in self.word_type:
				synset_list = wn.synsets(term)
				if len(synset_list)!=0:
					senti = synset_list[0].name()
					senti_obj = swn.senti_synset(senti)
					positive_score = positive_score + float(senti_obj.pos_score())
					negative_score = negative_score + float(senti_obj.neg_score())
		if (positive_score + negative_score == 0.0):
			return 0.0
		return float(positive_score) / float(positive_score + negative_score)


	def get_precision_recall(self, review_score_heap,product_id, answer_type):
		lcl_matrix_positive= [[0 for x in range(2)] for y in range(2)] 
		lcl_matrix_negative =[[0 for x in range(2)] for y in range(2)] 
		self.set_zero(lcl_matrix_positive)
		self.set_zero(lcl_matrix_negative)
		len_question = len(self.test_questions[product_id])
		no_of_reviews = float(len(review_score_heap))
		correct_classified = 0.0
		for i in range(len(review_score_heap)):
			val = review_score_heap[i]
			assert len(val)==2
			yes_prob = self.binary_voting_function(val[1])
			pol = "No"
			if yes_prob >= 0.5:
				pol = "Yes"
			if answer_type == 'Y':
				if pol == "Yes":
					correct_classified += 1.0
					lcl_matrix_positive[0][0] = lcl_matrix_positive[0][0] +1.0
					lcl_matrix_negative[0][1] = lcl_matrix_negative[0][1] + 1.0
				else:
					lcl_matrix_positive[1][0] = lcl_matrix_positive[1][0] + 1.0
			elif answer_type == 'N':
				if pol == "No":
					correct_classified += 1.0
					lcl_matrix_negative[0][0] = lcl_matrix_negative[0][0] + 1.0
					lcl_matrix_positive[0][1] = lcl_matrix_positive[0][1] + 1.0
				else:
					lcl_matrix_negative[1][0] = lcl_matrix_negative[1][0] + 1.0
		self.accuracy += (correct_classified/no_of_reviews)
		#Update the precision matrix
		if answer_type == 'Y' or answer_type == 'N':
			self.total_valid_values = self.total_valid_values + 1.0
			if answer_type == 'Y':
				prec_denom = (float(lcl_matrix_positive[0][0])+float(lcl_matrix_positive[0][1]))
				recal_denom = (float(lcl_matrix_positive[0][0])+float(lcl_matrix_positive[1][0]))
				if prec_denom == 0:
					prec_denom = 1.0
				if recal_denom == 0:
					recal_denom = 1.0
				Precision_positive = float(lcl_matrix_positive[0][0])/prec_denom
				Recall_positive = float(lcl_matrix_positive[0][0])/recal_denom
				self.precison_matrix[0][0] = self.precison_matrix[0][0] + Precision_positive
				self.precison_matrix[1][0] = self.precison_matrix[1][0] + Recall_positive
			elif answer_type == 'N':
				prec_denom = (float(lcl_matrix_negative[0][0])+float(lcl_matrix_negative[0][1]))
				recal_denom = (float(lcl_matrix_negative[0][0])+float(lcl_matrix_negative[1][0]))
				if prec_denom == 0:
					prec_denom = 1.0
				if recal_denom == 0:
					recal_denom = 1.0
				Precision_negative = float(lcl_matrix_negative[0][0])/prec_denom
				Recall_negative = float(lcl_matrix_negative[0][0])/recal_denom
				self.precison_matrix[0][0] = self.precison_matrix[0][0] + Precision_negative
				self.precison_matrix[1][0] = self.precison_matrix[1][0] + Recall_negative


	def set_zero(self,matrix):
		matrix[0][0]=0.0
		matrix[0][1]=0.0
		matrix[1][0]=0.0
		matrix[1][1]=0.0


	def remove_stop_words(self,word):
		# need to add part of code to remove stop words
		res = []
		for term in word:
			if term not in self.stop:
				res.append(term)
		return res


	def compute_centroid(self,rev_vect):
		# we have word vec with 100 features , so this value we can set
		# use different value for different number of features
		res = []
		len_val = len(rev_vect)
		if len_val == 0:
			return res
		for i in range(0,100):
			sum_val = 0.0
			for each_rev_word in rev_vect:
				sum_val = sum_val + each_rev_word[i]
			sum_val = sum_val/len_val
			res.append(sum_val)
		return res
