<p align="center">
  <a href="" rel="noopener">
 <img  height=200px src="https://github.com/pauladj/nlp-cyberpunk-2077-reviews/raw/master/img/cover.jpg" alt="Project logo"></a>
</p>
<h3 align="center">Text Mining Analysis for Cyberpunk 2077 Reviews</h3>

<div align="center">
    <img src="https://img.shields.io/badge/python-v3.7.9-blue" />
</div>

---

<p align="center">Cyberpunk 2077 is the new Cyberpunk game, and it was released a month ago (December 10, 2020). These last few days, I’ve seen many negative reviews, so I was curious to know what the gamers think.
    <br> 
    <br>
    <a href="https://github.com/pauladj/nlp-cyberpunk-2077-reviews/blob/master/Cyberpunk%20reviews.ipynb"><img src="https://img.shields.io/badge/Jupyter-Open notebook-red?logo=jupyter"></a> </p>
    
## Data Understanding

### Data Source

The reviews have been gathered from Steam using a [python library](https://pypi.org/project/steamreviews/). I only collected last week's reviews because there are more than 100,000. I got 7096 reviews, enough to explore and gain insights from the users' thoughts. 

![](https://github.com/pauladj/nlp-cyberpunk-2077-reviews/raw/master/img/dataset.jpg)

<p type="caption">First rows of the dataset</p>

### Data cleaning

After seeing the first few reviews, I decided which transformations to apply to get clean reviews. I lemmatized the words and removed stopwords. Stopwords are frequently used words, such as "and" or "the", that don't add a lot of information. I also added some new ones to the default list. On top of that, I only kept words with more than two characters to quickly discard some mistyped tokens.

```python
STOPWORDS = set(stopwords.words('english')+["game", "really", "would", "one", "much", 
                                            "many", "could", "way", "also", "feel", 												
                                            "like", "think", 'get', 'play', 
                                            'still', 'even', 'say', 'make'])
```

```python
def clean_text(text):
    """
    Clean the text
    """
    # lowercase text
    text = str(text).lower() 
    # strip html tags
    text = strip_html_tags(text) 
    # remove accented chars
    text = remove_accented_chars(text) 
    # expand contractions
    text = contractions.fix(text) 
    # tokenize 
    text = nltk.word_tokenize(text) 
    # remove special characters 
    text = [remove_special_characters(x) for x in text if remove_special_characters(x)]
    # lemmatize 
    text = lemmatize_text(" ".join(text)) 
    # remove stopwords and join the tokens
    text = ' '.join(word for word in text if word not in STOPWORDS and len(word) > 2) 
    return text
    
df['text_clean'] = df['text'].apply(clean_text)
```


![](https://github.com/pauladj/nlp-cyberpunk-2077-reviews/raw/master/img/before_clean.jpg)

<p type="caption">Before cleaning</p>

![](https://github.com/pauladj/nlp-cyberpunk-2077-reviews/raw/master/img/after_clean.jpg)

<p type="caption">After cleaning</p>

### Exploratory Data Analysis

#### Word count distribution

![](https://github.com/pauladj/nlp-cyberpunk-2077-reviews/raw/master/img/word_count.png)

Some of the reviews have only one word. We delete all the reviews with less than 30 words to ensure we have enough text to analyze.

#### Most common words

We can see how words like *story*, *good*, *time*, and *world* are used a lot. Some other words are *bug*, *experience*, *enjoy*, *character*, *fun*, and *bad*. We know what are the most common words, but we still don't know in what context they use them. After reading some online reviews, we see the game has some noticeable bugs, so it's consistent with the mentioned words.

![](https://github.com/pauladj/nlp-cyberpunk-2077-reviews/raw/master/img/top_50_words.png)

![](https://github.com/pauladj/nlp-cyberpunk-2077-reviews/raw/master/img/wordcloud.png)

#### Bigrams and Trigrams

We generate the most used bigrams and trigrams.

They talk a lot about the quests, the city, the world, the main story, and bugs.

![](https://github.com/pauladj/nlp-cyberpunk-2077-reviews/raw/master/img/bigram.png)

We can see how they also talk about some other famous video games, like *Grand Theft Auto* and *Fallout New Vegas*.

![](https://github.com/pauladj/nlp-cyberpunk-2077-reviews/raw/master/img/trigram.png)


## What do people say about ...?

We know the most common words and the bi/trigrams but we still don't know what they're saying about them. To answer this question, I will use the Word2Vec model and see which are the words that are most likely to appear around our target word. We are going to use the Bag-of-Words (CBOW) architecture because it's faster. We also have to specify the number of epochs to improve the word representation.

```python
from gensim.models import Word2Vec

good_token_clean = []
# list of list of tokens [["this", "is", "one", "sentence"], ["another", "one"],..]
for r in df.text_clean.values.tolist():
    good_token_clean.append(str(r).split())
    
# Train the word2vec with 25 epochs
model = Word2Vec(min_count = 3) #cbow
model.build_vocab(good_token_clean)
model.train(good_token_clean, total_examples = model.corpus_count, epochs = 25)    
```

Now we can see what the users are saying about some of the most frequent words:

![](https://github.com/pauladj/nlp-cyberpunk-2077-reviews/raw/master/img/w2v.jpg)

## 🧐 Insights

- The story seems to be compelling, amazing but short.
- The gameplay seems to be nothing new to some and enjoyable to others. 
- There are some graphical glitches and bugs. Some are minor but others may be major or game-breaking. Some are even funny?
- They talk a lot about the characters' customization, personality, and memorableness.
- Combat, hacking, and gunplay seem to be fun.
- The world is detailed and vibrant. The visuals are also gorgeous and visually stunning.
- Maybe the driving system is not good.


Riley MacLeod talks about some of the things discovered with this NLP analysis in [his review](https://kotaku.com/cyberpunk-2077-the-kotaku-review-1845946628).

> Its post-release life has been about the game’s **poor performance** on consoles, so rife with bugs and crashes that CDPR offered refunds.

> The doors on one side of the factory were **glitched** (unintentionally, a problem with the game code), (...) I couldn’t pass through them without falling to my death.

> I got a vehicle for my trouble, **drove** it politely out of the factory, and have yet to drive it again because of how badly it handles

> I can work around the technical failings and **laugh** at or even admire the **bugs**. It’s only crashed once, hilariously, when another car hit me so hard the whole game mysteriously shut down. 

> Much of my time in the game has been spent just driving for miles, **admiring** how naturally a busy commercial hub becomes an imposing corporate center becomes a run-down residential neighborhood becomes abandoned outskirts

> I liked exploring Night City, excellent lore and world-building, some interesting **characters**


## 🎉 Acknowledgements 

- Steam: https://store.steampowered.com/
- Image mask: https://www.hiclipart.com/free-transparent-background-png-clipart-xlukq
- Download steam reviews: https://github.com/woctezuma/download-steam-reviews

