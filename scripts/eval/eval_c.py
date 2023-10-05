import sys
import importlib.util
import os
import json

import conllu


def main():
    
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
    
    DOMAINS = [
        "answer", "email", "newsgroup", "reviews", "weblog",
        'GUM_conversation', 'GUM_fiction', 'GUM_interview', 'GUM_vlog', 'GUM_whow'
    ]
    PROPORTIONS = [
        '000', '005', '010', '015', '020', '025', '030', '035', '040', '045',
        '050', '055', '060', '065', '070', '075', '080', '085', '090', '095', '100'
    ]
    FOLDS = 'abcdefghij'
    
    assert 10 == len(DOMAINS)
    assert 21 == len(PROPORTIONS)
    assert 10 == len(FOLDS)
    
    NUM_GOLD_FILES = len(FOLDS) * len(DOMAINS)
    assert 100 == NUM_GOLD_FILES
    i = 1
    
    DATA_DIR = os.environ['DATA_DIR']
    assert os.path.isdir(DATA_DIR)
    
    treebanks_dir = os.path.join(DATA_DIR, 'treebanks')
    assert os.path.isdir(treebanks_dir)
    
    folds_dir = os.path.join(treebanks_dir, 'folds')
    assert os.path.isdir(folds_dir)
    
    for fold in FOLDS:
        specific_fold_dir = os.path.join(folds_dir, fold)
        assert os.path.isdir(specific_fold_dir)
        
        test_dir = os.path.join(specific_fold_dir, 'test')
        assert os.path.isdir(test_dir)
        
        for domain in DOMAINS:
            test_file_path = os.path.join(test_dir, domain+'.conllu')
            assert os.path.isfile(test_file_path)
            
            print(f'{i: >3} / {NUM_GOLD_FILES} gold test file present')
            i += 1
    
    NUM_PRED_FILES = len(DOMAINS) * len(PROPORTIONS) * len(FOLDS)
    assert 2100 == NUM_PRED_FILES
    j = 1
    n_present = 0
    n_missing = 0
    
    predictions_dir = os.path.join(DATA_DIR, 'predictions')
    assert os.path.isdir(predictions_dir)
    
    domain_to_proportion_to_is_done = {}
    
    for domain in DOMAINS:
        domain_dir = os.path.join(predictions_dir, domain)
        if not os.path.isdir(domain_dir):
            os.mkdir(domain_dir)
        
        assert domain not in domain_to_proportion_to_is_done
        domain_to_proportion_to_is_done[domain] = {}
        for proportion in PROPORTIONS:
            proportion_dir = os.path.join(domain_dir, proportion)
            if not os.path.isdir(proportion_dir):
                os.mkdir(proportion_dir)
            
            assert proportion not in domain_to_proportion_to_is_done[domain]
            domain_to_proportion_to_is_done[domain][proportion] = True
            for fold in FOLDS:
                fold_dir = os.path.join(proportion_dir, fold)
                if not os.path.isdir(fold_dir):
                    os.mkdir(fold_dir)
                
                test_file_path = os.path.join(fold_dir, 'test.conllu')
                if os.path.isfile(test_file_path):
                    n_present += 1
                    print(f'{j: >4} / {NUM_PRED_FILES} pred test file  is present')
                else:
                    n_missing += 1
                    print(f'{j: >4} / {NUM_PRED_FILES} pred test file NOT present')
                    domain_to_proportion_to_is_done[domain][proportion] = False
                j += 1
    
    assert NUM_PRED_FILES == n_present + n_missing
    print('')
    print(f'num pred test files present : {n_present:>4}')
    print(f'num pred test files missing : {n_missing:>4}')
    print('')
    print(f'frac pred test files present of total : {n_present/NUM_PRED_FILES:6.4f}')
    print('')
    
    print('')
    domain_to_is_done = {}
    n_domains_done = 0
    for domain in DOMAINS:
        domain_is_done = True
        for proportion in PROPORTIONS:
            is_done = domain_to_proportion_to_is_done[domain][proportion]
            if False == is_done:
                domain_is_done = False
            else:
                assert True == is_done
        assert domain not in domain_to_is_done
        if True == domain_is_done:
            print(f'{domain:<16}  is done')
            n_domains_done += 1
            domain_to_is_done[domain] = True
        else:
            assert False == domain_is_done
            print(f'{domain:<16} NOT done')
            domain_to_is_done[domain] = False
    print('')
    print(f'{n_domains_done:>2} / 10 domains are done')
    print('')
    
    input('press return to continue')
    print('')
    
    
    domain_to_is_done_str = json.dumps(domain_to_is_done)
    
    RSLT_DIR = os.environ['RSLT_DIR']
    os.path.isdir(RSLT_DIR)
    out_file_path = os.path.join(RSLT_DIR, 'domain_to_is_done.json')
    out_file = open(out_file_path, 'w')
    out_file.write(domain_to_is_done_str)
    out_file.close()
    
    n_pred_files_ready = n_domains_done * 21 * 10
    k = 1
    
    for domain in DOMAINS:
        assert domain in domain_to_is_done
        is_done = domain_to_is_done[domain]
        if False == is_done:
            continue
        else:
            assert True == is_done
        
        pred_domain_dir = os.path.join(predictions_dir, domain)
        assert os.path.isdir(pred_domain_dir)
        
        for proportion in PROPORTIONS:
            
            pred_proportion_dir = os.path.join(pred_domain_dir, proportion)
            assert os.path.isdir(pred_proportion_dir)
            
            for fold in FOLDS:
                
                print(f'{k: >4} / {n_pred_files_ready} pred-to-gold comparison')
                k += 1
                
                pred_fold_dir = os.path.join(pred_proportion_dir, fold)
                assert os.path.isdir(pred_fold_dir)
                
                pred_file_path = os.path.join(pred_fold_dir, 'test.conllu')
                assert os.path.isfile(pred_file_path)
                
                
                gold_fold_dir = os.path.join(treebanks_dir, 'folds', fold)
                assert os.path.isdir(gold_fold_dir)

                gold_file_path = os.path.join(gold_fold_dir, 'test', domain+'.conllu')
                assert os.path.isfile(gold_file_path)

                out_dict = get_out_dict(gold_file_path, pred_file_path, domain)
                out_name = 'test_v3.json'
                
                out_path = os.path.join(pred_fold_dir, out_name)
                out_file = open(out_path, 'w')
                out_file.write(json.dumps(out_dict))
                out_file.close()
    
    return 0


if '__main__' == __name__:
    sys.exit(main())






