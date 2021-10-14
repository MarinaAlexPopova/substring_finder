#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#@created: 
#@author: Marina Popova

from pathlib import Path
import sys
import argparse
import re

def main(settings):
    genes_dict = {}
    with open(Path(settings['input_file'])) as file:
            gene = []
            while True:
                line = file.readline().rstrip()
                if not line:
                    genes_dict[key] = ''.join(gene)
                    break
                elif line.startswith('>'):
                    if genes_dict:
                        genes_dict[key] = ''.join(gene)                                                            
                    key = line[1:].split()[0]
                    genes_dict[key] = None
                    gene = []
                else:
                    gene.append(line.rstrip())     

    complementary_table = str.maketrans({'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'})
    substring =  settings['substring']
    substring_complement = substring.translate(complementary_table)
    substring_reverse = substring_complement[::-1]    

    final_table = []
    for gene, seq in genes_dict.items():
            ind = [i.start() for i in re.finditer(f'(?={substring})', seq)]
            ind_reverse = [i.start() for i in re.finditer(f'(?={substring_reverse})', seq)]
            if ind:
                for i in ind:
                    final_table.append([gene, i+1, i+len(substring), '+', substring, '\n'])
            if ind_reverse:
                for i in ind_reverse:
                    final_table.append([gene, len(seq)-i-len(substring)+1, len(seq)-i, '-', substring, '\n'])

    with open(Path(settings['output_file']), 'w') as file:
        file.write('#chr #start_position #stop_position #strand #subsring_seq\n')
        file.writelines([' '.join(str(j) for j in i) for i in sorted(final_table)])
        


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Finding substring in genome')
    parser.add_argument('-a','--input', help='Input file', required=True)
    parser.add_argument('-o','--output', help='Ouput file', required=True)
    parser.add_argument('-s','--substring', help='Substring', required=True)
    args = vars(parser.parse_args())
    
    input_file = args["input"]
    output_file = args["output"]
    substring = args["substring"]

    settings = {
        "input_file": input_file,
        "output_file": output_file,
        "substring": substring,
    }

    main(settings)
