#!/usr/bin/env bash

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

if [ ! -v ACCOUNT ]
then
    echo 'error: slurm ACCOUNT variable not set, exiting'
    exit
fi


echo '#!/usr/bin/env bash'                            > ${REPO_DIR}/scripts/eval/archive_and_compress_results.sh
echo '(                                           \' >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sh 
echo '    cd '${RSLT_DIR}'/..                     \' >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sh
echo '    && tar czf `basename '${RSLT_DIR}'`.tgz \' >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sh
echo '               `basename '${RSLT_DIR}'`     \' >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sh
echo ')'                                             >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sh
chmod 700                                               ${REPO_DIR}/scripts/eval/archive_and_compress_results.sh


echo '#!/usr/bin/env sh'                                                > ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo '#SBATCH --account '${ACCOUNT}                                    >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo '#SBATCH --job-name tar_czf'                                      >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo '#SBATCH --partition gpu'                                         >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo '#SBATCH --output '${REPO_DIR}'/scripts/eval/archive_and_compress_results.stdout' >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo '#SBATCH --error  '${REPO_DIR}'/scripts/eval/archive_and_compress_results.stderr' >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo '#SBATCH --mail-type=ALL'                                         >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo '#SBATCH --mail-user=jstrieb@indiana.edu'                         >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo '#SBATCH --gres=gpu:1'                                            >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo '#SBATCH --nodes=1'                                               >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo '#SBATCH --time=1-00:00:00'                                       >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo '#SBATCH --mem=128G'                                              >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo '#SBATCH --cpus-per-task=1'                                       >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch
echo 'srun '${REPO_DIR}'/scripts/eval/archive_and_compress_results.sh' >> ${REPO_DIR}/scripts/eval/archive_and_compress_results.sbatch





