from abc import ABC, abstractmethod


class WordsProvider(ABC):

    @abstractmethod
    def retrieve_words(self):
        pass
