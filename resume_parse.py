# -*- coding: utf-8 -*-
import textract, pdb, re
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

'''
    This code read CVs in docs and pdf format and extract various required fields
'''
class ResumeParser(object):
    '''
        This fucntion contains all Global parameters
    '''
    def __init__(self):
        pass
    
    def StanfordNER(self, text):
        st = StanfordNERTagger('/home/ubuntu/Documents/nltk_data/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','/home/ubuntu/Documents/nltk_data/stanford-ner-2014-06-16/stanford-ner.jar',  encoding='utf-8')
        tokenized_text = word_tokenize(text)
        res = st.tag(tokenized_text)
        # print res
        for val in res:
            if val[1].lower() == 'person':
                print "Name : ", val[0]            
            elif val[1].lower() == 'organization':
                print "organization : ", val[0]        
    
    def name_extractor(self, text):
        skip_words = ['CURRICULUM', 'VITAE', 'resume']
        text_lines = text.split('\n')
        name = ''
        # pdb.set_trace()
        for  i in range(0,4):
            if text_lines[i]:
                for word in skip_words:
                    if word.lower() not in text_lines[i]:
                        name = text.split('\n')[i]
                        # print name
                        return name         
        return name
    
    def getPhone(self, text):
        mobile = re.findall(r'(?:\+?\d{2}[ -]?)?\d{10}', text)
        return mobile
    
    
    def fileReader(self):
        file_name = raw_input("\nEnter file name: ")
        text = textract.process(file_name)
        print "\nOrganizations and name using Stanford NER"
        st_name = self.StanfordNER(text.lower())
        print st_name
        print "\n\nName using rule based approach"
        rl_name = self.name_extractor(text.lower())
        print rl_name
        print "\n\nMobile number:"
        mb_number = self.getPhone(text.lower())
        print mb_number

if __name__ == '__main__':
    while True:
        ResumeParser().fileReader()
    