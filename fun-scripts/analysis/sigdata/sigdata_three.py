from sigdata import *

"""
Parse several sigdata file at a time
"""

if __name__ == '__main__':
    path1 = '/Users/adian/Desktop/research/aflpp_fun/paper/evaluation/sigdata/bench-fairfuzz/fun/objdump/outs/out-4/default/q_sigdata'
    path2 = '/Users/adian/Desktop/research/aflpp_fun/paper/evaluation/sigdata/20230406-sigdata/objdump/outs/out-1/default/q_sigdata'
    dpath = '/Users/adian/Desktop/research/aflpp_fun/paper/evaluation/sigdata'
    norm_df_fun = normalize_sig_score(pd.read_csv(path1))
    norm_df_aflpp = normalize_sig_score(pd.read_csv(path2))

    draw_sig_score_violin_and_output(norm_df_fun, dpath=dpath, name='fun-objdump')
    draw_sig_score_violin_and_output(norm_df_aflpp, dpath=dpath, name='aflpp-objdump')

    draw_scatter_paper_method(norm_df_fun, dpath, 'fun-objdump')
    draw_scatter_paper_method(norm_df_fun, dpath, 'fun-objdump', True)

    draw_scatter_paper_method(norm_df_aflpp, dpath, 'aflpp-objdump')
    draw_scatter_paper_method(norm_df_aflpp, dpath, 'aflpp-objdump', True)
