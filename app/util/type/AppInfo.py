
class AppInfo:
    def __init__(self) -> None:
        self.name = None
        self.icon_id = None
        self.release_datetime = None
        self.download_price = None
        self.file_size = None
        self.annual_sales = None
        self.download_count = None
        self.wau_count = None
        self.description = None
        self.billings = None
        self.keyword_ranking = None
        self.wau_nationality_ranking = None
        
        self.co_occurrence_network_result = {'1': self.__init_machine_learning_result_dict(),
                                             '2': self.__init_machine_learning_result_dict(),
                                             '3': self.__init_machine_learning_result_dict()}
        self.bag_of_words_result = {'1': self.__init_machine_learning_result_dict(),
                                    '2': self.__init_machine_learning_result_dict(),
                                    '3': self.__init_machine_learning_result_dict()}
        self.sunburst_chart_result_1_good = {'1': self.__init_machine_learning_result_dict(),
                                             '2': self.__init_machine_learning_result_dict(),
                                             '3': self.__init_machine_learning_result_dict()}

    def __init_machine_learning_result_dict(self):
        return {'good': None, 'normal': None, 'bad': None}