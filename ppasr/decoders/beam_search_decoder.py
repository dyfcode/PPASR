import os
import sys

from ppasr.decoders.swig_wrapper import Scorer
from ppasr.decoders.swig_wrapper import ctc_beam_search_decoder_batch, ctc_beam_search_decoder


class BeamSearchDecoder:
    def __init__(self, beam_alpha, beam_beta, language_model_path, vocab_list):
        if language_model_path != 'None' and language_model_path != '' and language_model_path is not None and os.path.exists(language_model_path):
            print('=' * 70)
            print("初始化解码器...")
            self._ext_scorer = Scorer(beam_alpha, beam_beta, language_model_path, vocab_list)
            lm_char_based = self._ext_scorer.is_character_based()
            lm_max_order = self._ext_scorer.get_max_order()
            lm_dict_size = self._ext_scorer.get_dict_size()
            print("language model: "
                  "is_character_based = %d," % lm_char_based +
                  " max_order = %d," % lm_max_order +
                  " dict_size = %d" % lm_dict_size)
            print("初始化解码器完成!")
            print('=' * 70)
        else:
            self._ext_scorer = None
            raise Exception("没有语言模型，请按照文档下载并指定语音模型路径！")

    # 单个数据解码
    def decode_beam_search(self, probs_split, beam_alpha, beam_beta,
                           beam_size, cutoff_prob, cutoff_top_n,
                           vocab_list, blank_id=0):
        if self._ext_scorer is not None:
            self._ext_scorer.reset_params(beam_alpha, beam_beta)
        # beam search decode
        beam_search_result = ctc_beam_search_decoder(probs_seq=probs_split,
                                                     vocabulary=vocab_list,
                                                     beam_size=beam_size,
                                                     ext_scoring_func=self._ext_scorer,
                                                     cutoff_prob=cutoff_prob,
                                                     cutoff_top_n=cutoff_top_n,
                                                     blank_id=blank_id)
        return beam_search_result[0]

    # 一批数据解码
    def decode_batch_beam_search(self, probs_split, beam_alpha, beam_beta,
                                 beam_size, cutoff_prob, cutoff_top_n,
                                 vocab_list, num_processes, blank_id=0):
        if self._ext_scorer is not None:
            self._ext_scorer.reset_params(beam_alpha, beam_beta)
        # beam search decode
        num_processes = min(num_processes, len(probs_split))
        beam_search_results = ctc_beam_search_decoder_batch(probs_split=probs_split,
                                                            vocabulary=vocab_list,
                                                            beam_size=beam_size,
                                                            num_processes=num_processes,
                                                            ext_scoring_func=self._ext_scorer,
                                                            cutoff_prob=cutoff_prob,
                                                            cutoff_top_n=cutoff_top_n,
                                                            blank_id=blank_id)
        results = [result[0][1] for result in beam_search_results]
        return results
