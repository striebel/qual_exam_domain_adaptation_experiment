import sys
import importlib.util
import os
import json

import numpy as np
from mlxtend.evaluate import mcnemar_table
from mlxtend.evaluate import mcnemar


def main(repo_dir):
    
    results_dir = os.path.join(repo_dir, 'results')
    assert os.path.isdir(results_dir)
    
    results = dict()
    results['all'] = dict()
    
    total = 10 * 21 * 10
    i = 1
    
    for domain in [
        "answer", "email", "newsgroup", "reviews", "weblog",
        'GUM_conversation', 'GUM_fiction', 'GUM_interview', 'GUM_vlog', 'GUM_whow',
    ]:
        domain_dir = os.path.join(results_dir, domain)
        assert os.path.isdir(domain_dir), \
            'domain_dir: '+domain_dir
        
        results[domain] = dict()
        
        for proportion_i, proportion in enumerate([
            '000', '005', '010', '015', '020', '025', '030', '035', '040', '045',
            '050', '055', '060', '065', '070', '075', '080', '085', '090', '095', '100'
        ]):
            proportion_dir = os.path.join(domain_dir, proportion)
            assert os.path.isdir(proportion_dir)
            
            results[domain][proportion] = dict()
            
            results[domain][proportion]['z'] = {
                'gold_head'   : list(),
                'pred_head'   : list(),
                'gold_deprel' : list(),
                'pred_deprel' : list()
            }
            
            if 'answer' == domain:
                assert isinstance(results['all'], dict)
                assert len(results['all']) == proportion_i
                assert proportion not in results['all']
                results['all'][proportion] = dict()
                results['all'][proportion]['z'] = {
                    'gold_head'   : list(),
                    'pred_head'   : list(),
                    'gold_deprel' : list(),
                    'pred_deprel' : list()
                }
            
            for fold in 'abcdefghij':
                
                print(f'loading {i: >4} / {total}')
                i += 1
                
                fold_dir = os.path.join(proportion_dir, fold)
                assert os.path.isdir(fold_dir)
                in_dir = fold_dir
                
                in_name = 'test_v3.json'
                in_path = os.path.join(in_dir, in_name)
                assert os.path.isfile(in_path)
                in_file = open(in_path, 'r')
                result = json.loads(in_file.read())
                in_file.close()
                
                assert 4 == len(result)
                assert 'gold_head' in result
                assert 'pred_head' in result
                assert 'gold_deprel' in result
                assert 'pred_deprel' in result
                
                results[domain][proportion][fold] = result
                
                results[domain][proportion]['z']['gold_head']   += result['gold_head'].copy() 
                results[domain][proportion]['z']['pred_head']   += result['pred_head'].copy()
                results[domain][proportion]['z']['gold_deprel'] += result['gold_deprel'].copy()
                results[domain][proportion]['z']['pred_deprel'] += result['pred_deprel'].copy()
                
                results[ 'all'][proportion]['z']['gold_head']   += result['gold_head'].copy() 
                results[ 'all'][proportion]['z']['pred_head']   += result['pred_head'].copy()
                results[ 'all'][proportion]['z']['gold_deprel'] += result['gold_deprel'].copy()
                results[ 'all'][proportion]['z']['pred_deprel'] += result['pred_deprel'].copy()

    
    total = 11 * 21
    i = 1
    
    for domain in [
        'all',
        "answer", "email", "newsgroup", "reviews", "weblog",
        'GUM_conversation', 'GUM_fiction', 'GUM_interview', 'GUM_vlog', 'GUM_whow'
    ]:
        #print()
        #print('domain      :', domain)
        #print('======================')
        
        for proportion in [
            '000', '005', '010', '015', '020', '025', '030', '035', '040', '045',
            '050', '055', '060', '065', '070', '075', '080', '085', '090', '095', '100'
        ]:
            
            print(f'processing {i: >3} / {total}')
            i += 1
            
            # 0002 denotes the baseline
            # 0004 denotes the result for comparison
            
            y_target_head       = results[domain][     '010']['z']['gold_head'].copy()
            y_model_0002_head   = results[domain][     '010']['z']['pred_head'].copy()
            y_model_0004_head   = results[domain][proportion]['z']['pred_head'].copy()
            
            #y_target_head     = results['0002'][genre][  'result']['gold_head'].copy()
            #y_model_0002_head = results['0002'][genre][  'result']['pred_head'].copy()
            #y_model_0004_head = results['0004'][genre][proportion]['result']['pred_head'].copy()
            
            assert len(y_target_head) == len(y_model_0002_head)
            assert len(y_target_head) == len(y_model_0004_head)
            
            y_target_head_other = results[domain][proportion]['z']['gold_head'].copy()
            assert len(y_target_head) == len(y_target_head_other)
            for a, b in zip(y_target_head, y_target_head_other):
                assert isinstance(a, int)
                assert isinstance(b, int)
                assert a == b            
            
            #assert (
            #    len(y_target_head)
            #    == len(results['0004'][genre][proportion]['result']['gold_head'])
            #),'\nlen(y_target_head)                                             : ' + \
            #   f'{len(y_target_head)}\n'                                            + \
            #   f'len(results["0004"]["{genre}"]["{proportion}"]["result"]["gold_head"]) : ' + \
            #   f'{len(results["0004"][genre][proportion]["result"]["gold_head"])}'
            #for index, (gold_head_0002, gold_head_0004) \
            #in enumerate(zip(y_target_head, results['0004'][genre][proportion]['result']['gold_head'])):
            #    assert isinstance(gold_head_0002, int), '\n' \
            #        + f'index               : {index}\n' \
            #        + f'type(gold_head_0002): {type(gold_head_0002)}'
            #    assert isinstance(gold_head_0004, int)
            #    
            #    assert gold_head_0002 == gold_head_0004
            
            
            y_target_deprel     = results[domain][     '010']['z']['gold_deprel'].copy()
            y_model_0002_deprel = results[domain][     '010']['z']['pred_deprel'].copy()
            y_model_0004_deprel = results[domain][proportion]['z']['pred_deprel'].copy()
            
            #y_target_deprel     = results['0002'][genre]['result']['gold_deprel'].copy()
            #y_model_0002_deprel = results['0002'][genre]['result']['pred_deprel'].copy()
            #y_model_0004_deprel = results['0004'][genre][proportion]['result']['pred_deprel'].copy()
            
            assert len(y_target_deprel) == len(y_model_0002_deprel)
            assert len(y_target_deprel) == len(y_model_0004_deprel)
            
            y_target_deprel_other = results[domain][proportion]['z']['gold_deprel'].copy()
            assert len(y_target_deprel) == len(y_target_deprel_other)
            for a, b in zip(y_target_deprel, y_target_deprel_other):
                assert isinstance(a, str)
                assert isinstance(b, str)
                assert a == b
            
            #for index, (gold_deprel_0002, gold_deprel_0004) \
            #in enumerate(zip(y_target_deprel, results['0004'][genre][proportion]['result']['gold_deprel'])):
            #    assert isinstance(gold_deprel_0002, str)
            #    assert isinstance(gold_deprel_0004, str)
            #    assert gold_deprel_0002 == gold_deprel_0004
            
            
            #_0002_official_uas = results['0002'][genre]['stats']['UAS'] \
            #    if 'all'!=genre else None 
            #_0004_official_uas = results['0004'][genre][proportion]['stats']['UAS'] \
            #    if 'all'!=genre else None 
            #_0002_official_las = results['0002'][genre]['stats']['LAS'] \
            #    if 'all'!=genre else None 
            #_0004_official_las = results['0004'][genre][proportion]['stats']['LAS'] \
            #    if 'all'!=genre else None 
            
            _0002_uas = sum([
                1 if gold == pred else 0
                for gold, pred in zip(y_target_head, y_model_0002_head)
             ]) / len(y_target_head)
            _0004_uas = sum([
                1 if gold == pred else 0
                for gold, pred in zip(y_target_head, y_model_0004_head)
            ]) / len(y_target_head)
            
            _0002_las = sum([
                1 if gold_head == pred_head and gold_deprel == pred_deprel else 0
                for (gold_head, pred_head), (gold_deprel, pred_deprel) in zip(
                    zip(y_target_head, y_model_0002_head),
                    zip(y_target_deprel, y_model_0002_deprel)
                )
            ]) / len(y_target_deprel)
            _0004_las = sum([
                1 if gold_head == pred_head and gold_deprel == pred_deprel else 0
                for (gold_head, pred_head), (gold_deprel, pred_deprel) in zip(
                    zip(y_target_head, y_model_0004_head),
                    zip(y_target_deprel, y_model_0004_deprel)
                )
            ]) / len(y_target_deprel)
            
            def deprel_to_id(deprel):
                LIST_OF_DEPRELS = '''
                    acl advcl advmod amod appos aux case cc ccomp clf compound
                    conj cop csubj dep det discourse dislocated expl fixed flat
                    goeswith iobj list mark nmod nsubj nummod obj obl orphan
                    parataxis punct reparandum root vocative xcomp
                    '''.split()
                assert deprel in LIST_OF_DEPRELS
                id = LIST_OF_DEPRELS.index(deprel)
                assert 0 <= id and id < len(LIST_OF_DEPRELS)
                return id
            
            y_target_deprel = \
                np.array([
                    (2 ** head) + (3 ** deprel_to_id(deprel))
                    for head, deprel in zip(y_target_head, y_target_deprel)
                ])
            y_model_0002_deprel = \
                np.array([
                    (2 ** head) + (3 ** deprel_to_id(deprel))
                    for head, deprel in zip(y_model_0002_head, y_model_0002_deprel)
                ])
            y_model_0004_deprel = \
                np.array([
                    (2 ** head) + (3 ** deprel_to_id(deprel))
                    for head, deprel in zip(y_model_0004_head, y_model_0004_deprel)
                ])
            
            y_target_head     = np.array(y_target_head)
            y_model_0002_head = np.array(y_model_0002_head)
            y_model_0004_head = np.array(y_model_0004_head)
            
            contingency_table_head = mcnemar_table(
                y_target = y_target_head,
                y_model1 = y_model_0002_head,
                y_model2 = y_model_0004_head
            )
            
            contingency_table_deprel = mcnemar_table(
                y_target = y_target_deprel,
                y_model1 = y_model_0002_deprel,
                y_model2 = y_model_0004_deprel
            )
            
            chi2_head, p_head = mcnemar(ary=contingency_table_head, corrected=False)
            
            chi2_deprel, p_deprel = mcnemar(ary=contingency_table_deprel, corrected=False)
            
            out_dict = {
                'chi2_head'  : chi2_head,
                'chi2_deprel': chi2_deprel,
                'p_head'     : p_head,
                'p_deprel'   : p_deprel,
                '0002_uas'   : _0002_uas,
                '0002_las'   : _0002_las,
                '0004_uas'   : _0004_uas,
                '0004_las'   : _0004_las
            }
            
            out_dir = os.path.join(repo_dir, 'visualize', domain, proportion)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            out_name = 'test_v4.json'
            out_path = os.path.join(out_dir, out_name)
            out_file = open(out_path, 'w')
            out_file.write(json.dumps(out_dict))
            out_file.close()
            
            
            #if _0002_uas < _0004_uas and p_head < 0.05:
            ##if _0002_uas > _0004_uas and p_head < 0.05:
            #
            #    print(contingency_table_head)
            #    
            #    print('proportion        :', proportion)
            #    
            #    print('chi-squared       :', chi2_head)
            #    print('p                 :', p_head)

            #    print('0002 my       UAS :', _0002_uas)
            #    print('0002 official UAS :', _0002_official_uas)
            #    print('0004 my       UAS :', _0004_uas)
            #    print('0004 official UAS :', _0004_official_uas)
            #
            #if _0002_las < _0004_las and p_deprel < 0.05:
            #if _0002_las > _0004_las and p_deprel < 0.05:
            #    
            #    print(contingency_table_deprel)
            #    
            #    print('proportion :', proportion)
            #    
            #    print('chi-squared:', chi2_deprel)
            #    print('p          :', p_deprel)
            #    
            #    print('0002 my       LAS :', _0002_las)
            #    print('0002 official LAS :', _0002_official_las)
            #    print('0004 my       LAS :', _0004_las)
            #    print('0004 official LAS :', _0004_official_las)
                
            


if '__main__' == __name__:
    print('BEGIN')
    repo_dir = sys.argv[1]
    main(repo_dir)
    print('END')
