# -*- coding: iso-8859-1 -*-
import logging
import sys
import time
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException
from kalliope.neurons.say.say import Say
from kalliope.core import Utils

import requests
from html.parser import HTMLParser

reload(sys)
sys.setdefaultencoding('utf-8')


logging.basicConfig()
logger = logging.getLogger("kalliope")

# Code on https://github.com/Areeb-M/GoogleAnswers
    
class Ask_google(NeuronModule):
    def __init__(self, **kwargs):
        super(Ask_google, self).__init__(**kwargs)
        # the args from the neuron configuration
        self.question = kwargs.get('question', None)

        # check if parameters have been provided
        if self._is_parameters_ok():
            class Target:
                def __init__(self, elements):
                    self.elements = elements

                def check_path(self, path):
                    length = len(self.elements)
                    for i in range(length):
                        index = -length + i
                        if path[index][0] == self.elements[index][0] and (path[index][1] == self.elements[index][1] or self.elements[index][1] == ''):
                            continue
                        else:
                            return False
                    return True
                    
            self.TARGET_LIST = [
                                        Target([['div', 'class="Z0LcW"']]),  # Enables Featured Snippet Scraping
                                        Target([['span', 'class="Y0NH2b CLPzrc"']]),  # Enables Featured Snippet Scraping
                                        Target([['span', 'class="ILfuVd yZ8quc"']]),  # Enables Featured Snippet Scraping
                                        Target([['span', 'class="_Tgc"']]),  # Enables Featured Snippet Description Scraping
                                        Target([['span', 'class="cwcot" id="cwos"']]),  # Enables Calculator Answer Scraping
                                        Target([['div', 'class="vk_bk dDoNo"']])  # Enable Time Scraping
                                        ]

            self.HEADER_PAYLOAD = {  # Enables requests.get() to See the Same Web Page a Browser Does.
                                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                                                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                                                }
            class Parser(HTMLParser):
                def __init__(self, target):
                    HTMLParser.__init__(self)
                    self.target = target
                    self.target_depth = 0
                    self.path = []
                    self.occurrences = []

                def handle_starttag(self, tag, attributes):
                    attr_string = ""
                    for attribute in attributes:
                        attr_string += attribute[0] + '="' + attribute[1] + '" '
                    attr_string = attr_string[:-1]

                    self.path.append([tag, attr_string])
                    if self.target_depth > 0 or self.target.check_path(self.path):
                        if self.target_depth == 0:
                            self.occurrences.append('')
                        self.target_depth += 1

                def handle_endtag(self, tag):
                    self.path.pop()
                    if self.target_depth > 0:
                        self.target_depth -= 1

                def handle_data(self, data):
                    if self.target_depth > 0:
                        self.occurrences[-1] += data

                def feed(self, data):
                    HTMLParser.feed(self, data)
                    return self.occurrences

            
            def scrape(url):
                data = requests.get(url, headers=self.HEADER_PAYLOAD).text
                start_js = data.index('/g-section-with-header')
                data = data[0:start_js]
                #f = open("google.html", "w")
                #f.write(data)
                #f.close
                results = []

                for target in self.TARGET_LIST:
                    results += Parser(target).feed(data)

                return results

            def GetAnswer(query, scraper_results):
                if len(scraper_results) > 0:
                    for i in range(len(scraper_results)):
                        answer = scraper_results[i].replace('  ', ' ')
                        answer = ({"answer_found": answer})
                else:
                    answer = ({"answer_not_found": query})
                logger.info(answer)
                self.say(answer)


            def ask(query):
                url = convert_query(query)
                result = GetAnswer(query, scrape(url))
                return result

            def convert_query(query):
                result = query
                result = result.replace(' ', '+')
                result = result.replace('?', '')
                result = "http://www.google.com/search?q=" + result
                return result

            ask(self.question)
            
            


    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.question is None:
            raise MissingParameterException("You have to ask a question.") 

        return True
       
