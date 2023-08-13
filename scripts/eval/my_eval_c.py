import sys
import importlib.util
import os
import json

import conllu


def main(repo_dir, data_dir):
    
    def get_out_dict(gold_file_path, pred_file_path, domain):
        
        gold_file = open(gold_file_path, 'r')
        pred_file = open(pred_file_path, 'r')
        
        gold_file_str = gold_file.read()
        pred_file_str = pred_file.read()
        
        gold_file.close()
        pred_file.close()
        
        gold_sents     = conllu.parse(gold_file_str)
        all_pred_sents = conllu.parse(pred_file_str)
        
        sent_id_to_pred_sent = dict()
        for pred_sent in all_pred_sents:
            sent_id = pred_sent.metadata['sent_id']
            assert sent_id not in sent_id_to_pred_sent
            sent_id_to_pred_sent[sent_id] = pred_sent
        
        pred_sents = [
            sent_id_to_pred_sent[
                gold_sent.metadata['sent_id']
            ]
            for gold_sent in gold_sents
        ]
        
        assert len(gold_sents) == len(pred_sents)
        
        gold_head = list()
        pred_head = list()
        
        gold_deprel = list()
        pred_deprel = list()
        
        for gold_sent, pred_sent in zip(gold_sents, pred_sents):
            
            assert domain == gold_sent.metadata['domain']
            assert domain == pred_sent.metadata['domain']
            
            assert gold_sent.metadata['sent_id'] == pred_sent.metadata['sent_id']
            
            assert len(gold_sent) == len(pred_sent)
            
            assert gold_sent.metadata['text'] == pred_sent.metadata['text']
            
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

    total = 10 * 21 * 10
    i = 1 

    results_dir = os.path.join(repo_dir, 'results')
    if not os.path.isdir(results_dir):
        os.mkdir(results_dir)
    
    for domain in [
        "answer", "email", "newsgroup", "reviews", "weblog",
        'GUM_conversation', 'GUM_fiction', 'GUM_interview', 'GUM_vlog', 'GUM_whow'
    ]:
        
        domain_dir = os.path.join(results_dir, domain)
        if not os.path.isdir(domain_dir):
            os.mkdir(domain_dir)
        
        for proportion in [
            '000', '005', '010', '015', '020', '025', '030', '035', '040', '045',
            '050', '055', '060', '065', '070', '075', '080', '085', '090', '095', '100'
        ]:
            
            proportion_dir = os.path.join(domain_dir, proportion)
            if not os.path.isdir(proportion_dir):
                os.mkdir(proportion_dir)
            
            for fold in 'abcdefghij':
                
                print(f'{i: >4} / {total}')
                i += 1
                
                fold_dir = os.path.join(proportion_dir, fold)
                if not os.path.isdir(fold_dir):
                    os.mkdir(fold_dir)
                out_dir = fold_dir
                
                gold_file_path = os.path.join(data_dir, 'treebanks', 'folds', fold, 'test', domain+'.conllu')
                pred_file_path = os.path.join(data_dir, 'predictions', domain, proportion, fold, 'test.conllu')
                
                out_dict = get_out_dict(gold_file_path, pred_file_path, domain)
                out_name = 'test_v3.json'
                
                out_path = os.path.join(out_dir, out_name)
                out_file = open(out_path, 'w')
                out_file.write(json.dumps(out_dict))
                out_file.close()


if '__main__' == __name__:
    repo_dir = sys.argv[1]
    data_dir = sys.argv[2]
    main(repo_dir, data_dir)
