import os
from allennlp.common import Params
import myutils

udPath = 'data/ud-treebanks-v2.7/'
UDSETS = []
for UDdir in os.listdir(udPath):
    if 'Iceland' in UDdir:
        continue
    train, dev, _ = myutils.getTrainDevTest(udPath + UDdir)
    if dev != '' and myutils.hasColumn(train, 1):
        UDSETS.append(UDdir)


outDir = 'preds/'
for setting in ['self', 'concat.smoothed', 'sepDec.smoothed', 'datasetEmbeds.smoothed', 'concat']:
    scores = []
    for UDdir in UDSETS:
        output = outDir + ('' if setting == 'self' else 'fullUD') + setting + '.' + UDdir + '.dev.conllu.eval'
        if os.path.isfile(output):
            score = float(open(output).readline().strip().split()[-1])
        else:
            score = 0.0
            print("NF", setting, UDdir)
        scores.append(score)
        #print(UDdir, score)
    print(setting + ' & ' + str(round(sum(scores)/len(scores), 2)))
            
print()
glue = Params.from_file('configs/glue.json')
for setting in ['glue', 'glue.smoothSampling', 'glue.single']:
    scores = []
    for task in glue:
        output = outDir + setting + '.' + task + '.eval'
        if os.path.isfile(output):
            score = float(open(output).readline().split()[0])
        else:
            score = 0.0
        scores.append(score)
    print(setting + ' & ' + str(round(sum(100 * scores)/len(scores), 2)))


