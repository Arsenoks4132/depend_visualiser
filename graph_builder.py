from requests import get


class GraphBuilder:
    def __init__(self):
        self.xml = None
        pass

    def get_pom(self, href):
        self.xml = get(href)
        print(self.xml.text)
