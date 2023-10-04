from typing import Iterator
import sys
import random
import math

import torch
import allennlp
from allennlp.data.dataloader import DataLoader

@DataLoader.register("dependency_data_loader")
class DependencyDataLoader(allennlp.data.dataloader.DataLoader):

    DOMAINS = [
        'GUM_conversation',
        'GUM_fiction',
        'GUM_interview',
        'GUM_vlog',
        'GUM_whow',
        'answer',
        'email',
        'newsgroup',
        'reviews',
        'weblog'
    ]
    PROPORTIONS = [
        '000', '005',
        '010', '015',            
        '020', '025',
        '030', '035',
        '040', '045',
        '050', '055',
        '060', '065',
        '070', '075',
        '080', '085',
        '090', '095',
        '100'
    ]
    FOLDS = 'abcdefghij'
    
    n_init = 0 
    n_next = 0
    
    def __init__(
        self,
        dataset    : allennlp.data.dataset_readers.dataset_reader.AllennlpDataset,
        batch_size : int,
        batch_sampler # not used here
    ):
        #import code
        #code.interact(local=locals())
        #sys.exit(-1)
        #sys.stderr.write('DependencyDataLoader : begin\n')
        #sys.stderr.write('type(dataset)        : ' + str(type(dataset)) + '\n')
        #sys.stderr.write('len(dataset)         : ' + str(len(dataset)) + '\n')
        #sys.stderr.write('batch_size           : ' + str(batch_size) + '\n')
        #sys.stderr.write('dir(dataset[3])      :\n')
        #import pprint
        #pprint.pprint(dir(dataset[3]), stream=sys.stderr)
        #sys.stderr.write('dataset[3].fields    :\n')
        #pprint.pprint(dataset[3].fields, stream=sys.stderr)
        ##sys.stderr.write('dir(dataset[3].fields) :\n')
        ##pprint.pprint(dir(dataset[3].fields), stream=sys.stderr)
        #sys.stderr.write('dir(dataset[3].fields["dataset"]) :\n')
        #pprint.pprint(dir(dataset[3].fields['dataset']), stream=sys.stderr)
        #sys.stderr.write('dir(dataset[3].fields["metadata"]):\n')
        #pprint.pprint(dir(dataset[3].fields['metadata']), stream=sys.stderr)
        #pprint.pprint(dataset[3].fields['metadata'].keys()     , stream=sys.stderr)
        #pprint.pprint(dataset[3].fields['metadata']['col_idxs'], stream=sys.stderr)
        ##sys.stderr.write('type(sampler)        : ' + str(type(sampler)) + '\n')
        ##sys.stderr.write('type(batch_sampler)  : ' + str(type(batch_sampler)) + '\n')
        ##sys.stderr.write('dir(batch_sampler)   : \n')
        ##import pprint
        ##pprint.pprint(dir(batch_sampler), stream=sys.stderr)
        #sys.stderr.write('DependencyDataLoader : end\n')
        #sys.exit(-1)
        
        
        self._domain     = dataset[0].domain
        self._proportion = dataset[0].proportion
        self._fold       = dataset[0].fold
        
        self._domain_to_instances = dict(
            [(domain, list()) for domain in DependencyDataLoader.DOMAINS]
        )
        
        #print('len(dataset):', len(dataset)); sys.exit(-1)
        
        #for idx in range(len(dataset)):
        
        assert len(dataset) in [100, 8000]
        if 100 == len(dataset):
            my_len = 100
            self._partition = 'dev'
        else:
            assert 8000 == len(dataset)
            my_len = 8000
            self._partition = 'train'
        for idx in range(my_len):
            instance = dataset[idx]
            assert self._domain     == instance.domain
            assert self._proportion == instance.proportion
            assert self._fold       == instance.fold
            
            assert hasattr(instance.conllu_obj, 'metadata')
            
            domain = instance.conllu_obj.metadata['domain']
            
            assert domain in self._domain_to_instances
            
            self._domain_to_instances[domain].append(instance)
            
        #print([(domain, len(instances)) for domain, instances in self._domain_to_instances.items()]); sys.exit(-1)
        
        
        self._dataset    = dataset   ; del dataset
        self._batch_size = batch_size; del batch_size
        self._idx        = 0
        
        assert self._domain     in DependencyDataLoader.DOMAINS
        assert self._proportion in DependencyDataLoader.PROPORTIONS
        assert self._fold       in DependencyDataLoader.FOLDS
        
        #file = open('/N/slate/jstrieb/tmp/flag', 'a')
        #file.write('1')
        #tell = file.tell()
        if 2 == DependencyDataLoader.n_init:
            sys.stderr.write('DependencyDataLoader.__init__: called for the third time\n')
            sys.stderr.write('init has been called n times: ' + str(DependencyDataLoader.n_init) + '\n')
            sys.stderr.write('next has been called n times: ' + str(DependencyDataLoader.n_next) + '\n')
            sys.exit(-1)
        #sys.exit(-1)

        DependencyDataLoader.n_init += 1
        
        self._batches = list()
        self._prepare_epoch()
    
    def _prepare_epoch(self) -> None:
        
        assert 0 == len(self._batches)
        
        proportion = int(self._proportion) / 100
        assert isinstance(proportion, float)
        assert 0.0 <= proportion
        assert proportion <= 1.0
        
        domain_to_instances = dict()
        for domain, instances in self._domain_to_instances.items():
            instances = instances.copy()
            random.shuffle(instances)
            domain_to_instances[domain] = instances
        
        domain_to_count = dict([(d, 0) for d in self._domain_to_instances.keys()])
        total=0
        
        other_domains = [d for d in domain_to_instances.keys() if d != self._domain]
        assert 9 == len(other_domains)
        
        assert self._partition in ['dev', 'train']
        if 'dev' == self._partition:
            for other_domain in other_domains:
                assert 0 == len(domain_to_instances[other_domain])
            assert 100 == len(domain_to_instances[self._domain])
            batch = domain_to_instances[self._domain]
            self._batches.append(batch)
        else:
            assert 'train' == self._partition
            batches_per_epoch = math.floor( 800.0 / self._batch_size )
            #while True:
            for _ in range(batches_per_epoch):
                batch = list()
                for _ in range(self._batch_size):
                    sample = random.random()
                    assert isinstance(sample, float)
                    assert 0.0 <= sample and sample < 1.0
                    if sample < proportion:
                        try:
                            batch.append(domain_to_instances[self._domain].pop())
                            domain_to_count[self._domain] += 1
                            total+=1
                        except IndexError:
                            break
                    else:
                        other_domain = random.choice(other_domains)
                        try:
                            batch.append(domain_to_instances[other_domain].pop())
                            domain_to_count[other_domain] += 1
                            total+=1 
                        except IndexError:
                            break
                if len(batch) < self._batch_size:
                    break
                assert len(batch) == self._batch_size
                self._batches.append(batch)
            
            assert batches_per_epoch <= len(self._batches)
            self._batches = self._batches[:batches_per_epoch]
            assert batches_per_epoch == len(self._batches)
            
        self._len = len(self._batches)
        
        #print('proportion :', proportion)
        #for domain, count in domain_to_count.items():
        #    print('domain :', domain)
        #    print('count             :', count)
        #    print('fraction                      :', count / total)
        #sys.exit(-1)
            

    def __len__(self) -> int:
        return self._len

    
    def __iter__(self) -> Iterator[allennlp.data.dataloader.TensorDict]:
        return self

    
    def __next__(self) -> allennlp.data.dataloader.TensorDict:
        
        #if 12 <= DependencyDataLoader.n_next:
        #    sys.stderr.write('init has been called n times: ' + str(DependencyDataLoader.n_init) + '\n')
        #    sys.stderr.write('next has been called n times: ' + str(DependencyDataLoader.n_next) + '\n')
        #    sys.exit(-1)
        
        DependencyDataLoader.n_next += 1
        
        try:
            instances = self._batches.pop()
            return allennlp.data.dataloader.allennlp_collate(instances)
        except IndexError:
            self._prepare_epoch()
            raise StopIteration
        

