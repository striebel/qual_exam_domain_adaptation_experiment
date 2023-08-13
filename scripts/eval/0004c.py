import sys
import importlib.util
import os
import json

import conllu


def main(repo_dir, data_dir):
    
    def get_out_dict(gold_file_path, pred_file_path):
        
        gold_file = open(gold_file_path, 'r')
        pred_file = open(pred_file_path, 'r')
        
        gold_file_str = gold_file.read()
        pred_file_str = pred_file.read()
        
        gold_file.close()
        pred_file.close()
        
        #gold_sent_strs = gold_file_str.strip().split('\n\n')
        #pred_sent_strs = pred_file_str.strip().split('\n\n')
        
        #assert len(gold_sent_strs) == len(pred_sent_strs)
        
        #gold_sents = [conllu.parse(gold_sent_str) for gold_sent_str in gold_sent_strs]
        #pred_sents = [conllu.parse(pred_sent_str) for pred_sent_str in pred_sent_strs]
        
        gold_sents = conllu.parse(gold_file_str)
        pred_sents = conllu.parse(pred_file_str)
        
        assert len(gold_sents) == len(pred_sents)
        
        print('len(gold_sents):', len(gold_sents))
        print('len(pred_sents):', len(pred_sents))
        
        gold_head = list()
        pred_head = list()
        
        gold_deprel = list()
        pred_deprel = list()
        
        for gold_sent, pred_sent in zip(gold_sents, pred_sents):
            
            assert len(gold_sent) == len(pred_sent)
            
            for gold_token, pred_token in zip(gold_sent, pred_sent):

                gold_head.append(gold_token['head'])
                pred_head.append(pred_token['head'])
                
                gold_deprel.append(gold_token['deprel'])
                pred_deprel.append(pred_token['deprel'])
        
        return dict([
            ('gold_head', gold_head),
            ('pred_head', pred_head),
            ('gold_deprel', gold_deprel),
            ('pred_deprel', pred_deprel)
        ])
        
    for genre in ["answer", "email", "newsgroup", "reviews", "weblog"]:
        
        base_results_dir = os.path.join(repo_dir, 'results', '0004')
        if not os.path.isdir(base_results_dir):
            os.mkdir(base_results_dir)
        
        ###############################
        
        out_dir = os.path.join(base_results_dir, '0002')
        if not os.path.isdir(out_dir):
             os.mkdir(out_dir)
        
        gold_file_path = os.path.join(data_dir, 'treebanks', 'ewt', 'clean', 'test', genre+'.conllu')
        pred_file_path = os.path.join(data_dir, 'predictions', '0002', genre+'.conllu')
        
        out_dict = get_out_dict(gold_file_path, pred_file_path)
        out_name = genre + '.v3.json'
        
        out_path = os.path.join(out_dir, out_name)
        out_file = open(out_path, 'w')
        out_file.write(json.dumps(out_dict))
        out_file.close()
        
        ###############################
        
        out_dir = os.path.join(base_results_dir, '0003')
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)
        
        gold_file_path = os.path.join(data_dir, 'treebanks', 'ewt', 'clean', 'test_with_genre_column', genre+'.conllu')
        pred_file_path = os.path.join(data_dir, 'predictions', '0003', genre+'.conllu')
        
        out_dict = get_out_dict(gold_file_path, pred_file_path)
        out_name = genre + '.v3.json'
        
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
            
            gold_file_path = os.path.join(data_dir, 'treebanks', 'ewt', 'clean', 'test', genre+'.conllu')
            pred_file_path = os.path.join(data_dir, 'predictions', '0004', genre, proportion+'.conllu')
            
            out_dict = get_out_dict(gold_file_path, pred_file_path)
            out_name = proportion + '.v3.json'
            
            out_path = os.path.join(out_dir, out_name)
            out_file = open(out_path, 'w')
            out_file.write(json.dumps(out_dict))
            out_file.close()


if '__main__' == __name__:
    repo_dir = sys.argv[1]
    data_dir = sys.argv[2]
    main(repo_dir, data_dir)
