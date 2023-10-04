#!/usr/bin/env bash

if [ ! -v DATA_DIR ]
then
    echo 'error: DATA_DIR variable not set, exiting'
    exit
fi

if [ ! -v RSLT_DIR ]
then
    echo 'error: RSLT_DIR variable not set, exiting'
    exit 1
fi

if [ ! -v REPO_DIR ]
then
    echo 'error: REPO_DIR variable not set, exiting'
    exit
fi

if [ ! -v VENV_NAME ]
then
    echo 'error: VENV_NAME variable not set, exiting'
    exit
fi

if [ ! -v ACCOUNT ]
then
    echo 'error: slurm ACCOUNT variable not set, exiting'
    exit
fi


for domain in "answer" "email" "newsgroup" "reviews" "weblog" 'GUM_conversation' 'GUM_fiction' 'GUM_interview' 'GUM_vlog' 'GUM_whow'
do
    for proportion in \
        '000' '005' \
        '010' '015' \
        '020' '025' \
        '030' '035' \
        '040' '045' \
        '050' '055' \
        '060' '065' \
        '070' '075' \
        '080' '085' \
        '090' '095' \
        '100'
    do
        for fold in 'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j'
        do
            mkdir --parents                                                                                              ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}
            echo '{'                                                                                                   > ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
            echo '    "model_'${proportion}${fold}'_'${domain}'" : {'                                                 >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
            echo '        "train_data_path"      : "'${DATA_DIR}'/treebanks/folds/'${fold}'/train.conllu",'           >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
            echo '        "validation_data_path" : "'${DATA_DIR}'/treebanks/folds/'${fold}'/dev/'${domain}'.conllu",' >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
            echo '        "word_idx"             : 1,'                                                                >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
            echo '        "tasks"                : {'                                                                 >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
            echo '            "dependency_task_name" : {'                                                             >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
            echo '                "task_type"  : "dependency",'                                                       >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
            echo '                "column_idx" : 6'                                                                   >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
            echo '            }'                                                                                      >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
            echo '        },'                                                                                         >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
            echo '        "domain"     : "'${domain}'",'                                                              >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json 
            echo '        "proportion" : "'${proportion}'",'                                                          >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json 
            echo '        "fold"       : "'${fold}'"'                                                                 >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json 
            echo '    }'                                                                                              >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
            echo '}'                                                                                                  >> ${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json
           
            mkdir --parents                                                                               ${REPO_DIR}/scripts/train/${domain}/${proportion} 
            echo '#!/usr/bin/env sh'                                                                    > ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo ''                                                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '# build the config file'                                                             >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo ${REPO_DIR}/${VENV_NAME}/bin/python'                          \'                      >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '    '${REPO_DIR}/scripts/utils/translate_jsonnet_to_json.py' \'                      >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '        '${REPO_DIR}/configs/src/params.jsonnet'             \'                      >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '        '${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/params.json         >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo ''                                                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'RETCODE=$?'                                                                          >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'if [ 0 -ne $RETCODE ]'                                                               >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'then'                                                                                >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    echo "error: build config file failed"'                                          >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    exit $RETCODE'                                                                   >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo 'fi'                                                                                  >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo ''                                                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '# train the model'                                                                   >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            MODEL_NAME=model_${proportion}${fold}_${domain}
            echo ${REPO_DIR}/${VENV_NAME}/bin/python'                                               \' >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '    '${REPO_DIR}/parser/machamp-${MACHAMP_VERSION}/train.py'                      \' >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '        '--name' '${MODEL_NAME}'                                                  \' >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '        '--dataset_config'                                                        \' >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '            '${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/data.json'   \' >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '        '--parameters_config'                                                     \' >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '            '${REPO_DIR}/configs/bin/${domain}/${proportion}/${fold}/params.json' \' >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '        '--device' '0'                                                             ' >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo ''                                                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'RETCODE=$?'                                                                          >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'if [ 0 -ne $RETCODE ]'                                                               >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'then'                                                                                >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    echo "error: training the model failed"'                                         >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    exit $RETCODE'                                                                   >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo 'fi'                                                                                  >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo ''                                                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '# run predict on the test data'                                                      >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh  
            OUT_DIR_NAME=${DATA_DIR}/predictions/${domain}/${proportion}/${fold}
            echo 'mkdir --parents '${OUT_DIR_NAME}                                                     >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'MODEL_DIR_NAME=`ls -1 '${REPO_DIR}'/logs/'${MODEL_NAME}' | tail -n 1`'               >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo ${REPO_DIR}/${VENV_NAME}/bin/python'                                           \'     >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    '${REPO_DIR}/parser/machamp-${MACHAMP_VERSION}/predict.py'                \'     >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '        '${REPO_DIR}/logs/${MODEL_NAME}/'${MODEL_DIR_NAME}'/model.tar.gz'     \'     >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '        '${DATA_DIR}/treebanks/folds/${fold}/test/${domain}.conllu'           \'     >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '        '${OUT_DIR_NAME}/test.conllu'                                         \'     >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '        '--device' '0                                                                >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo ''                                                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'RETCODE=$?'                                                                          >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'if [ 0 -ne $RETCODE ]'                                                               >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'then'                                                                                >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    echo "error: predicting with the model failed"'                                  >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    exit $RETCODE'                                                                   >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo 'fi'                                                                                  >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo ''                                                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '# save the per epoch training progress before deleting the model dir'                >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo 'mkdir --parents '${RSLT_DIR}/${domain}/${proportion}/${fold}                         >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo 'cp                                                                     \'            >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '    '${REPO_DIR}'/logs/'${MODEL_NAME}'/${MODEL_DIR_NAME}/metrics*.json \'            >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '    '${RSLT_DIR}/${domain}/${proportion}/${fold}/'                      '            >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo ''                                                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo 'RETCODE=$?'                                                                          >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'if [ 0 -ne $RETCODE ]'                                                               >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'then'                                                                                >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    echo "error: copying the per-epoch log files failed"'                            >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    exit $RETCODE'                                                                   >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo 'fi'                                                                                  >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo ''                                                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '# delete the model since we can not afford to keep 2010 850M models on disk'         >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo 'rm -rf '${REPO_DIR}/logs/${MODEL_NAME}/'${MODEL_DIR_NAME}'                           >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo ''                                                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'RETCODE=$?'                                                                          >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'if [ 0 -ne $RETCODE ]'                                                               >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'then'                                                                                >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    echo "error: deleting the model failed"'                                         >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    exit $RETCODE'                                                                   >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo 'fi'                                                                                  >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo ''                                                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '# run the official ud eval script'                                                   >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo ${REPO_DIR}/${VENV_NAME}/bin/python'                                           \'     >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    '${REPO_DIR}/scripts/ud_tools/eval.py'                                    \'     >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '        '${DATA_DIR}/treebanks/folds/${fold}/test/${domain}.conllu'           \'     >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '        '${OUT_DIR_NAME}/test.conllu'                                         \'     >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo '        > '${RSLT_DIR}/${domain}/${proportion}/${fold}/test.txt                      >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo ''                                                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo 'RETCODE=$?'                                                                          >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'if [ 0 -ne $RETCODE ]'                                                               >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh 
            echo 'then'                                                                                >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    echo "error: running the official UD eval script failed"'                        >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo '    exit $RETCODE'                                                                   >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            echo 'fi'                                                                                  >> ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
            chmod 700                                                                                     ${REPO_DIR}/scripts/train/${domain}/${proportion}/${fold}.sh
        done
        
        echo '#!/usr/bin/env sh'                                                     > ${REPO_DIR}/scripts/train/${domain}/${proportion}.sh
        echo ''                                                                     >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sh
        echo 'for fold in "a" "b" "c" "d" "e" "f" "g" "h" "i" "j"'                  >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sh 
        echo 'do'                                                                   >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sh
        echo '    '${REPO_DIR}/scripts/train/${domain}/${proportion}/'${fold}'.sh   >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sh
        echo 'done'                                                                 >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sh
        chmod 700                                                                      ${REPO_DIR}/scripts/train/${domain}/${proportion}.sh
        
        mkdir --parents ${REPO_DIR}/logs/sbatch
        echo '#!/usr/bin/env sh'                                                     > ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo '#SBATCH --account '${ACCOUNT}                                         >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo '#SBATCH --job-name '${proportion}${domain}                            >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo '#SBATCH --partition gpu'                                              >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo '#SBATCH --output '${REPO_DIR}/logs/sbatch/${MODEL_NAME}.out           >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo '#SBATCH --error  '${REPO_DIR}/logs/sbatch/${MODEL_NAME}.err           >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo '#SBATCH --mail-type=ALL'                                              >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo '#SBATCH --mail-user=jstrieb@indiana.edu'                              >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo '#SBATCH --gres=gpu:1'                                                 >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo '#SBATCH --nodes=1'                                                    >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo '#SBATCH --time=1-00:00:00'                                            >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo '#SBATCH --mem=128G'                                                   >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo '#SBATCH --cpus-per-task=1'                                            >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo 'module load python/3.9.8'                                             >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
        echo 'srun '${REPO_DIR}/scripts/train/${domain}/${proportion}.sh            >> ${REPO_DIR}/scripts/train/${domain}/${proportion}.sbatch
    done
    
    echo '#!/usr/bin/env sh'                                                                      > ${REPO_DIR}/scripts/train/${domain}_dispatch.sh 
    echo ''                                                                                      >> ${REPO_DIR}/scripts/train/${domain}_dispatch.sh 
    echo 'for proportion in "000" "005" "010" "015" "020" "025" "030" "035" "040" "045"       \' >> ${REPO_DIR}/scripts/train/${domain}_dispatch.sh 
    echo '                  "050" "055" "060" "065" "070" "075" "080" "085" "090" "095" "100"  ' >> ${REPO_DIR}/scripts/train/${domain}_dispatch.sh
    echo 'do'                                                                                    >> ${REPO_DIR}/scripts/train/${domain}_dispatch.sh
    echo '    'sbatch ${REPO_DIR}/scripts/train/${domain}/'${proportion}'.sbatch                 >> ${REPO_DIR}/scripts/train/${domain}_dispatch.sh 
    echo 'done'                                                                                  >> ${REPO_DIR}/scripts/train/${domain}_dispatch.sh 
    chmod 700                                                                                       ${REPO_DIR}/scripts/train/${domain}_dispatch.sh
done






