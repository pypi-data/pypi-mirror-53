from quorapy.scraper import Scraper
import os


class Quora:
    def __init__(self, browser):
        self.BASE_URL = "https://quora.com"
        self.browser = browser

    def search(self, keyword, question_limit=None, answer_limit=None, load_user_data=False):
        question_limit = int(question_limit) if question_limit else None
        answer_limit = int(answer_limit) if answer_limit else None

        # Browser Actions
        b = self.browser
        b.get_home()
        if b.login(os.getenv('QR_EMAIL'), os.getenv('QR_PASSWORD') == False):
            return {'error': 'Login failed'}
        b.search_by(keyword)
        b.infinite_scroll(question_limit)
        our_urls = b.get_urls()

        # Scraper Actions
        all_data = {}
        all_data['question_limit'] = question_limit
        all_data['answer_limit'] = answer_limit
        all_data['load_user'] = load_user_data
        all_data['query'] = keyword
        all_data['data'] = []

        count = 0
        for url in our_urls:
            datum = {}
            datum['url'] = url
            datum['question'] = {}
            datum['comments'] = []
            if question_limit and count >= question_limit:
                break
            count = count + 1

            b.get_url(url)
            datum['question']['text'] = b.get_title()
            b.infinite_scroll(answer_limit)
            dat = b.get_comments(answer_limit)
            for d in dat:
                datum['comments'].append(d)

            b.get_url(url+'/log')
            b.infinite_scroll()
            u = Scraper(html=b.get_source())
            # data['text'] = u.get_details()
            data = u.get_details()
            if 'url' in data['user'] and load_user_data:
                b.get_url(data['user']['url'])
                v = Scraper(html=b.get_source())
                data['user']['followers'] = v.get_followers()

            datum['question']['user'] = data['user']
            datum['question']['datetime'] = data['datetime']
            all_data['data'].append(datum)
        return all_data
