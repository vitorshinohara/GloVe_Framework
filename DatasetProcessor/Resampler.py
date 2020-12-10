import json
import csv
import random

from tqdm import tqdm
from DatasetOptions.dataset_options import DatasetOptions

def _write(file, string):
    file.write(string + '\n')

def _concantenate_data_str(data, separator):
    _str = ''
    for item in data:
        _str += str(item) + ';'

    return _str[:-1]

def shuffle_words(text):
    words = text.split()
    random.shuffle(words)
    return ' '.join(words)

def main(opt):

    remaining_entries = {
        '1.0': int(opt.amount),
        '2.0': int(opt.amount),
        '3.0': int(opt.amount),
        '4.0': int(opt.amount),
        '5.0': int(opt.amount)
    }

    with open(opt.input, 'r') as input_file:
        input_lines = input_file.readlines()

    # Clear output file
    _ = open(opt.output, 'w')

    with open(opt.output, 'a') as output_file:

        for line in tqdm(input_lines):
            line_dict = json.loads(line)

            line_dict[u'shuffled'] = str(shuffle_words(line_dict['reviewText']))

            if opt.amount == 'max' or remaining_entries[str(line_dict['overall'])] > 0:

                _write(output_file, json.dumps(line_dict))
                remaining_entries[str(line_dict['overall'])] -= 1


if __name__ == "__main__":
    opt = DatasetOptions().get_parser().parse_args()

    main(opt)
