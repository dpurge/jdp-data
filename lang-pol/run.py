# -*- coding: utf-8 -*-
"""

"""
import sys
import argparse
import config

from spylls.hunspell import Dictionary
from helper import *
from pathlib import Path
from io import StringIO

def main(input, output):
    
    input_folder = Path(input)
    output_folder = Path(output)
    
    if not input_folder.is_dir():
        raise Exception(f"Input folder does not exist: {input_folder}")
    
    if not output_folder.is_dir():
        output_folder.mkdir(parents=True)

    hunspell = Dictionary.from_files(str(config.data_folder / 'pl_PL'))
    alphabet = hunspell.aff.TRY
    
    input_files = list(input_folder.rglob('*.txt'))
    output_files = list([output_folder / i.name for i in input_files])
    work_data = zip(input_files, output_files)
    
    for (_, (input_file, output_file)) in enumerate(work_data):
        print(f"{input_file.relative_to(config.root_folder)} -> {output_file.relative_to(config.root_folder)}")
        
        text = input_file.read_text(encoding='utf-8')
        words = set()

        for form in get_word_forms(text=text, alphabet=alphabet):
            entry = next(hunspell.lookuper.good_forms(form))
            if entry.in_dictionary:
                words.add(entry.stem)
            else:
                words.add(form)

        vocabulary = get_vocabulary(words=words)
        
        report = StringIO()
        
        report.write("# Vocabulary\n\n")
        report.write(vocabulary)
        
        output_file.write_text(data=report.getvalue(), encoding='utf-8')

    return 0


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', 
        help='Input folder', default=config.input_folder)
    parser.add_argument('-o', '--output', 
        help='Output folder', default=config.output_folder)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_arguments()
    try:
        sys.exit(main(input=args.input, output=args.output))
    except Exception as exc:
        print(exc, file=sys.stderr, end="\n")
        sys.exit(1)