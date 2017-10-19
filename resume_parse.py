# -*- coding: utf-8 -*-
import textract, pdb, re, csv
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
        read_skill = open('skills_list_source', 'r').read()
        self.skill_list = read_skill.split('#')
        read_education = open('educations', 'r').read()
        self.education_list = read_education.split('#')     
        read_company = open('company_list', 'r').read()
        self.company_list = read_company.split(',')     
    
    def StanfordNER(self, text):
        st = StanfordNERTagger('/home/ubuntu/Documents/nltk_data/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz','/home/ubuntu/Documents/nltk_data/stanford-ner-2014-06-16/stanford-ner.jar',  encoding='utf-8')
        tokenized_text = word_tokenize(text)
        res = st.tag(tokenized_text)
        # print res
        # pdb.set_trace()
        for val in res:
            if val[1].lower() == 'person':
                print "Name : ", val[0]            
            elif val[1].lower() == 'organization':
                print "organization : ", val[0]        
    
    def name_extractor(self, text):
        skip_words = ['curriculum', 'vitae', 'resume']
        text_lines = text.split('\n')
        name = ''
        # pdb.set_trace()
        
        for line in text_lines[:4]:
            if line:
                line_words = set(line.lower().split(' '))
                if not line_words.intersection(skip_words):
                    return line
        return ''
    
    def get_skill(self, text):
        # read_skill = 
        skill_present = []
        for skill in self.skill_list:
            if  skill.lower()+ ' ' in text or skill.lower()+ ',' in text:
                skill_present.append(skill)        
        return list(set(skill_present))   

    def get_education(self, text):
        # read_skill = 
        degree_present = []
        for degree in self.education_list:
            if  degree.lower()+ ' ' in text or degree.lower()+ ',' in text or degree in text:
               degree_present.append(degree)        
        return list(set(degree_present))   

    def get_company(self, text):
        # read_skill = 
        company_present = []
        for comp in self.company_list:
            if  comp.lower()+ ' ' in text or comp.lower()+ ',' in text:
               company_present.append(comp)        
        return list(set(company_present))  

    def getPhone(self, text):
        mobile = re.findall(r'(?:\+?\d{2}[ -]?)?\d{10}', text)
        return mobile
    
    def getEmail(self, text):
        # pdb.set_trace()
        res = re.findall(r'[\w\.-]+@[\w\.-]+',text,re.I) 
        return list(set(res))
    
    def getUrls(self, text):
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        return urls 
    
    def fileReader(self):
        res = {}
        file_name = raw_input("\nEnter file name: ")
        res['file_name'] = file_name
        text = textract.process(file_name)
        # print "\nOrganizations and name using Stanford NER"
        # SF_name = self.StanfordNER(text.lower())
        RB_name = self.name_extractor(text.lower())
        res['RB_name'] = RB_name
        mb_number = self.getPhone(text.lower())
        res['mb_number'] = mb_number
        email = self.getEmail(text.lower())
        res['email'] = email
        candidate_skills = self.get_skill(text.lower())
        res['candidate_skills'] = candidate_skills
        candidate_education = self.get_education(text)
        res['candidate_education'] = candidate_education
        candidate_company = self.get_company(text.lower())
        res['candidate_company'] = candidate_company
        urls_list = self.getUrls(text.lower())
        res['urls_list'] = urls_list
        print res
        with open('result.csv', 'a') as csvfile:
            fieldnames = res.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(res)
        

if __name__ == '__main__':
    while True:
        ResumeParser().fileReader()
    