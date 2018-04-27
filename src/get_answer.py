from scipy import spatial
import operator
import nltk
from nltk.corpus import stopwords
import string
from w2v_model import word2vec

import os
import sys
import re
from w2v_model import word2vec
import math

ob = None

class Driver:
    #ob = word2vec()
    def run_w2v(self, folder, fp):
        category = (folder.split('/'))[3]
        review_file = os.path.join(folder, category + "_Review.json")
        question_file = os.path.join(folder, category + "_QA.json")
        dict_file = os.path.join(folder, category + "_Dict.p")
        wordvec_file = os.path.join(folder, category + "_WordVec.p")
        model_file = os.path.join(folder, category + "_Model.p")
        #ob = word2vec()
        global ob
        if check_file_exists(dict_file,wordvec_file,model_file):
            print("loading data")
            ob.read_data(dict_file,wordvec_file,model_file)
            ob.init_word2vect(False)
        else:
        #read the files
            print("creating data files")
            print ("Reading files", review_file)
            ob.read_file_review(review_file)
            ob.read_file_question(question_file)
            #perform wordvec
            print ("Performing Word2Vec")
            ob.init_word2vect(True)
            ob.get_review_dump(review_file)
            #dump
            print ("Dumping Pickles")
            ob.dump_data(dict_file, wordvec_file, model_file)
            #test code
            for p in ob.test_questions:
                if len(ob.test_questions[p]) == 0:
                    del ob.test_questions[p]
            print ("Total products with Questions = %d" % len(ob.test_questions))
            print ("Processing")
            ob.test_code(fp)
            #x = ob.predict("does this pedal work on Yamaha P-35 keyboards?",6,[],"B00005ML71")
            #print x

def get_dir_list(path_name):
    path_name = "ls "+path_name+" > sample.txt"
    os.system(path_name)
    f = open('sample.txt','r')
    res = []
    for line in f:
        line = line.strip()
        res.append(line)
    os.system("rm -f sample.txt")
    return res

def check_file_exists(dict_file,wordvec_file,model_file):
    if not os.path.exists(dict_file) or os.path.getsize(dict_file) == 0:
        return False
    if not os.path.exists(wordvec_file) or os.path.getsize(wordvec_file) == 0:
        return False
    if not os.path.exists(model_file) or os.path.getsize(model_file) == 0:
        return False
    return True

def get_reviews(test_question,num_of_reviews,product_id):
    global ob
    x,y,z,reviews = ob.predict(test_question,num_of_reviews,[],product_id)
    return reviews

def get_sentences(reviews):
    vocab_freq = {}
    sentences = []
    for r in reviews:
        lines = r[0].split('.')
        for line in lines:
            translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
            line = line.lower().translate(translator)
            s = line.strip()
            if len(s)>4:
                sentences.append(s)
                for word in s.split(' '):
                    pw = word.strip(")( []{},")
                    if len(pw)>1 and pw in vocab_freq:
                        vocab_freq[pw]+=1
                    elif len(pw)>1:
                        vocab_freq[pw]=1
    return vocab_freq,sentences

def get_normalised_idf(idf,length):
    n_idf={}
    for word in idf:
        n_idf[word] = math.log(length/float(idf[word]+1))
    return n_idf

def get_idf(vocab_freq,sentences):
    idf = {}
    stp = set(stopwords.words('english'))
    for word in vocab_freq:
        if word not in stp:
            for s in sentences:
                if word in s:
                    if word in idf:
                        idf[word]+=1
                    else:
                        idf[word]=1
    n_idf = get_normalised_idf(idf,len(sentences))
    return n_idf

def count_tf(word,wordList):
    c =0
    for w in wordList:
        if w== word:
            c+=1
    return c
    
def get_sentence_vectors(sentences,n_idf):
    sent_dict = {}
    n_sent_dict = {}
    global ob
    for s in sentences:
        wordList=[]
        for word in s.split(' '):
            if len(word)>1:
                wordList.append(word.strip(")( []{},"))
        s_vec_lcl=[]
        n_vec_lcl=[]
        for word in wordList:
            if word in ob.model.wv.vocab:
                sc =1
                if word in n_idf:
                    sc = n_idf[word]*(count_tf(word,wordList)/float(len(wordList)))
                l=[x * sc for x in ob.model[word]]
                s_vec_lcl.append(l)
                n_vec_lcl.append(ob.model[word])
            else:
                s_vec_lcl.append([0]*100)
                n_vec_lcl.append([0]*100)
        if len(s_vec_lcl)>0:
            sent_dict[s]=ob.compute_centroid(s_vec_lcl)
            n_sent_dict[s] = ob.compute_centroid(n_vec_lcl)

    return sent_dict,n_sent_dict

