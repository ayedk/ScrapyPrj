from pathlib import Path
import scrapy 
import re
from operator import itemgetter 
from scrapy.exceptions import CloseSpider
import json 

import os

class ExamLinksSpider(scrapy.Spider):
    name = "ExamLinks"
    page_number = 1
    ExamName=''
    PagesNumber=0
    LinksList=[]
    base_url = "https://www.examtopics.com"
    
    """custom_settings = {
       'CONCURRENT_REQUESTS': 1,
    }"""


         
    def start_requests(self):
        self.ExamName=getattr(self,'Exam')
        self.PagesNumber=getattr(self,'PagesNumber')
        for i in range(1,int(self.PagesNumber)+1):
            yield scrapy.Request(str(self.base_url)+'/discussions/microsoft/'+str(i),callback = self.parse)

    def parse(self, response):  
        
        for  exams in response.css("a.discussion-link"):
                if (self.ExamName in exams.attrib["href"]): 
                    self.LinksList.append(
                        {
                            "Topic": int(re.findall(r'\d+', str(exams.attrib["href"]))[2]),
                            "Question": int(re.findall(r'\d+', str(exams.attrib["href"]))[3]),
                            "Url": self.base_url +str(exams.attrib["href"])
                        }
                        ) 
        
        if int(self.PagesNumber)==self.page_number: 
            LinksFile = '..\Exams\\'+str(self.ExamName).upper()+'\Links\LinksFor_'+self.ExamName+'.json'
            os.makedirs(os.path.dirname(LinksFile), exist_ok=True)
            with open(LinksFile, 'w+', encoding="utf-8") as FLink:
                self.LinksList = sorted(self.LinksList, key=itemgetter('Topic','Question')) 
                json.dump(self.LinksList, FLink) 
            raise CloseSpider("END oF Links"); 
        self.page_number+=1
        
        """self.page_number += 1
        if self.page_number == 100: 
            LinksFile = '..\Exams\\'+str(self.ExamName).upper()+'\Links\LinksFor_'+self.ExamName+'.json'
            os.makedirs(os.path.dirname(LinksFile), exist_ok=True)
            with open(LinksFile, 'w+', encoding="utf-8") as FLink:
                self.LinksList = sorted(self.LinksList, key=itemgetter('Topic','Question')) 
                json.dump(self.LinksList, FLink) 
            raise CloseSpider("END oF Links"); """
        
        
        """next_page = str(self.base_url)+'/discussions/microsoft/' + str(self.page_number)
        yield scrapy.Request(next_page, callback=self.parse)"""
 
#cd "C:\Users\ayed.klila\OneDrive - CED Cloud\Bureaublad\ScrapyProjects\ExamLinks" | scrapy crawl ExamLinks -a Exam="dp-300" -a PagesNumber=1400  
#cd "C:\Users\ayed.klila\OneDrive - CED Cloud\Bureaublad\ScrapyProjects\ExamQuestions" | scrapy crawl ExamQuestions -a Exam="dp-300" -a BatchSize=50