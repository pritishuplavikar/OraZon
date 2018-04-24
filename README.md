[//]: <> <center><img src= "http://www.lighthealing.com/loveoracle/images/orb-copy.jpg"></center>

## OraZon - an Oracle for Amazon

E-commerce websites like Amazon have millions of products for sale. For answering queries about any product, there is a separate question answer section. However, most of the products either don’t have this section at all or sometimes fail to answer all the user queries. In such cases, the user has to go through many product reviews to be sure that the product satisfies all his requirements, before making the purchase. For a popular product on Amazon, the number of reviews can be exceptionally huge. The user may be required to spend a lot of time going through these huge number of queries before finding relevant reviews and when the user is comparing multiple products the case is even more worse.

Our tool OraZon tries to solve this problem by analyzing all the product reviews and suggesting top 5 reviews which are most relevant to the user query. We are additionally finding top relevant sentences to the user query. As relevant sentences can have both positive and negative opinion polarity, we are generating two answers from top 5 sentences of both the polarities. 

With our tool in place, we plan to reduce the time spent by the user in making the the product purchase decision. Also, suggesting the top product reviews along with two automatically generated answers of different opinion polarities can help the user make a more informed purchase decision.

## Related work

There has been some previous work in this domain concentrating on getting the top relevant reviews for the query. [[1]](https://arxiv.org/abs/1512.06863) learns a relevance function to rank the reviews. They use a Mixture of Experts model containing parameterized similarity measures like cosine similarity, Okapi BM25 etc., along with bilinear mappings to handle synonyms, to get the relevance of a review to the query. 

For similarity measures, [[2]](https://arxiv.org/abs/1703.02507) converts sentences to vectors, using the centroid of all words embeddings in the sentence, and then finds the similarity between vectors.

To generate a natural language answer, [[3]](https://arxiv.org/abs/1606.05491) uses a sequence to sequence ([[4]](https://arxiv.org/abs/1409.3215)) model to generate an answer. [[5]](https://arxiv.org/abs/1506.06714) uses such a sequence to sequence model which also takes a context, or in this case, a review into account while generating an answer to the question.    

## Proposed solutions

### Approach 1 - Finding the most similar sentence to the question from the reviews

One of the ways to get an answer to the query from the reviews will be to rank the reviews based on their relevance to the query. However, a review can have a lot of junk data too. Not only would a user not want to read this jusn data, it also reduces the relevance of the review if it is taken as a whole. Hence, instead of taking a review as an entity, we break it into its constituent sentences. Ranking these sentences then gives a much better answer to the query.

To rank the sentences by their relevance to the query, we break down the sentence into unique tokens. We remove stop words from these tokens and calculate the following for each word:
- word embeddings for the word using word2vec method
- tf for the word in the given set of sentences
- idf for the word taking each sentence as a document
- tf.idf value

Now we estimate the representation of each sentence by finding the weighted centroid of all the vectors. We simply multiply the tf.idf weight of each word to its vector representation and then we take mean of these vectors. 

The final step is to find the cosine similarity of each sentence with the question/query sentence. The one with maximum similarity score is ranked the highest.

### Approach 2 - Generating a natural language answer

#### Sequence to sequence models

Sequence to sequence models contain an encoder recurrent neural network (RNN) and a decoder RNN for end to end mapping of input to response. Following the architecture of a sequence to sequence model.

![Sequence to sequence model](https://i.stack.imgur.com/YjlBt.png)

The hidden state of the last RNN cell is given as the initial hidden state of the decoder. By doing this, the decoder is able to take the context of the input into account while generating a response. The decoder is trained to predict the next word in the sequence given the initial hidden state.

#### Our model

To generate a natural language answer, we follow the approach mentioned in [[5]](https://arxiv.org/abs/1506.06714). We build a sequence to sequence model with two encoders, one each for the question and a review. Each encoder is a bi-directional LSTM network and an attention mechanism is used at each time step of the context encoder. Following is the graph of our model exported from TensorFlow:

![](https://i.imgur.com/4TgdPd8.png)

This model helps us to use the encoded hidden states from both the question and the review from which an answer is to be extracted. The attention mechanism additionally helps us to focus on the parts of the review to focus on while generating the answer.

## Evaluation and analysis of results

We ran our models on four categories of products, namely - Musical Instruments, Patio, Lawn and Garden Products, Office Products and Baby Products. These are the results obtained by using approach 1:

| Category                        | Precision | Recall |  BLEU  |  WMD  |
|:-------------------------------:|:---------:|:------:|:------:|:-----:|
| Musical Instruments             | 74.2      |  48.9  | $160   | 74.2  |
| Patio, Lawn and Garden Products | 74.2      |  74.2  | 74.2   | 74.2  |
| Office Products                 | 74.2      |  74.2  | 74.2   | 74.2  |
| Baby Products                   | 74.2      |  74.2  | 74.2   | 74.2  |

For approach 2, our model was able to respond to objective questions in terms of "yes" and "no", but for subjective questions, it performed poorly.

## Conclusion



## References

[1] Julian McAuley and Alex Yang. Addressing Complex and Subjective Product-Related Queries with Customer Reviews. CoRR, 2015.
[2] Matteo Pagliardini, Prakhar Gupta and Martin Jaggi. Unsupervised Learning of Sentence Embeddings using Compositional n-Gram Features. CoRR, 2017.
[3] Ondřej Dušek and Filip Jurčíček. Sequence-to-Sequence Generation for Spoken Dialogue via Deep Syntax Trees and Strings. CoRR, 2016.
[4] Ilya Sutskever, Oriol Vinyals and Quoc V. Le. Sequence to Sequence Learning with Neural Networks. CoRR, 2014.
[5] Alessandro Sordoni, Michel Galley, Michael Auli, Chris Brockett, Yangfeng Ji, Margaret Mitchell, Jian-Yun Nie, Jianfeng Gao and Bill Dolan. A Neural Network Approach to Context-Sensitive Generation of Conversational Responses. CoRR, 2015
