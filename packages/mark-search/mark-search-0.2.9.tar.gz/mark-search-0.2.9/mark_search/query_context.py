class QueryContext(object):
    def __init__(self, index):
        self.index = index
        self.setting = None
        self.filter_ids = None
        self.not_filter_ids = None
    
    def setSetting(self, setting):
        self.setting = setting

