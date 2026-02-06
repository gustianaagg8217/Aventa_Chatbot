import requests
import time
import json

class WikipediaSearcher:
    def __init__(self, language='en', user_agent=None):
        self.language = language
        self.user_agent = user_agent if user_agent else 'Mozilla/5.0'
        self.cache = {}

    def search(self, query):
        if query in self.cache:
            return self.cache[query]
        
        headers = {'User-Agent': self.user_agent}
        url = f'https://{self.language}.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json'
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            self.cache[query] = data
            return data
        else:
            return {'error': 'Failed to fetch data from Wikipedia'}

class QuestionAnswerer:
    def __init__(self, searcher):
        self.searcher = searcher
    
    def answer_question(self, question):
        search_results = self.searcher.search(question)
        # Process search results to find an answer
        # For simplicity, we'll return the raw results
        return search_results

class KnowledgeBase:
    def __init__(self):
        self.knowledge = {}

    def add_knowledge(self, topic, data):
        self.knowledge[topic] = data

    def get_knowledge(self, topic):
        return self.knowledge.get(topic, 'No knowledge available on that topic.')

# Example usage
if __name__ == '__main__':
    searcher = WikipediaSearcher()
    answerer = QuestionAnswerer(searcher)
    
    question = "What is machine learning?"
    answer = answerer.answer_question(question)
    print(answer)
