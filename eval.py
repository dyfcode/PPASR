import argparse
import functools
import time

from ppasr.trainer import PPASRTrainer
from ppasr.utils.utils import add_arguments, print_arguments

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg('batch_size',       int,    32,                       '评估的批量大小')
add_arg('num_workers',      int,    8,                        '读取数据的线程数量')
add_arg('alpha',            float,  2.2,                      '集束搜索的LM系数')
add_arg('beta',             float,  4.3,                      '集束搜索的WC系数')
add_arg('beam_size',        int,    300,                      '集束搜索的大小，范围:[5, 500]')
add_arg('num_proc_bsearch', int,    10,                       '集束搜索方法使用CPU数量')
add_arg('cutoff_prob',      float,  0.99,                     '剪枝的概率')
add_arg('cutoff_top_n',     int,    40,                       '剪枝的最大值')
add_arg('use_model',        str,   'deepspeech2',             '所使用的模型')
add_arg('test_manifest',    str,   'dataset/manifest.test',   '测试数据的数据列表路径')
add_arg('dataset_vocab',    str,   'dataset/vocabulary.txt',  '数据字典的路径')
add_arg('mean_std_path',    str,   'dataset/mean_std.npz',    '数据集的均值和标准值的npy文件路径')
add_arg('decoder',          str,   'ctc_beam_search',         '结果解码方法', choices=['ctc_beam_search', 'ctc_greedy'])
add_arg('resume_model',     str,   'models/deepspeech2/best_model/', '模型的路径')
add_arg('lang_model_path',  str,   'lm/zh_giga.no_cna_cmn.prune01244.klm',        "语言模型文件路径")
args = parser.parse_args()
print_arguments(args)


trainer = PPASRTrainer(use_model=args.use_model,
                       mean_std_path=args.mean_std_path,
                       test_manifest=args.test_manifest,
                       dataset_vocab=args.dataset_vocab,
                       num_workers=args.num_workers,
                       alpha=args.alpha,
                       beta=args.beta,
                       beam_size=args.beam_size,
                       num_proc_bsearch=args.num_proc_bsearch,
                       cutoff_prob=args.cutoff_prob,
                       cutoff_top_n=args.cutoff_top_n,
                       decoder=args.decoder,
                       lang_model_path=args.lang_model_path)

start = time.time()
cer = trainer.evaluate(batch_size=args.batch_size,
                       resume_model=args.resume_model)
end = time.time()
print('评估消耗时间：{}s，字错率：{:.5f}'.format(int(end - start), cer))
