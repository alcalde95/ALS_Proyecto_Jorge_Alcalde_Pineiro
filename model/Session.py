class Session:
    def __init__(self, class_id,date,instructor):
        self.__class_id = class_id
        self.__date = date
        self.__instructor = instructor
    @property
    def class_id(self):
        return self.__class_id
    @property
    def date(self):
        return self.__date
    @property
    def instructor(self):
        return self.__instructor