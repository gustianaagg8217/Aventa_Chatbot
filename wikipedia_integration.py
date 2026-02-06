import requests

class WikipediaSearcher:
    def __init__(self):
        self.user_agent = 'AventaChatbot/1.0'
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})

    def search(self, query):
        response = self.session.get('https://en.wikipedia.org/w/api.php', params={
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json'
        })
        return response.json()

class QuestionAnswerer:
    def __init__(self):
        self.fallback_data = {
            'what is your name?': 'I am Aventa, your chatbot assistant.',
            'how can I contact support?': 'You can contact support at support@example.com.'
        }

    def answer_question(self, question):
        return self.fallback_data.get(question.lower(), 'I am sorry, I do not know the answer to that question.')

class KnowledgeBase:
    def __init__(self):
        self.knowledge = {}

    def add_entry(self, topic, information):
        self.knowledge[topic] = information

    def get_information(self, topic):
        return self.knowledge.get(topic, 'No information found.')
