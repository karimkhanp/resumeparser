# -*- coding: utf-8 -*-
import textract, pdb, re, csv, os, json
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from datetime import date
from work_experience import WorkExperience

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
        read_designation = open('designation.txt', 'r').read()
        self.designation_list = read_designation.split('#')
        read_certificate = open('certification.txt', 'r').read()
        self.certificate_list = read_certificate.split('#')
    
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
    
    def get_certificate(self, text):
        # read_skill = 
        certificate_present = []
        for certificate in self.certificate_list:
            if  certificate+ ' ' in text or certificate+ ',' in text:
               certificate_present.append(certificate)        
        return list(set(certificate_present))  

    def get_designation(self, text):
        # read_skill = 
        designation_present = []
        for designation in self.designation_list:
            if  designation.lower()+ ' ' in text or designation.lower()+ ',' in text:
               designation_present.append(designation)        
        return list(set(designation_present))
    
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
    
    def get_passingyear(self, text, education):
        # pdb.set_trace()
        text_lines = text.splitlines()
        passing_year = []
        for line in text_lines:
            for degree in education:
                # pdb.set_trace()
                if degree.lower().strip() in line:
                    year = re.findall('((?:19|20)\d\d)', line)
                    p_year = {}
                    if len(year) > 1:
                        year = '-'.join(year)
                        p_year[degree]= year
                        passing_year.append(p_year)
                        break
                    elif len(year) == 1:
                        p_year[degree]= year
                        passing_year.append(p_year)
                        break
        return passing_year
    def fileReader(self):
        res = {}
        result_list = []
        #one can give path of any  target direcory here
        cwd = os.getcwd()
        count = 0
        try:
            os.remove(result.csv)
        except:
            pass
        for filename in os.listdir(cwd):
            if filename.endswith(".docx") or filename.endswith(".pdf") or filename.endswith(".doc"):
                try:
                    print
                    print "filename: ", filename
                    count += 1
                    print "count: ", count
                    res['file_name'] = filename
                    text = textract.process(filename)
                    work_experience_obj = WorkExperience(text.lower())
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
                    candidate_designation = self.get_designation(text.lower())
                    res['candidate_designation'] = candidate_designation
                    certificate_list = self.get_certificate(text.lower())
                    res['certificate_list'] = certificate_list
                    passing_year = self.get_passingyear(text.lower(), candidate_education)
                    res['passing_year'] = passing_year
                    print res['passing_year']
                    res['work_experience'] = work_experience_obj.get_work()    
                    result_list.append(res)
                    with open('result.csv', 'a') as csvfile:
                        fieldnames = res.keys()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        # writer.writeheader()
                        writer.writerow(res)
                except Exception:
                    # print "---**---Error in File Name: ", filename
                    # raw_input("Press any key to continue....")
                    continue
        with open('result.json', 'w') as fp:
            json.dump(result_list, fp)

if __name__ == '__main__':
    ResumeParser().fileReader()
    