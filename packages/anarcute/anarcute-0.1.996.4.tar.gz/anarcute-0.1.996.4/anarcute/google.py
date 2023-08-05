import hy.macros
import requests
from anarcute import *

hy.macros.require('anarcute.lib', None, assignments='ALL', prefix='')


class GT(object):
    """Google translate"""

    def __init__(self, key):
        self.key = key
        self.api = 'https://translation.googleapis.com/language/translate/v2'
        return None

    def translate(self, source, target, q, format='text', model=None):
        params = {'key': self.key, 'q': q, 'source':
            source, 'target': target, 'format': format, 'model': model}
        return requests.get(self.api, params).json()


class GS(object):
    """Google Custom Search Engine"""

    def __init__(self, cx, key):
        self.api = 'https://www.googleapis.com/customsearch/v1/siterestrict'
        self.cx = cx
        self.key = key

    # start = number of first item
    # by default it returns search result with 10 searches
    def search(self, q, follow=True, TIMEOUT=10, start=1):
        params = {'q': q, 'cx': self.cx, 'key':
            self.key, 'start': start}
        res = requests.get(self.api, params=params, timeout=TIMEOUT).json()

        if (not 'items' in res
                and follow
                and 'spelling' in res
                and 'correctedQuery' in res['spelling']):
            corrected = res['spelling']['correctedQuery']
            print('REDIRECT from', q, 'to', corrected)
            return self.search(corrected, follow=True, start=start, TIMEOUT=TIMEOUT)
        else:
            return res

    # start = number of first item
    # end = number of last item
    # by default Google will return 100 items
    def items(self, q, start=1, end=None):
        r = self.search(q, start=start)
        try:
            items = r['items']
        except Exception:
            items = []
        if 'queries' in r and 'nextPage' in r['queries'] \
                and r['queries']['nextPage'] \
                and (not end or end < len(items)):
            return items + self.items(q, start=r['queries']['nextPage'][0][
                'startIndex'])
        else:
            return items


if __name__ == "__main__":
    __key__ = "#####"
    __cx__ = "########"
    gt = GT(__key__)
    print(gt.translate("en", "ru", "eat those pancakes and drink tea"))

    gs = GS(__cx__, __key__)
    print(gs.search("barbie"))
