# OraZon - an Oracle for Amazon

## Introduction

E-commerce websites like Amazon have millions of products for sale. For answering queries about any product, there is a separate question answer section. However, most of the products either don’t have this section at all or sometimes fail to answer all the user queries.  The only way to get the information in this case is to go through all the product reviews.

We provide an automated system to find answers to any given user query. Using IR techniques we fetch the most relevant sentences to a user query and our attention based seq2seq model uses these sentences to generate a response.

## Related work

There has been some previous work in this domain concentrating on getting the top relevant reviews for the query. [[1]](https://arxiv.org/abs/1512.06863) learns a relevance function to rank the reviews. They use a Mixture of Experts model containing parameterized similarity measures like cosine similarity, Okapi BM25 etc., along with bilinear mappings to handle synonyms, to get the relevance of a review to the query. 

For similarity measures, [[2]](https://arxiv.org/abs/1703.02507) converts sentences to vectors, using the centroid of all words embeddings in the sentence, and then finds the similarity between vectors.

To generate a natural language answer, [[3]](https://arxiv.org/abs/1606.05491) uses a sequence to sequence ([[4]](https://arxiv.org/abs/1409.3215)) model to generate an answer. [[5]](https://arxiv.org/abs/1506.06714) uses such a sequence to sequence model which also takes a context, or in this case, a review into account while generating an answer to the question.    

## Dataset and our trained model

We have developed and tested our system based on the dataset provided by Julian McAuley. This dataset has two parts to it. One is just the Q/A data which contains information such as : Product id, category, questions asked for the product, a binary answer to the question in terms of yes/no and an subjective answer given by a human. Note that the answer provided here may not actually be a part of the reviews. The second part contains only the reviews of all the products listed by their IDs. 

[Link to the dataset for part 1 and part 2](https://drive.google.com/open?id=1wRxYr8XWYqWpYU-l599-STof4MCIh1Mu)

To train a network to generate a natural language answer, we used the target answers from the above dataset as the labels. The questions and the top sentences generated by part 1 were used as the input to our model.

[Link to our trained model for part 2](https://drive.google.com/open?id=19Rz8IBbBnaBW2u0ZIqpmFEFBGkwwP_B0)

The model files should be placed in the "checkpoints" folder in "gen_ans" directory.

## Proposed solution

### Part 1 - Finding the most similar sentence to the question from the reviews

One of the ways to get an answer to the query from the reviews will be to rank the reviews based on their relevance to the query. However, a review can have a lot of junk data too. Not only would a user not want to read this junk data, it also reduces the relevance of the review if it is taken as a whole. Hence, instead of taking a review as an entity, we break it into its constituent sentences. Ranking these sentences then gives a much better answer to the query.

To rank the sentences by their relevance to the query, we break down the sentence into unique tokens. We remove stop words from these tokens and calculate the following for each word:
- word embeddings for the word using word2vec method
- tf for the word in the given set of sentences
- idf for the word taking each sentence as a document
- tf.idf value

Now we estimate the representation of each sentence by finding the weighted centroid of all the vectors. We simply multiply the tf.idf weight of each word to its vector representation and then we take mean of these vectors. 

The final step is to find the cosine similarity of each sentence with the question/query sentence. The one with maximum similarity score is ranked the highest.

### Part 2 - Generating a natural language answer

#### Sequence to sequence models

Sequence to sequence models contain an encoder recurrent neural network (RNN) and a decoder RNN for end to end mapping of input to response. Following the architecture of a sequence to sequence model.

![Sequence to sequence model](https://i.stack.imgur.com/YjlBt.png)

The hidden state of the last RNN cell is given as the initial hidden state of the decoder. By doing this, the decoder is able to take the context of the input into account while generating a response. The decoder is trained to predict the next word in the sequence given the initial hidden state.

#### Our model

To generate a natural language answer, we follow the approach mentioned in [[5]](https://arxiv.org/abs/1506.06714). We build a sequence to sequence model with two encoders, one each for the question and a review. Each encoder is a bi-directional LSTM network and an attention mechanism is used at each time step of the context encoder. Following is the graph of our model exported from TensorFlow:

![](https://i.imgur.com/4TgdPd8.png)

This model helps us to use the encoded hidden states from both the question and the review from which an answer is to be extracted. The attention mechanism additionally helps us to focus on the parts of the review to focus on while generating the answer.

## Evaluation and analysis of results

We ran our models on four categories of products, namely - Musical Instruments, Patio, Lawn and Garden Products, Office Products and Baby Products. The major takeaway from part 1 was that word embeddings are an effective tool to identify relevant reviews to the question. Results for part 1:

| Category                        | Precision | Recall |
|:-------------------------------:|:---------:|:------:|
| Musical Instruments             | 74.2      |  49.6  |
| Patio, Lawn and Garden Products | 73.1      |  50.7  |
| Office Products                 | 92.4      |  64.2  |
| Baby Products                   | 80.2      |  55.3  |

For part 2, our model was able to respond to objective questions in terms of “yes” and “no”, but for subjective questions, it performed poorly. This can indicate that the model is able to learn short term dependencies like phrases and grammar. Results for part 2:

| Category                        |  BLEU  |  WMD  |
|:-------------------------------:|:------:|:-----:|
| Musical Instruments             | 0.68   | 0.49  |
| Patio, Lawn and Garden Products | 0.66   | 0.54  |
| Office Products                 | 0.78   | 0.59  |
| Baby Products                   | 0.73   | 0.61  |

## YouTube link

[Watch on YouTube](https://youtu.be/-it0gK1hBWI)

## Conclusion

We were able to give answers for user queries about the product without the user having to scroll and find the answers. We also learnt that word embeddings are an effective way to measure similarity between two documents. For generating a natural language answer, we can conclude that sequence to sequence models are a good way to map input and response sequences which have short term dependency, but they can still be improved to generate long answers.

## Ethical implications

The system will give misleading answers if the reviews have been attacked by spammers.

## References

[1] Julian McAuley and Alex Yang. Addressing Complex and Subjective Product-Related Queries with Customer Reviews. CoRR, 2015.

[2] Matteo Pagliardini, Prakhar Gupta and Martin Jaggi. Unsupervised Learning of Sentence Embeddings using Compositional n-Gram Features. CoRR, 2017.

[3] Ondřej Dušek and Filip Jurčíček. Sequence-to-Sequence Generation for Spoken Dialogue via Deep Syntax Trees and Strings. CoRR, 2016.

[4] Ilya Sutskever, Oriol Vinyals and Quoc V. Le. Sequence to Sequence Learning with Neural Networks. CoRR, 2014.

[5] Alessandro Sordoni, Michel Galley, Michael Auli, Chris Brockett, Yangfeng Ji, Margaret Mitchell, Jian-Yun Nie, Jianfeng Gao and Bill Dolan. A Neural Network Approach to Context-Sensitive Generation of Conversational Responses. CoRR, 2015
