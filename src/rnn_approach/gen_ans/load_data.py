import nltk

def load_ip(path):
    with open(path) as f:
        data = f.readlines()

    dataset = []
    for line in data:
        tokens = nltk.word_tokenize(line[:-1])
        tokens = [token.lower() for token in tokens]
        tokens.append("<EOS>")
        dataset.append(tokens)

    for _ in range(5):
        dataset.extend(dataset)

    return dataset

def load_labels(path):
    with open(path) as f:
        data = f.readlines()

    dataset = []
    for line in data:
        tokens = nltk.word_tokenize(line[:-1])
        tokens = [token.lower() for token in tokens]
        tokens = ["<START>"] + tokens + ["<EOS>"]
        dataset.append(tokens)

    for _ in range(5):
        dataset.extend(dataset)

    return dataset