from flask import Flask, jsonify
from flask_cors import CORS
import random
import nltk
from nltk.corpus import wordnet as wn

app = Flask(__name__)
CORS(app)

def get_random_word():
    # Get a list of all synsets in WordNet
    all_synsets = list(wn.all_synsets())
    
    while True:
            random_synset = random.choice(all_synsets)

            random_word = random.choice(random_synset.lemmas()).name()

            if '_' not in random_word and random_word.isalpha():
                return random_word


@app.route('/api/word/<word>', methods=['GET'])
def get_word_synsets(word):
    try:
        synsets = wn.synsets(word)
        results = []
        
        for synset in synsets:
            results.append({
                "name": synset.name(),
                "definition": synset.definition(),
                "examples": synset.examples(),
                "lemmas": [lemma.name() for lemma in synset.lemmas()]
            })
        
        return jsonify(results)
    except Exception as e:
        print (f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/similarity/<word1>/<word2>', methods=['GET'])
def get_similarity(word1, word2):
    try:
        # retrieve synsets for each word from the API
        synsets1 = wn.synsets(word1)
        synsets2 = wn.synsets(word2)
        
        if not synsets1 or not synsets2:
            return jsonify({"error": "No synsets found for one or both words"}), 400
        
        max_similarity = 0
        for synset1 in synsets1:
            for synset2 in synsets2:
                similarity = synset1.wup_similarity(synset2) or 0
                if similarity > max_similarity:
                    max_similarity = similarity
        
        return jsonify({"similarity": max_similarity})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/random-word', methods=['GET'])
def random_word():
    word = get_random_word()
    return jsonify({"targetWord": word})


if __name__ == '__main__':
    app.run(debug=True)
