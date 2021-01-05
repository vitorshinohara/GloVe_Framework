import argparse

class RunOptions():

    def __init__(self):
        """
        Define the options for feature extraction
        """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--input', type=str, required=True, help='Input data path.')
        self.parser.add_argument('--output', type=str, default='output/features.json', help='Output csv file that features will be stored')
        self.parser.add_argument('--text-column', type=str, default='Closed Captions', help='Column that contains the text which the features will be extracted.')
        self.parser.add_argument('--cores', type=int, default=4, help='Number of cores which will be used.')
        self.parser.add_argument('--glove-embedding-path', type=str, default='./Embedding/glove.6B.100d.txt', help='Path of glove embedding')
        self.parser.add_argument('--stop-words-path', type=str, default='Utils/updated_stop_words.txt', help='Stop Words file path')

    def get_parser(self):
        return self.parser
