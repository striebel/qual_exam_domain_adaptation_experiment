import sys
import os
import pickle

import conllu


def generate_conllu_files(treebank_dir, folds_dir):
    assert os.path.isdir(treebank_dir)
    assert os.path.isdir(folds_dir)
    
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
    
    sent_id_to_sent_str = dict()
    for domain, sent_strs in domain_to_sent_strs.items():
        for sent_str in sent_strs:
            conllu_objs = conllu.parse(sent_str)
            assert 1 == len(conllu_objs)
            c = conllu_objs[0]
            assert domain == c.metadata['domain']
            sent_id = c.metadata['sent_id']
            assert sent_id not in sent_id_to_sent_str
            sent_id_to_sent_str[sent_id] = sent_str
    
    domain_to_sent_ids = dict()
    for sent_ids_list_file_name in os.listdir(folds_dir):
        assert '.txt' == sent_ids_list_file_name[-4:]
        domain = sent_ids_list_file_name[:-4]
        assert domain in domain_to_sent_strs
        sent_ids_list_file = open(os.path.join(folds_dir, sent_ids_list_file_name))
        sent_ids_list = sent_ids_list_file.read().split()
        sent_ids_list_file.close()
        assert 1000 == len(sent_ids_list)
        assert domain not in domain_to_sent_ids
        domain_to_sent_ids[domain] = sent_ids_list
    assert 10 == len(domain_to_sent_ids)
    
    domain_to_chosen_sent_strs = dict()
    for domain, sent_ids in domain_to_sent_ids.items():
        assert 1000 == len(sent_ids)
        assert domain not in domain_to_chosen_sent_strs
        domain_to_chosen_sent_strs[domain] = list()
        for sent_id in sent_ids:
            sent_str = sent_id_to_sent_str[sent_id]
            assert (
                domain
                == conllu.parse(sent_str)[0].metadata['domain']
            )            
            domain_to_chosen_sent_strs[domain].append(
                sent_str
            )
    assert 10 == len(domain_to_chosen_sent_strs)
    for chosen_sent_strs in domain_to_chosen_sent_strs.values():
        assert 1000 == len(chosen_sent_strs)
    
    assert os.path.isdir(treebank_dir)
    conllu_folds_dir = os.path.join(treebank_dir, 'folds')
    assert not os.path.isfile(conllu_folds_dir)
    if os.path.isdir(conllu_folds_dir):
        print('error: conllu folds dir is specified as', file=sys.stderr)
        print('    '+conllu_folds_dir                  , file=sys.stderr)
        print('    which already exits, exiting'       , file=sys.stderr)
        sys.exit(-1)
    
    for fold in 'abcdefghij': # ten folds labeled 'a' through 'j'
        test_sent_strs  = list()
        dev_sent_strs   = list()
        train_sent_strs = list()
        domain_to_test_sent_strs = dict()
        domain_to_dev_sent_strs  = dict()
        for domain, chosen_sent_strs in domain_to_chosen_sent_strs.items():
            assert 1000 == len(chosen_sent_strs)
            _test_sent_strs  = chosen_sent_strs[
                                   100*(ord(fold)-ord('a'))
                                  :100*(ord(fold)-ord('a')+1)
                               ]
            _dev_sent_strs   = chosen_sent_strs[
                                   100*(ord(fold)-ord('a')-1)
                                  :100*(ord(fold)-ord('a'))
                                  if 'a'!=fold else None
                               ]
            _train_sent_strs = chosen_sent_strs[
                                  :100*(ord(fold)-ord('a')-1)
                                   if 'a'!=fold else 0
                               ] \
                               + chosen_sent_strs[
                                   100*(ord(fold)-ord('a')+1)
                                  :None # 1000
                                   if 'a'!=fold else 900
                               ]
            assert 100 == len(_test_sent_strs)
            assert 100 == len(_dev_sent_strs)
            assert 800 == len(_train_sent_strs), \
                'len(_train_sent_strs): '+str(len(_train_sent_strs))
            test_sent_strs  += _test_sent_strs
            dev_sent_strs   += _dev_sent_strs
            train_sent_strs += _train_sent_strs
            assert domain not in domain_to_test_sent_strs
            domain_to_test_sent_strs[domain] = _test_sent_strs
            domain_to_dev_sent_strs[domain]  = _dev_sent_strs
        assert 1000 == len(test_sent_strs)
        assert 1000 == len(dev_sent_strs)
        assert 8000 == len(train_sent_strs)
        
        if 'a'==fold:
            assert not os.path.isdir(conllu_folds_dir)
            os.mkdir(conllu_folds_dir)
        assert os.path.isdir(conllu_folds_dir)
        this_fold_dir = os.path.join(conllu_folds_dir, fold)
        assert not os.path.isdir(this_fold_dir)
        os.mkdir(this_fold_dir)
        for split_name, sent_strs in zip(
            ['test', 'dev', 'train'],
            [test_sent_strs, dev_sent_strs, train_sent_strs]
        ):
            file_path = os.path.join(this_fold_dir, split_name + '.conllu')
            assert not os.path.isfile(file_path)
            file = open(file_path, 'w')
            file.write(
                '\n\n'.join([sent_str.strip() for sent_str in sent_strs])
                + '\n\n'
            )
            file.close()
        test_domains_dir = os.path.join(this_fold_dir, 'test')
        assert not os.path.isdir(test_domains_dir)
        os.mkdir(test_domains_dir)
        for domain, test_sent_strs in domain_to_test_sent_strs.items():
            file_path = os.path.join(test_domains_dir, domain+'.conllu')
            assert not os.path.isfile(file_path)
            file = open(file_path, 'w')
            file.write(
                '\n\n'.join([sent_str.strip() for sent_str in test_sent_strs])
                + '\n\n'
            )
            file.close()
        dev_domains_dir = os.path.join(this_fold_dir, 'dev')
        assert not os.path.isdir(dev_domains_dir)
        os.mkdir(dev_domains_dir)
        for domain, dev_sent_strs in domain_to_dev_sent_strs.items():
            file_path = os.path.join(dev_domains_dir, domain+'.conllu')
            assert not os.path.isfile(file_path)
            file = open(file_path, 'w')
            file.write(
                '\n\n'.join([sent_str.strip() for sent_str in dev_sent_strs])
                + '\n\n'
            )
    
    return 0


if '__main__' == __name__:
    treebank_dir = sys.argv[1]
    folds_dir    = sys.argv[2]
    sys.exit(
        generate_conllu_files(
            treebank_dir,
            folds_dir
        )
    )


