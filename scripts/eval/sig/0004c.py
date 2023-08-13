import sys
import importlib.util
import os
import json

import numpy as np
from mlxtend.evaluate import mcnemar_table
from mlxtend.evaluate import mcnemar

def main(repo_dir):
    
    results = {'0002': dict(), '0003': dict(), '0004': dict()}
    
    base_results_dir = os.path.join(repo_dir, 'results', '0004')
    if not os.path.isdir(base_results_dir):
        os.mkdir(base_results_dir)
    
    for genre in ["answer", "email", "newsgroup", "reviews", "weblog"]:
        
        ###############################
        ## 0002
        
        in_dir = os.path.join(base_results_dir, '0002')
        assert os.path.isdir(in_dir)
        
        in_name = genre + '.v3.json'
        in_path = os.path.join(in_dir, in_name)
        in_file = open(in_path, 'r')
        result_0002 = json.loads(in_file.read())
        in_file.close()

        in_name = genre + '.json'
        in_path = os.path.join(in_dir, in_name)
        in_file = open(in_path, 'r')
        stats_0002 = json.loads(in_file.read())
        in_file.close()
        
        out_dir = in_dir
        out_name = genre + '.sig_v1.json'
        out_path = os.path.join(out_dir, out_name)
        
        results['0002'][genre] = dict()
        results['0002'][genre]['result'] = result_0002
        results['0002'][genre]['stats'] = stats_0002
        results['0002'][genre]['out_path'] = out_path
        
        ###############################
        ## 0003
        
        in_dir = os.path.join(base_results_dir, '0003')
        assert os.path.isdir(in_dir)
        
        in_name = genre + '.v3.json'
        in_path = os.path.join(in_dir, in_name)
        in_file = open(in_path, 'r')
        result_0003 = json.loads(in_file.read())
        in_file.close()

        in_name = genre + '.json'
        in_path = os.path.join(in_dir, in_name)
        in_file = open(in_path, 'r')
        stats_0003 = json.loads(in_file.read())
        in_file.close()
        
        out_dir = in_dir
        out_name = genre + '.sig_v1.json'
        out_path = os.path.join(out_dir, out_name)
        
        results['0003'][genre] = dict()
        results['0003'][genre]['result'] = result_0003
        results['0003'][genre]['stats'] = stats_0003
        results['0003'][genre]['out_path'] = out_path
        
        ###############################
        
        results['0004'][genre] = dict()
        
        for proportion in ["00", "02", "04", "06", "08", "10"]:
            
            in_dir = os.path.join(base_results_dir, '0004')
            assert os.path.isdir(in_dir)
            
            in_dir = os.path.join(in_dir, genre)
            assert os.path.isdir(in_dir)
            
            in_name = proportion + '.v3.json'
            in_path = os.path.join(in_dir, in_name)
            in_file = open(in_path, 'r')
            result_0004 = json.loads(in_file.read())
            in_file.close()

            in_name = proportion + '.json'
            in_path = os.path.join(in_dir, in_name)
            in_file = open(in_path, 'r')
            stats_0004 = json.loads(in_file.read())
            in_file.close()
            
            out_dir = in_dir
            out_name = proportion + '.sig_v1.json'
            out_path = os.path.join(out_dir, out_name)
            
            results['0004'][genre][proportion] = dict()
            results['0004'][genre][proportion]['result'] = result_0004
            results['0004'][genre][proportion]['stats'] = stats_0004
            results['0004'][genre][proportion]['out_path'] = out_path
    
    
    results['0002']['all'] = dict()
    results['0004']['all'] = dict()
    
    keys = ['gold_head', 'pred_head', 'gold_deprel', 'pred_deprel']
    
    
    results['0002']['all']['result'] = dict()
    results['0002']['all']['out_path'] = \
        os.path.join(
            os.path.dirname(results['0002']['answer']['out_path']),
            'all.sig_v1.json'
        )
    
    for k in keys:
        results['0002']['all']['result'][k] = []
    
    for genre in ["answer", "email", "newsgroup", "reviews", "weblog"]:
        for k in keys:
            tmp = results['0002'][genre]['result'][k]
            results['0002']['all']['result'][k] += tmp
        #print('len(tmp):', len(tmp))
    
    #print(len(results['0002']['all']['result']['gold_head'])); sys.exit(-1)
    
    
    for proportion in ["00", "02", "04", "06", "08", "10"]:

        out_dir = os.path.join(
            os.path.dirname(os.path.dirname(
                results['0004']['answer']['00']['out_path']
            )),
            'all'
        )
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)
        
        results['0004']['all'][proportion] = dict()
        results['0004']['all'][proportion]['result'] = dict()
        results['0004']['all'][proportion]['out_path'] = \
            os.path.join(out_dir, proportion + '.sig_v1.json')

        for k in keys:
            results['0004']['all'][proportion]['result'][k] = []
        
        for genre in ["answer", "email", "newsgroup", "reviews", "weblog"]:
            
            for k in keys:
                results['0004']['all'][proportion]['result'][k] += \
                    results['0004'][genre][proportion]['result'][k]
        

            
    for genre in ["answer", "email", "newsgroup", "reviews", "weblog", "all"]:
        
        print()
        print('genre      :', genre)
        print('======================')
        
        for proportion in ["00", "02", "04", "06", "08", "10"]:
            
            y_target_head     = results['0002'][genre]['result']['gold_head'].copy()
            y_model_0002_head = results['0002'][genre]['result']['pred_head'].copy()
            y_model_0004_head = results['0004'][genre][proportion]['result']['pred_head'].copy()
            
            assert (
                len(y_target_head)
                == len(results['0004'][genre][proportion]['result']['gold_head'])
            ),'\nlen(y_target_head)                                             : ' + \
               f'{len(y_target_head)}\n'                                            + \
               f'len(results["0004"]["{genre}"]["{proportion}"]["result"]["gold_head"]) : ' + \
               f'{len(results["0004"][genre][proportion]["result"]["gold_head"])}'
            assert len(y_target_head) == len(y_model_0002_head)
            assert len(y_target_head) == len(y_model_0004_head)
            for index, (gold_head_0002, gold_head_0004) \
            in enumerate(zip(y_target_head, results['0004'][genre][proportion]['result']['gold_head'])):
                assert isinstance(gold_head_0002, int), '\n' \
                    + f'index               : {index}\n' \
                    + f'type(gold_head_0002): {type(gold_head_0002)}'
                assert isinstance(gold_head_0004, int)
                
                assert gold_head_0002 == gold_head_0004
            
            y_target_deprel     = results['0002'][genre]['result']['gold_deprel'].copy()
            y_model_0002_deprel = results['0002'][genre]['result']['pred_deprel'].copy()
            y_model_0004_deprel = results['0004'][genre][proportion]['result']['pred_deprel'].copy()

            assert len(y_target_deprel) == len(y_target_head)
            assert len(y_target_deprel) == len(results['0004'][genre][proportion]['result']['gold_deprel'])
            assert len(y_target_deprel) == len(y_model_0002_deprel)
            assert len(y_target_deprel) == len(y_model_0004_deprel)
            for index, (gold_deprel_0002, gold_deprel_0004) \
            in enumerate(zip(y_target_deprel, results['0004'][genre][proportion]['result']['gold_deprel'])):
                assert isinstance(gold_deprel_0002, str)
                assert isinstance(gold_deprel_0004, str)
                assert gold_deprel_0002 == gold_deprel_0004
            
            _0002_official_uas = results['0002'][genre]['stats']['UAS'] \
                if 'all'!=genre else None 
            _0004_official_uas = results['0004'][genre][proportion]['stats']['UAS'] \
                if 'all'!=genre else None 
            _0002_official_las = results['0002'][genre]['stats']['LAS'] \
                if 'all'!=genre else None 
            _0004_official_las = results['0004'][genre][proportion]['stats']['LAS'] \
                if 'all'!=genre else None 
            
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
            out_path = results['0004'][genre][proportion]['out_path']
            out_file = open(out_path, 'w')
            out_file.write(json.dumps(out_dict))
            out_file.close()
            
            
            if _0002_uas < _0004_uas and p_head < 0.05:
            #if _0002_uas > _0004_uas and p_head < 0.05:
            
                print(contingency_table_head)
                
                print('proportion        :', proportion)
                
                print('chi-squared       :', chi2_head)
                print('p                 :', p_head)

                print('0002 my       UAS :', _0002_uas)
                print('0002 official UAS :', _0002_official_uas)
                print('0004 my       UAS :', _0004_uas)
                print('0004 official UAS :', _0004_official_uas)
            
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
