import sys
import os
import pickle

def print_stats(treebank_dir, treebank_name):
    assert treebank_name in ['ewt', 'gum']
    
    assert os.path.isdir(treebank_dir)
    base_dir = os.path.join(treebank_dir, treebank_name)
    assert os.path.isdir(base_dir)
    
    domain_annotated_dir = os.path.join(base_dir, 'domain')
    assert os.path.isdir(domain_annotated_dir)
    
    in_path = os.path.join(domain_annotated_dir, 'domain_to_sent_strs.pickle')
    assert os.path.isfile(in_path)
    
    in_file = open(in_path, 'rb')
    domain_to_sent_strs = pickle.load(in_file)
    in_file.close()
    
    if 'ewt' == treebank_name:
        domains = [
           'answer',
           'email',
           'newsgroup',
           'reviews',
           'weblog'
        ]
    else:
        assert 'gum' == treebank_name
        domains = [
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
    
    for d in domain_to_sent_strs.keys():
        assert d in domains
    for d in domains:
        assert d in domain_to_sent_strs.keys()
    
    total = 0
    print('treebank:', treebank_name)
    for domain, sent_strs in domain_to_sent_strs.items():
        print(f'    {domain:<20}: {len(sent_strs):>5}')
        total += len(sent_strs)
    total_name = 'total'
    print(f'    {total_name:<20}: {total:>5}')
    
    return 0

if '__main__' == __name__:
    treebank_dir  = sys.argv[1]
    treebank_name = sys.argv[2]
    sys.exit(print_stats(treebank_dir, treebank_name))
