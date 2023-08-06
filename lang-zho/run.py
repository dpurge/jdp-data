# -*- coding: utf-8 -*-
"""

"""
import sys
import argparse
import config

from helper import *
from pathlib import Path
from io import StringIO

def main(input, output, traditional=False):
    
    input_folder = Path(input)
    output_folder = Path(output)
    
    if not input_folder.is_dir():
        raise Exception(f"Input folder does not exist: {input_folder}")
    
    if not output_folder.is_dir():
        output_folder.mkdir(parents=True)
    
    input_files = list(input_folder.rglob('*.txt'))
    output_files = list([output_folder / i.name for i in input_files])
    work_data = zip(input_files, output_files)
    
    for (_, (input_file, output_file)) in enumerate(work_data):
        print(f"{input_file.relative_to(config.root_folder)} -> {output_file.relative_to(config.root_folder)}")
        
        text = input_file.read_text(encoding='utf-8')
        vocabulary = get_vocabulary(text=text, traditional=traditional)
        hanzi = set([ char for char in vocabulary if char > u'\u4e00' and char < u'\u9fff'])
        pinyin = get_pinyin(hanzi)
        wubi = get_ime(items=hanzi, datafile='wubi86')
        decomposition = get_decomposition(hanzi)
        # zhengma = get_ime(items=hanzi, datafile='zhengma')
        characters = merge_items(pinyin, decomposition, wubi, join_char=',')
        
        report = StringIO()
        
        #if traditional:
        #    report.write("# 《五筆字型輸入法》\n\n")
        #else:
        #    report.write("# 《五笔字型输入法》\n\n")
        #report.write(wubi + "\n")
        
        #if traditional:
        #    report.write("# 《鄭碼輸入法》\n\n")
        #else:
        #    report.write("# 《郑码输入法》\n\n")
        #report.write(zhengma + "\n")
        
        #if traditional:
        #    report.write("# 《漢語拼音》\n\n")
        #else:
        #    report.write("# 《汉语拼音》\n\n")
        #report.write(pinyin + "\n")
        
        report.write("# Characters\n\n")
        report.write(characters + "\n")
        
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
    parser.add_argument('-t', '--traditional', default=False, action='store_true',
        help='Traditional characters')
    parser.add_argument('-s', '--simplified', dest='traditional', action='store_false', 
        help='Simplified characters')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_arguments()
    try:
        sys.exit(main(input=args.input, output=args.output, traditional=args.traditional))
    except Exception as exc:
        print(exc, file=sys.stderr, end="\n")
        sys.exit(1)