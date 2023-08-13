import sys
import importlib.util
import os
import json

import statsmodels


def main(repo_dir):

    results = {'0002': dict(), '0003': dict(), '0004': dict()}
    
    for genre in ["answer", "email", "newsgroup", "reviews", "weblog"]:
        
        results[genre] = dict()
        
        base_results_dir = os.path.join(repo_dir, 'results', '0004')
        if not os.path.isdir(base_results_dir):
            os.mkdir(base_results_dir)
        
        ###############################
        ## 0002
        
        in_dir = os.path.join(base_results_dir, '0002')
        assert os.path.isdir(in_dir)
        
        in_name = genre + '.v2.json'
        in_path = os.path.join(in_dir, in_name)
        in_file = open(in_path, 'r')
        result_0002 = json.loads(in_file.read())
        in_file.close()
        
        results['0002'][genre] = result_0002
        
        ###############################
        ## 0003
        
        in_dir = os.path.join(base_results_dir, '0003')
        assert os.path.isdir(in_dir)
        
        in_name = genre + '.v2.json'
        in_path = os.path.join(in_dir, in_name)
        in_file = open(in_path, 'r')
        result_0003 = json.loads(in_file.read())
        in_file.close()
        
        results['0003'][genre] = result_0003
        
        ###############################
        
        results['0004'][genre] = dict()
        
        for proportion in ["00", "02", "04", "06", "08", "10"]:
            
            in_dir = os.path.join(base_results_dir, '0004')
            assert os.path.isdir(in_dir)
            
            in_dir = os.path.join(in_dir, genre)
            assert os.path.isdir(in_dir)
            
            in_name = proportion + '.v2.json'
            in_path = os.path.join(in_dir, in_name)
            in_file = open(in_path, 'r')
            result_0004 = json.loads(in_file.read())
            in_file.close()
            
            results['0004'][genre][proportion] = result_0004
            
    for genre in ["answer", "email", "newsgroup", "reviews", "weblog"]:
        _0002_correct       = results['0002'][genre]['LAS']['correct']      ; print('_0002_correct      :', _0002_correct)
        _0002_gold_total    = results['0002'][genre]['LAS']['gold_total']   ; print('_0002_gold_total   :', _0002_gold_total)
        _0002_system_total  = results['0002'][genre]['LAS']['system_total'] #; print('_0002_system_total :', _0002_system_total)
        _0002_aligned_total = results['0002'][genre]['LAS']['aligned_total']#; print('_0002_aligned_total:', _0002_aligned_total)
        _0002_precision     = results['0002'][genre]['LAS']['precision']    #; print('_0002_precision    :', _0002_precision)
        pass                                                                #; print('(correct/total)    :', (_0002_correct/_0002_gold_total))
        assert _0002_gold_total == _0002_system_total
        assert _0002_gold_total == _0002_aligned_total
        _0002_incorrect     = _0002_gold_total - _0002_correct              ; print('_0002_incorrect    :', _0002_incorrect)
        sys.exit(-1)
        
        _0003_correct = results['0003'][genre]['LAS']['correct']
        
        A = min([_0002_correct, _0003_correct])     # n correct in both model 1 and 2
        D = min([_0002_incorrect, _0003_incorrect]) # n incorrect in both model 1 and 2
        
        print(f'0002.{genre}   .LAS.correct:', _0002_correct)
        print(f'0003.{genre}   .LAS.correct:', _0003_correct, '\tdelta:', _0003_correct - _0002_correct)
        for proportion in ["00", "02", "04", "06", "08", "10"]:
            _0004_correct = results['0004'][genre][proportion]['LAS']['correct']
            print(f'0004.{genre}.{proportion}.LAS.correct:', _0004_correct, '\tdelta:', _0004_correct - _0002_correct)


if '__main__' == __name__:
    repo_dir = sys.argv[1]
    main(repo_dir)
