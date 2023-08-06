# create by fanfan on 2017/8/25 0025
import os

class Params:
    projectDir = os.path.dirname(os.path.abspath(__file__))
    origin_data = os.path.join(projectDir,'data')
    output_path = os.path.join(projectDir,"output_ner")

    # 词库预处理设置
    vocab_size = 0
    num_tags = 0
    min_freq = 3
    max_sentence_length = 100
    tag_schema='iobes'


    # 网络参数
    hidden_size = 256
    embedding_size = 200
    initializer_range = 0.02
    clip = 5

    cell_type = 'lstm'      # bilstm 参数
    bilstm_layer_nums = 2  # bilstm 参数

    filter_width = 3 #idcnn参数
    num_filter = 256 #idcnn参数
    repeat_times = 4 #idcnn参数

    # 训练参数
    #model_path = os.path.join(output_path, 'model_ckpt/tf')
    total_train_steps = 100000
    batch_size = 256
    dropout_prob = 0.7
    learning_rate = 0.0001
    evaluate_every_steps = 500
    @property
    def model_path(self):
        return os.path.join(self.output_path, 'model_ckpt')

    def update_object(self,object):
        self.__dict__.update(object.__dict__)


    def update_dict(self,dict):
        self.__dict__.update(dict)


if __name__ == '__main__':
    params = Params()
    object = Params()
    object.batch_size = 0
    object.hidden_size = 0
    params.update_object(object)
    print(params.batch_size)
    print(params.hidden_size)

    dict = {"batch_size":1,"hidden_size":1}
    params.update_dict(dict)
    print(params.batch_size)
    print(params.hidden_size)