def get_q_vec(test_question,n_idf):
    qlist=[]
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    test_question = test_question.translate(translator).strip()
    stp = set(stopwords.words('english'))
    for word in test_question.split(' '):
        word = word.strip(")( []{},")
        if len(word)>1 and word not in stp:
            qlist.append(word)
    q_w_vec=[]
    q_n_vec=[]
    global ob
    for word in qlist:
        if word in ob.model.wv.vocab:
            sc =1
            if word in n_idf:
                sc = n_idf[word]*(count_tf(word,qlist)/float(len(qlist)))
            q_w_vec.append([x * sc for x in ob.model[word]])
            q_n_vec.append(ob.model[word])
        else:
            q_w_vec.append([0]*100) ## for unknown words
            q_n_vec.append([0]*100)
    q_vec_w = ob.compute_centroid(q_w_vec)
    q_vec_n = ob.compute_centroid(q_n_vec)
    return q_vec_w,q_vec_n

def get_cosine_similarity(sent_dict,q_vec):
    cosine_sent = {}
    for vec in sent_dict:
        cosine_sent[vec] = 1 - spatial.distance.cosine(sent_dict[vec],q_vec)
    return cosine_sent

def get_top_sent(cosine_sent):
    sorted_sent = sorted(cosine_sent.items(), key=operator.itemgetter(1), reverse=True)
    sent = []
    for s in sorted_sent:
        sent.append(s)
    return sent

def print_top(sentences, num_r):
    ind = 0;
    for s in sentences:
        print (s)
        ind+=1
        if ind == num_r:
            break

def get_sentiment(reviews,sentiment):
    result=[]
    for r in reviews:
        if r[1]==sentiment:
            result.append(r)
    return result

def get_ranked_sent(reviews,question):
    vocab_freq,sentences = get_sentences(reviews)
    n_idf = get_idf(vocab_freq,sentences)
    sent_dict,n_sent_dict = get_sentence_vectors(sentences,n_idf)
    q_vec_w,q_vec_n = get_q_vec(question,n_idf)
    wt_cosine = get_cosine_similarity(sent_dict,q_vec_w)
    nm_cosine = get_cosine_similarity(n_sent_dict,q_vec_n)
    wt_sent = get_top_sent(wt_cosine)
    nm_sent = get_top_sent(nm_cosine)
    return wt_sent

def formatted_answer(all_rev,pos,neg):
    toprev = []
    for s in all_rev[:6]:
        toprev.append(s[0])
    finalPos=""
    finalNeg=""    
    for s in pos:
        if s[0] in toprev:
            finalPos=finalPos+s[0]+'.'
    for s in neg:
        if s[0] in toprev:
            finalNeg=finalNeg+s[0]+'.'

    return {'positive':finalPos,'negative':finalNeg}

def get_relevant_reviews(reviews,k):
    review_list =[]
    for r in reviews:
        review_list.append(r[0])
        if(len(review_list)==k):
            break
    return review_list


def review_2_sent(question,num_r,p_id):
    reviews = get_reviews(question,50,p_id)
    #print reviews
    pos_reviews = get_sentiment(reviews,"Yes")
    neg_reviews = get_sentiment(reviews,"No")
    wt_sent_pos=[]
    wt_sent_neg=[]
    wt_sent_all = get_ranked_sent(reviews,question)
    # if len(pos_reviews)>0:
    #     wt_sent_pos = get_ranked_sent(pos_reviews,question)
    #     #print_top(wt_sent_pos,5)
    # if len(neg_reviews)>0:
    #     wt_sent_neg = get_ranked_sent(neg_reviews,question)
    #     #print_top(wt_sent_neg,5)
    top = []
    for s in  wt_sent_all:
        top.append(s[0])
    answer = formatted_answer(wt_sent_all,wt_sent_pos,wt_sent_neg)
    answer['reviews'] = get_relevant_reviews(reviews,num_r)
    answer['top'] = top[:num_r]
    return answer
