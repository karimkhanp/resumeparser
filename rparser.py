import nltk
from nltk.corpus import stopwords

class PhraseExtractor(object):
    
    def __init__(self):
        self.sentence_re = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'
        self.lemmatizer = nltk.WordNetLemmatizer()
        self.stemmer = nltk.stem.porter.PorterStemmer()
        self.grammar = r"""
            NBAR:
                {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
                
            NP:
                {<NBAR>}
                {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
        """
        self.stop_words = stopwords.words('english')
        
    def parser(self, text):
        chunker = nltk.RegexpParser(self.grammar)
        toks = nltk.regexp_tokenize(text, self.sentence_re)
        postoks = nltk.tag.pos_tag(toks)
        tree = chunker.parse(postoks)
        return tree

    def leaves(self, tree):
        """Finds NP (nounphrase) leaf nodes of a chunk tree."""
        for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
            yield subtree.leaves()
    
    def normalise(self, word):
        """Normalises words to lowercase and stems and lemmatizes it."""
        word = word.lower()
        # word = self.stemmer.stem_word(word) #if we consider self.stemmer then results comes with stemmed word, but in this case word will not match with comment
        word = self.lemmatizer.lemmatize(word)
        return word
    
    def acceptable_word(self, word):
        """Checks conditions for acceptable word: length, stopword. We can increase the length if we want to consider large phrase"""
        accepted = bool(2 <= len(word) <= 40
            and word.lower() not in self.stop_words)
        return accepted


    def get_terms(self, tree):
        for leaf in self.leaves(tree):
            term = [ self.normalise(w) for w,t in leaf if self.acceptable_word(w) ]
            yield term
            
    def actual_phrases(self, tree):
        lst_phrases = []
        terms = self.get_terms(tree)
        for term in terms:
            for word in term:
                lst_phrases.append(word)
        return lst_phrases
    
    def run(self, text):
        print text
        tree = self.parser(text)
        self.leaves(tree)
        lst_phrases = self.actual_phrases(tree)
        print "lst_phrases: ", lst_phrases
        return lst_phrases
            
if __name__ == '__main__':
    PhraseExtractor().run("i am feeling thristy and hunger and suffering from headache.")