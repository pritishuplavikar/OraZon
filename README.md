## OraZon - an Oracle for Amazon

E-commerce websites like Amazon have millions of products for sale. For answering queries about any product, there is a separate question answer section. However, most of the products either don’t have this section at all or sometimes fail to answer all the user queries. In such cases, the user has to go through many product reviews to be sure that the product satisfies all his requirements, before making the purchase. For a popular product on Amazon, the number of reviews can be exceptionally huge. The user may be required to spend a lot of time going through these huge number of queries before finding relevant reviews and when the user is comparing multiple products the case is even more worse.

Our tool OraZon tries to solve this problem by analyzing all the product reviews and suggesting top 5 reviews which are most relevant to the user query. We are additionally finding top relevant sentences to the user query. As relevant sentences can have both positive and negative opinion polarity, we are generating two answers from top 5 sentences of both the polarities. 

With our tool in place, we plan to reduce the time spent by the user in making the the product purchase decision. Also, suggesting the top product reviews along with two automatically generated answers of different opinion polarities can help the user make a more informed purchase decision.

## Related work

There has been some previous work in this domain concentrating on getting the top relevant reviews for the query. [[1]](https://arxiv.org/abs/1512.06863) learns a relevance function to rank the reviews. They use a Mixture of Experts model containing parameterized similarity measures like cosine similarity, Okapi BM25 etc., along with bilinear mappings to handle synonyms, to get the relevance of a review to the query. 

For similarity measures, [[2]](https://arxiv.org/abs/1703.02507) converts sentences to vectors, using the centroid of all words embeddings in the sentence, and then finds the similarity between vectors.

To generate a natural language answer, [[3]](https://arxiv.org/pdf/1606.05491.pdf) uses a sequence to sequence ([[4]](https://arxiv.org/abs/1409.3215)) model to generate an answer. [[5]](https://arxiv.org/abs/1506.06714) uses such a sequence to sequence model which also takes a context, or in this case, a review into account while generating an answer to the question.    

![](http://www.lighthealing.com/loveoracle/loveoracle.aspx?raw=true) "OraZon")





### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/pritishuplavikar/orazon/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Orazon project



### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
