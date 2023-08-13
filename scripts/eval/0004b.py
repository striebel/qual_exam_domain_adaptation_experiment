import sys
import importlib.util
import os
import json


def main(repo_dir, data_dir, eval_script_path):
    
    def score_to_dict(score):
        return {
            'correct'         : score.correct,
            'gold_total'      : score.gold_total,
            'system_total'    : score.system_total,
            'aligned_total'   : score.aligned_total,
            'precision'       : score.precision,
            'recall'          : score.recall,
            'f1'              : score.f1,
            'aligned_accuracy': score.aligned_accuracy
        }
    
    spec = importlib.util.spec_from_file_location('eval', eval_script_path)
    eval = importlib.util.module_from_spec(spec)
    sys.modules['eval'] = eval
    spec.loader.exec_module(eval)
    
    
    for genre in ["answer", "email", "newsgroup", "reviews", "weblog"]:
        
        base_results_dir = os.path.join(repo_dir, 'results', '0004')
        if not os.path.isdir(base_results_dir):
            os.mkdir(base_results_dir)
        
        ###############################
        
        out_dir = os.path.join(base_results_dir, '0002')
        if not os.path.isdir(out_dir):
             os.mkdir(out_dir)
        
        gold = eval.load_conllu_file(os.path.join(data_dir, 'treebanks', 'ewt', 'clean', 'test', genre+'.conllu'))
        predicted = eval.load_conllu_file(os.path.join(data_dir, 'predictions', '0002', genre+'.conllu'))
        
        result = eval.evaluate(gold, predicted)

        out_dict = dict([(key, score_to_dict(score)) for key, score in result.items()])
        out_name = genre + '.v2.json'
        
        out_path = os.path.join(out_dir, out_name)
        out_file = open(out_path, 'w')
        out_file.write(json.dumps(out_dict))
        out_file.close()
        
        ###############################
        
        out_dir = os.path.join(base_results_dir, '0003')
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)
        
        gold = eval.load_conllu_file(os.path.join(data_dir, 'treebanks', 'ewt', 'clean', 'test_with_genre_column', genre+'.conllu'))
        predicted = eval.load_conllu_file(os.path.join(data_dir, 'predictions', '0003', genre+'.conllu'))
        
        result = eval.evaluate(gold, predicted)
        
        out_dict = dict([(key, score_to_dict(score)) for key, score in result.items()])
        out_name = genre + '.v2.json'
        
        out_path = os.path.join(out_dir, out_name)
        out_file = open(out_path, 'w')
        out_file.write(json.dumps(out_dict))
        out_file.close()
        
        ###############################
        
        for proportion in ["00", "02", "04", "06", "08", "10"]:
            
            out_dir = os.path.join(base_results_dir, '0004')
            if not os.path.isdir(out_dir):
                os.mkdir(out_dir)
            
            out_dir = os.path.join(out_dir, genre)
            if not os.path.isdir(out_dir):
                os.mkdir(out_dir)
            
            gold = eval.load_conllu_file(os.path.join(data_dir, 'treebanks', 'ewt', 'clean', 'test', genre+'.conllu'))
            predicted = eval.load_conllu_file(os.path.join(data_dir, 'predictions', '0004', genre, proportion+'.conllu'))
            
            result = eval.evaluate(gold, predicted)
            
            out_dict = dict([(key, score_to_dict(score)) for key, score in result.items()])
            out_name = proportion + '.v2.json'
            
            out_path = os.path.join(out_dir, out_name)
            out_file = open(out_path, 'w')
            out_file.write(json.dumps(out_dict))
            out_file.close()


if '__main__' == __name__:
    repo_dir = sys.argv[1]
    data_dir = sys.argv[2]
    eval_script_path = sys.argv[3]
    main(repo_dir, data_dir, eval_script_path)
