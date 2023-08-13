import sys
import os
import pickle

def annotate_domain(treebank_dir, treebank_name):
    assert treebank_name in ['ewt', 'gum']
    
    assert os.path.isdir(treebank_dir)
    base_dir = os.path.join(treebank_dir, treebank_name)
    assert os.path.isdir(base_dir)
    
    clean_dir = os.path.join(base_dir, 'clean')
    assert os.path.isdir(clean_dir)
    in_path = os.path.join(clean_dir, 'all.conllu')
    assert os.path.isfile(in_path)
    
    domain_annotated_dir = os.path.join(base_dir, 'domain')
    out_path = os.path.join(domain_annotated_dir, 'domain_to_sent_strs.pickle')
    if os.path.isfile(out_path):
        os.remove(out_path)
    if not os.path.isdir(domain_annotated_dir):
        os.mkdir(domain_annotated_dir)
    
    with open(in_path, 'r') as file:
        file_str = file.read()
    
    if __debug__:
        print('len(file_str)        :', len(file_str))
        print('len(file_str.strip()):', len(file_str.strip()))
    file_str = file_str.strip() # remove the terminating '\n\n'
    sent_strs = file_str.split('\n\n')
    if __debug__:
        print('len(sent_strs)       :', len(sent_strs))
        #print('first sent           :\n', sent_strs[0])
        #print('last sent            :\n', sent_strs[-1])
    
    if 'ewt' == treebank_name:
        genres = [
           'answer',
           'email',
           'newsgroup',
           'reviews',
           'weblog'
        ]
    else:
        assert 'gum' == treebank_name
        genres = [
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
    
    genre_to_sent_strs = dict([(genre, []) for genre in genres])
    for sent_str in sent_strs:
        sent_genres = set()
        for genre in genres:
            sent_id_prefix = f'sent_id = {genre}'
            if 0 < sent_str.find(sent_id_prefix):
                sent_genres.add(genre)
        assert len(sent_genres) <= 1
        if 0 == len(sent_genres):
            idx_of_id = sent_str.find('sent_id = ')
            assert 0 < idx_of_id
            idx_of_nl = sent_str[idx_of_id:].find('\n')
            assert 0 < idx_of_nl
            print('unkown genre', file=sys.stderr)
            print('============', file=sys.stderr)
            print('   ', sent_str[idx_of_id:idx_of_id+idx_of_nl], file=sys.stderr)
            sys.exit(-1)
        genre = sent_genres.pop()
        assert genre in genre_to_sent_strs
        assert isinstance(genre_to_sent_strs[genre], list)
        genre_to_sent_strs[genre].append(sent_str)
    
    genre_to_updated_sent_strs = dict([(genre, []) for genre in genres])
    for genre, sent_strs in genre_to_sent_strs.items():
        for sent_str in sent_strs:
            updated_sent_str = f'# domain = {genre}\n' + sent_str
            assert '\n' != updated_sent_str[-1]
            genre_to_updated_sent_strs[genre].append(updated_sent_str)
    
    out_file = open(out_path, 'wb')
    pickle.dump(genre_to_updated_sent_strs, out_file)
    out_file.close()
    
    return 0

if '__main__' == __name__:
    treebank_dir  = sys.argv[1]
    treebank_name = sys.argv[2]
    sys.exit(annotate_domain(treebank_dir, treebank_name))
