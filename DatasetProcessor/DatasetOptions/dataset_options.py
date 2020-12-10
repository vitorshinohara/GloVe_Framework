import argparse

class DatasetOptions:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--input', type=str, required=True, help='Input data path.')
        self.parser.add_argument('--output', type=str, required=True, help='Output csv file that features will be stored')
        self.parser.add_argument('--separator', type=str, default=';', help='Character that separates the different columns.')
        self.parser.add_argument('--amount', type=str, default='max', help='Number of rows that will be outputed.')

    def get_parser(self):
        return self.parser
