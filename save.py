class SaveCollector:
    def __init__(self):
        self.__savers = []

    def add_saver(self, saver):
        self.__savers.append(saver)

    def save(self):
        for saver in self.__savers:
            saver.save()