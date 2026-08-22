import sys
import argparse
from . import ssr_bac, ssr_euk, aa_bac, aa_euk, split_1, split_2, site_num, site, concat_1, overlap_count, concat_2, combine_list, com, coord2excel, split, score, final_score, delete


def order():
    parser = argparse.ArgumentParser(prog='PROG')
    subparsers = parser.add_subparsers(help = 'Functions')

    #添加子命令 Genome_sequences_extract
    parser_e = subparsers.add_parser('e', help='Extract genome sequences and translate into amino acid sequences')
    parser_e.add_argument('-c', '--coord', type=str, metavar = '<dir>', required=True, help='Input coord path; ExampleData = ExampleData/input-similar')
    parser_e.add_argument('-g', '--genome', type=str, metavar = '<dir>', required=True, help='Input bacterias/eukaryotes genome path; ExampleData1 = ExampleData/genome-bac, ExampleData2 = ExampleData/genome-euk')
    parser_e.add_argument('-s', '--specie', type=str, metavar = 'bac/euk', required=True, help='\'bac\' or \'euk\'; Write in \'bac\' if specie is bacteria, write in \'euk\' if specie is eukaryote')
    parser_e.add_argument('-o', '--output', type=str, metavar = '<dir>', required=True, help='Output path; For example: Results')
    parser_e.add_argument('-k', '--keep', default='False', action='store_true', help='Keep the processing files')
    #添加子命令 Genome_sequences_family_selection
    parser_f = subparsers.add_parser('b', help='Build the initiated amino acid sequence families')
    parser_f.add_argument('-i', '--input', type=str, metavar = '<dir>', required=True, help='Input path; ExampleData = ExampleData/input-b')
    parser_f.add_argument('-o', '--output', type=str, metavar = '<dir>', required=True, help='Output path; For example: Results')
    parser_f.add_argument('-k', '--keep', default='False', action='store_true', help='Keep the processing files')
    #添加子命令 Marker_sequences_selection_1
    parser_c = subparsers.add_parser('cl', help='Give a possible list shows which sequences can combine and also a list shows the sequences need to be deleted')
    parser_c.add_argument('-i', '--input', type=str, metavar = '<dir>', required=True, help='Input path; ExampleData = ExampleData/input-cl')
    parser_c.add_argument('-o', '--output', type=str, metavar = '<dir>', required=True, help='Output path; For example: Results')
    parser_c.add_argument('-k', '--keep', default='False', action='store_true', help='Keep the processing files')
    #添加子命令 Marker_sequences_selection_2
    parser_c = subparsers.add_parser('c', help='Combine partial sequences from the same taxon to form a single sequence if they branched together with high support(>=95 for UFBOOT2, >= 85 for True Bootstrap) and remove amino acid sequences whose amino acids are all the same with other sequences')
    parser_c.add_argument('-i1', '--input1', type=str, metavar = '<dir>', required=True, help='Input sequences file path; ExampleData = ExampleData/input-cl')
    parser_c.add_argument('-i2', '--input2', type=str, metavar = '<dir>', required=True, help='Input path which contains delete and combine folders, two folder names must be \'delete\' and \'combine\', file filename extension must be \'fasta\'; ExampleData = ExampleData/input-c')
    parser_c.add_argument('-o', '--output', type=str, metavar = '<dir>', required=True, help='Output path; For example: Results')
    parser_c.add_argument('-k', '--keep', default='False', action='store_true', help='Keep the processing files')
    #添加子命令 Similarity_order
    parser_s = subparsers.add_parser('s', help='Score the similarity between two species\' genome')
    parser_s.add_argument('-i', '--input', type=str, metavar = '<dir>', required=True, help='Input path; ExampleData = ExampleData/input-s')
    parser_s.add_argument('-o', '--output', type=str, metavar = '<dir>', required=True, help='Output path; For example: Results')
    parser_s.add_argument('-k', '--keep', default='False', action='store_true', help='Keep the processing files')

    args = parser.parse_args()
    delete_judge = args.keep
    return args, delete_judge

def b(args, delete_judge):
    split_1.process_excel_files(args)
    site.site(args)
    concat_1.concat(args)
    split_2.process_excel_files(args)
    overlap_count.count(args)
    site_num.site_num(args)
    concat_2.concat(args, delete_judge)

def cl(args):
    combine_list.main(args)

def c(args, delete_judge):
    delete.main(args)
    com.main(args, delete_judge)

def s(args, delete_judge):
    coord2excel.excel(args)
    split.process_excel_files(args)
    score.main(args)
    final_score.process_scores(args, delete_judge)


def e(args, delete_judge):
    if args.specie == "bac":
        ssr_bac.main(args)
        aa_bac.main(args, delete_judge)
    elif args.specie == "euk":
        ssr_euk.main(args)
        aa_euk.main(args, delete_judge)
    else:
        print("specie is error,please write in 'euk' or 'bac'")

def main():
    args, delete_judge = order()
    if sys.argv[1] == "e":
        e(args, delete_judge)
    if sys.argv[1] == "b":
        b(args, delete_judge)
    if sys.argv[1] == "cl":
        cl(args)
    if sys.argv[1] == "c":
        c(args, delete_judge)
    if sys.argv[1] == "s":
        s(args, delete_judge)        

if __name__ == "__main__":
    main()