import requests
import textacy
import spacy


NEWSAPI_KEY = "0797893c0ac04d8bbd4e89d43cb27539"
TEXTS = None


def get_claims(term=None, limit=100):
    print("getting articles...")
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "sortBy": "popularity",
        "language": "en",
        "country": "gb",
        "category": "business",
        "apiKey": NEWSAPI_KEY
    }
    if term is not None:
        params["q"] = term
    print(params)
    resp = requests.get(base_url, params=params)
    results = resp.json()
    try:
        articles = results["articles"]
    except KeyError:
        print(resp.json())
        return []
    for article in articles[:limit]:
        yield article["title"]
        yield article["description"]
        yield article["content"]


def main_textacy():
    # Make sure to download an English language model with
    # `python -m spacy download en_core_web_sm`
    en = textacy.load_spacy("en_core_web_sm")

    for text in TEXTS:
        doc = textacy.Doc(text, lang=en)
        triples = textacy.extract.subject_verb_object_triples(doc)
        if triples:
            print("original text:")
            print(text)
            print("subject, verb, object:")
            for subject, verb, obj in triples:
                print("s: '{}', v: '{}', o: '{}'".format(subject, verb, obj))
            print("")


def main_spacy():
    nlp = spacy.load("en_core_web_sm")
    for text in TEXTS:
        print("original text:")
        print("  ", text)
        doc = nlp(text)

        for sent in doc.sents:
            subjects = [w for w in sent if w.dep_ == "nsubj"]
            for subj in subjects:
                print("subject: {}".format(subj))
                print("lefts: {}".format(list(subj.lefts)))


if __name__ == "__main__":
    # with open("texts.txt") as f:
    #     TEXTS = f.read().split("\n")
    TEXTS = get_claims()

    # main = main_textacy
    main = main_spacy
    main()
