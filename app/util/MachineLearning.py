from conf import settings

class MachineLearning:
    
    def create_stopwords(self, country: str) -> list:
        stopwords = []
        with open(settings.DIR_PATH_STOPWORDS + country) as file:
            for stopword in file.read().splitlines():
                stopwords.append(stopword)
        return stopwords
