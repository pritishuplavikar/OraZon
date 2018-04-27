import glob
import numpy as np
import pickle
from tqdm import tqdm
import tensorflow as tf
import tensorflow.contrib.legacy_seq2seq as seq2seq
import json
import os
import nltk
from time import gmtime, strftime
import random
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

class Demo:
    def __init__(self, cat):
        self.unique_words = pickle.load(open('unique_words.p', 'rb'))
        self.word2idx, self.idx2word, self.vocab_size = self.build_vocabs(self.unique_words)
        self.cat = cat

    def build_vocabs(self, unique_words):
        word2idx = {value:index for index, value in enumerate(unique_words)}
        idx2word = {index:value for index, value in enumerate(unique_words)}
    
        return word2idx, idx2word, len(word2idx)

    def num2sent(self, pred, mode, seq_len=None):
        res = ""
        if mode == "q":
            pred = pred[:seq_len]        
            for idx in pred:
                res += self.idx2word[idx] + " "
        elif mode == "t":
            pred = pred[:seq_len]
            for idx in pred:
                res += self.idx2word[idx] + " "
        elif mode == "a":
            pred = pred[1:-1]
            for idx in pred:
                res += self.idx2word[idx] + " "
        return res, pred

    def test_sample(self, test_sess, ques, ques_len, review, rev_len, bs=1):
        dec_input = np.zeros((1, 1)) + self.word2idx['<START>']
        dec_len = [1]
        while dec_input[0, -1] != self.word2idx['<EOS>']:
            batch_logits = test_sess.run("decoder_lstm/decoder/transpose:0",
                           feed_dict = {"encoder_inputs:0": [ques],
                                        "context_encoder_inputs:0": [review],
                                        "decoder_inputs:0": dec_input,
                                        "encoder_lengths:0": [ques_len],
                                        "context_encoder_lengths:0": [rev_len],
                                        "decoder_lengths:0": dec_len,
                                        "batch_size:0": bs})
            prediction = batch_logits[:,-1].argmax(axis=-1)
            dec_len[0] += 1

            dec_input = np.hstack([dec_input, prediction[:,None]])

        return dec_input[0]

    # Demo
    def predict(self, ques, review):
        musical_model = "epoch_10_2018-04-23_09_25_56"
        office_model = "epoch_10_2018-04-26_04_35_11"
        if self.cat == 'Office_Products':
            model = office_model
        elif self.cat == 'Musical_Instruments':
            model = musical_model
        model = musical_model
        self.cat = 'Musical_Instruments'
        with tf.Session() as demo_sess:
            print ("category is: " + self.cat)
            print ("model is: " + model)
            saver = tf.train.import_meta_graph('./checkpoints/' + self.cat + '/' + model+'.meta')
            saver.restore(demo_sess, tf.train.latest_checkpoint('./checkpoints/' + self.cat + '/'))

            ques = nltk.word_tokenize(ques)
            ques = [token.lower() for token in ques]

            for idx, word in enumerate(ques):
                if word in self.word2idx:
                    ques[idx] = self.word2idx[word]
                else:
                    ques[idx] = self.word2idx["<UNK>"]

            ques += [self.word2idx['<EOS>']]
            
            review = nltk.word_tokenize(review)
            review = [token.lower() for token in review]

            for idx, word in enumerate(review):
                if word in self.word2idx:
                    review[idx] = self.word2idx[word]
                else:
                    review[idx] = self.word2idx["<UNK>"]

            review += [self.word2idx['<EOS>']]
            
            predict = self.test_sample(demo_sess, ques, len(ques), review, len(review))
            prediction, _ = self.num2sent(predict, mode="a")

        return prediction
# d= Demo()
# q = "does this pedal work on Yamaha P-35 keyboards?"
# r = "In my opinion, a sustain pedal like the M-Audio SP-2 Sustain Pedal with Piano Style Action or other similar pedal is a much better choice. If you are not use to using a large sustaining pedal while playing the piano, it may appear little awkward. I love it, I used this for my Yamaha ypt-230 and it works great, I would recommend it to anyone. I got it to have it if I needed it."
# res = d.predict(q, r)
# print (res) 
