class UrlManager(object):
    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticurl(path):
        path = path + "?ver=" + "201805021500"
        return UrlManager.buildUrl(path)