# Tek Innovators: Profanity Filter

## Context
This project is similar to work we did at Singularity 6 for the game Palia, which is an online game on PC/Steam, Switch, Xbox, and Playstation. The game involves multiplayer coordination and communication and is still available.

We had many goals regarding profanity and toxicity:
- Prevent and reduce harm of hate speech, harassment, and any other online harm. If possible we wanted to catch those harmful behaviors automatically rather than relying solely on the moderation team
- Adhere to common practices in gaming in which profanity is bleeped out
- Adhere to various laws around children playing games TODO
- Adhere to the certification requirements of Nintendo, Microsoft, and Sony (many of which are private)

Some of the constaints of the game to consider:
- The game was worldwide. Our most commonly used languages were English, German, Spanish, Dutch, Portuguese, French, Russian, Chinese, Japanese, and Hungarian (if I remember correctly).
- English profanity was frequently used in other languages
- Chat was shared between all players on a given server and would mix players from different languages.
- We had to process about 1,000,000 messages per day and the messages were just plain text.

User experience considerations:
- Players shouldn't be allowed to create offensive usernames, and it should be clear why. For example, if a username like "cass" is blocked for profanity that can be confusing if it's not explained that it's because of "ass"
- The convention is to star out bad words in chat. This is helpful if the filter flags something incorrectly, as in ***essment.
- People in games often try to circumvent filters in creative ways by using deliberate misspellings or uncommon Unicode characters.

## This project
This project is to approximate what we needed for Palia, but in a few different levels. Write it in Python. You can use Jupyter notebooks as needed but the majority of your code should be in CLI scripts.

### Learning goals

- Build an understanding of the spectrum of solutions from rule-based solutions to traditional machine learning to applications of large language models. What are the tradeoffs involved? When does each approach shine?
- Basics of applied machine learning for text classification
- Basics of applying LLM APIs
- Get some experience with text data, unicode, etc

### Level 1: Explore some data, build a basic rule-based filter

- Download the [GameTox dataset](https://github.com/shucoll/GameTox) to the `data/` dir
- Download the [Reddit Usernames dataset](https://www.kaggle.com/datasets/colinmorris/reddit-usernames) to the `data/` dir
- Explore and understand the data, both manually and using scripts to run analysis
- Build a basic detector that identifies whether a message has English profanity in it. Implement it by building a regex from a profanity list (either a small hand-written one, or a dynamically-generated regex from a downloaded list)
- Evaluate the filter on the GameTox data, comparing against filtering nothing. Note that the GameTox data has many categories and you only want to classify text as profane or not at this level
- Review Reddit usernames that are flagged by your filter
- Try to circumvent your own filter
- Compare against any existing Python libraries: 
    - [alt-profanity-check](https://github.com/dimitrismistriotis/alt-profanity-check): An updated version of the old, abandoned profanity-check

**Definition of done**

As you work to improve your filter, over time you'll find that it's tough to block bad text without accidentally blocking good text. That's a good sign to move on.

#### To learn

- Basic regular expressions
- Gain experience with semi-documented data sets, bias in data, etc
- Gain experience with evaluation (and how it differs from unit testing or other testing). Begin to learn about evaluation metrics like accuracy

### Level 2: Build a basic LLM-based filter

- Implement an alternative filter based on an online LLM. Use [OpenRouter](https://openrouter.ai/) if you don't already have a preferred provider because they have some free LLMs
- Compare/contrast against your other solution(s)
- Compare/contrast different LLMs, such as openai/gpt-oss-20b:free, x-ai/grok-4.1-fast, meta-llama/llama-3.3-70b-instruct:free. Which is best?
- Estimate the cost for running this on 1 million messages per day with a paid model such as openai/gpt-5.1

**Extra credit**
- Build a caching layer to reduce cost and latency
- Use structured output with the LLM
- Optimize your prompt
- Experiment with multiple categories, such clean vs profanity vs insult

#### To learn
- Experience calling LLMs
- Understanding of cost and latency challenges with LLMs

### Level 3: Build a traditional text classifier

- Implement a basic scikit-learn filter based on the GameTox data. Note that you'll need to decide on a train/test split for this.
- Compare/contrast against the other options in terms of latency, memory use, external costs, and your evaluation metrics

#### Tutorials for reference

- https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html
- https://www.geeksforgeeks.org/nlp/text-classification-using-scikit-learn-in-nlp/

#### To learn

- More thorough evaluation: train/test split, precision, recall, F-score

**Extra credit**
- Use a scikit-learn pipeline to package

### Level 4: Choose your own adventure!

- Fine-tune a BERT-based model to it, like [ModernBert](https://huggingface.co/blog/modernbert)
- Compare against [toxic-bert](https://huggingface.co/unitary/toxic-bert)
- Try the same code on a different data set. See `docs/Perplexity_note.md` for some ideas
- Support languages other than English: This will be easier if you use LLMs or multilingual BERT variants BUT be careful about the data set quality if it's a language you don't know!
- Add a detector for hate speech, harassment, and other harmful behaviors (key consideration: Should our system handle curse words differently than hate speech?)
- Machine learning approaches to bleeping out profanity: You can use BERT or similar models to solve this as sequence labeling (classify each token as toxic/not). You can also use generative models like T5 to do the same.
- Fine-tune a LLM for this to get a smaller/cheaper model to work as well as a big one
- Wrap your code in a Python package that someone else could import