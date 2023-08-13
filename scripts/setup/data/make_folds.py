import sys
import os
import pickle
import random

import conllu


def make_folds(treebank_dir, repo_dir):
    assert os.path.isdir(treebank_dir)
    assert os.path.isdir(repo_dir)
    
    domain_to_sent_strs = dict()
    
    for treebank_name in ['ewt', 'gum']:
        base_dir = os.path.join(treebank_dir, treebank_name)
        assert os.path.isdir(base_dir)
        
        domain_annotated_dir = os.path.join(base_dir, 'domain')
        assert os.path.isdir(domain_annotated_dir)
        
        in_path = os.path.join(domain_annotated_dir, 'domain_to_sent_strs.pickle')
        assert os.path.isfile(in_path)
        
        in_file = open(in_path, 'rb')
        _domain_to_sent_strs = pickle.load(in_file)
        in_file.close()
    
        for domain, sent_strs in _domain_to_sent_strs.items():
            assert domain not in domain_to_sent_strs
            domain_to_sent_strs[domain] = sent_strs
    
    ewt_domains = [
        'answer',
        'email',
        'newsgroup',
        'reviews',
        'weblog'
    ]
    gum_domains = [
        'GUM_academic',
        'GUM_bio',
        'GUM_conversation',
        'GUM_fiction',
        'GUM_interview',
        'GUM_news',
        'GUM_speech',
        'GUM_textbook',
        'GUM_vlog',
        'GUM_voyage',
        'GUM_whow'
    ]
    domains = ewt_domains + gum_domains
    
    assert 16 == len(domains)
    assert 16 == len(domain_to_sent_strs)
    
    for d in domain_to_sent_strs.keys():
        assert d in domains
    for d in domains:
        assert d in domain_to_sent_strs.keys()
    
    domains_to_del = set()
    for domain, sent_strs in domain_to_sent_strs.items():
        if len(sent_strs) < 1000:
            domains_to_del.add(domain)
    
    for domain in domains_to_del:
        del domain_to_sent_strs[domain]
    
    assert 10 == len(domain_to_sent_strs)
    
    folds_dir = os.path.join(repo_dir, 'folds')
    assert not os.path.isfile(folds_dir)
    if os.path.isdir(folds_dir):
        print('error: folds dir is specified as' , file=sys.stderr)
        print('    '+folds_dir                   , file=sys.stderr)
        print('    which already exists, exiting', file=sys.stderr)
        sys.exit(-1)
    assert not os.path.isfile(folds_dir)
    assert not os.path.isdir(folds_dir)
    os.mkdir(folds_dir)
    
    domain_to_sent_ids = dict(
        [(domain, list()) for domain in domain_to_sent_strs.keys()]
    )
    for domain, sent_strs in domain_to_sent_strs.items():
        random.shuffle(sent_strs)
        assert 0 == len(domain_to_sent_ids[domain])
        assert 1000 <= len(sent_strs)
        for sent_str in sent_strs[:1000]:
            conllu_objs = conllu.parse(sent_str)
            assert 1 == len(conllu_objs)
            c = conllu_objs[0]
            assert domain == c.metadata['domain']
            sent_id = c.metadata['sent_id']
            assert len(domain) < len(sent_id)
            domain_to_sent_ids[domain].append(sent_id)
    
    assert 10 == len(domain_to_sent_ids)
    for domain, sent_ids in domain_to_sent_ids.items():
        assert 1000 == len(sent_ids)
    
    for domain, sent_ids in domain_to_sent_ids.items():
        out_path = os.path.join(folds_dir, f'{domain}.txt')
        assert not os.path.isfile(out_path)
        out_file = open(out_path, 'w')
        out_file.write(
            '\n'.join(sent_ids)
        )
        out_file.close()
    
    return 0


if '__main__' == __name__:
    treebank_dir = sys.argv[1]
    repo_dir     = sys.argv[2]
    sys.exit(make_folds(treebank_dir, repo_dir))
