## Setup and Intro Work
### 3/11/17

- Couple helpful URLs
  [1] https://github.com/tensorflow/models/tree/master/research/object_detection
  [2] https://github.com/tensorflow/models
  [3] https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md
  [4] https://towardsdatascience.com/building-a-real-time-object-recognition-app-with-tensorflow-and-opencv-b7a2b4ebdc32
  [5] https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md
  [6] https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/running_locally.md

- Start by installing all the dependencies following [3]
- Next, I'm going to work through the tutorial
  - NOTE: "Tensorflow Object Detection API expects data to be in the TFRecord format"
  - Training is in the `object_detection` folder. Use `train.py` [6]
    - To train a model```
      python3 train.py \
         --logtostderr \
         --train_dir=models/pet_model/train \
         --pipeline_config_path=models/pet_model/faster_rcnn_resnet101_pets.config
      ```
    - To evaluate a model. Separate job```
      python object_detection/eval.py \
        --logtostderr \
        --pipeline_config_path=${PATH_TO_YOUR_PIPELINE_CONFIG} \
        --checkpoint_dir=${PATH_TO_TRAIN_DIR} \
        --eval_dir=${PATH_TO_EVAL_DIR}
      ```
    -
