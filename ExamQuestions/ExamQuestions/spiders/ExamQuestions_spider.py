from pathlib import Path
import scrapy
from bs4 import BeautifulSoup 
from operator import itemgetter  
import json 
import os


class ExamQuestionsSpider(scrapy.Spider):
    name = "ExamQuestions" 
    LinksList=[]
    LinkNumber = 1  
    BatchSize=30
    ExamName=''
    FileNumber=0
    baseHtml = """
    <!DOCTYPE html>
    <html lang="en" >     
            <link rel="stylesheet" type="text/css" href="https://www.examtopics.com/assets/css/bootstrap.min.css">
            <link rel="stylesheet" type="text/css" defhref="https://www.examtopics.com/assets/css/slick.css" href="https://www.examtopics.com/assets/css/slick.css">
            <link rel="stylesheet" type="text/css" href="https://www.examtopics.com/assets/css/style.css?ver=1">
            <link rel="stylesheet" type="text/css" href="https://www.examtopics.com/assets/css/color/default.css">
            <link rel="stylesheet" type="text/css" href="https://www.examtopics.com/assets/css/responsive.css">
			<link rel="stylesheet" type="text/css" href="https://www.examtopics.com/assets/css/forum.css">   
    <body>
	    <!-- jquery latest version -->
		<script src="https://www.examtopics.com//assets/js/jquery.min.js"></script>
		<script type="text/javascript" src="https://www.examtopics.com/assets/js/examview.js?ver=4"></script>
        <div class="sec-spacer pt-50">
	        <div class="container">
	        <!-- BEGIN Discussion Content -->
		        <div class="row">
			        <div >
    """
    
    HtmlTags=[]
    
        
    custom_settings = {
       'CONCURRENT_REQUESTS': 1,
    }
     
    def start_requests(self): 
        self.ExamName=getattr(self,'Exam')
        self.BatchSize=getattr(self,'BatchSize')
        
        LinksFile = '..\\Exams\\'+str(self.ExamName).upper()+'\\Links\\LinksFor_'+self.ExamName+'.json' 
        with open(LinksFile) as json_file :
            self.LinksList = json.load(json_file)
            self.LinksList = sorted(self.LinksList, key=itemgetter('Topic','Question')) 
            for link in self.LinksList:
                yield scrapy.Request(link["Url"],callback = self.parse)
    
    def parse(self, response):
        
        
        soup = BeautifulSoup(response.body, 'html.parser')  
        discussion = soup.find_all("div", class_="discussion-header-container")
        self.HtmlTags.append(
                    '<a href="'
                   +response.url
                   +'" class="discussion-link" target="_blank" rel="noopener noreferrer"> Click Me '
                   +response.url
                   +'</a>'
                   +str(discussion).replace('/assets/media/exam-media','https://www.examtopics.com/assets/media/exam-media')
                   ) 
        if ((self.LinkNumber % int(self.BatchSize) ==0 ) and (self.LinkNumber / int(self.BatchSize)>0)) or (int(len(self.LinksList))==int(self.LinkNumber)):
            
            self.FileNumber+=1
            HtmlFile =  '..\\Exams\\'+str(self.ExamName).upper()+'\\HtmlFiles\\'+str(self.ExamName).upper()+'_QuestionsList_'+str(self.FileNumber)+'.html'
            os.makedirs(os.path.dirname(HtmlFile), exist_ok=True)
            with open(HtmlFile, 'w+', encoding="utf-8") as f:
                print(self.baseHtml ,file=f)
                for tag in self.HtmlTags:
                    print(str(tag),file=f)
                self.HtmlTags.clear()
                
             
        self.LinkNumber += 1
    
 
