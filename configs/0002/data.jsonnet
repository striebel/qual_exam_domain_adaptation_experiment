local model_id = "0002";
{
    model_0002 : {
        "train_data_path"     : "data/"+model_id+"/train.conllu",
        "validation_data_path": "data/"+model_id+"/dev.conllu",
        "word_idx": 1,
        "tasks": {
            "dependency_task_name": {
                "task_type": "dependency",
                "column_idx": 6
            }
        }
    }
}
