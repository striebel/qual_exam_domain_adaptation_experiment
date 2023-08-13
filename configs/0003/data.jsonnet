local model_id = "0003";
{
    model_0003 : {
        "train_data_path"       : "data/"+model_id+"/train.conllu",
        "validations_data_path" : "data/"+model_id+"/dev.conllu",
        "word_idx": 1,
        "dataset_embed_idx": 9,
        "tasks": {
            "dependency_task_name": {
                "task_type": "dependency",
                "column_idx": 6
            }
        }
    }
}
