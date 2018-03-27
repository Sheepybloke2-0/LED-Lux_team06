import numpy as np
import os
import cv2
import six.moves.urllib as urllib
import sys
import tensorflow as tf
import threading
import multiprocessing

# Append the current dir to the syspath so that it finds the correct modules
sys.path.append("..")

# From https://github.com/datitran/object_detector_app/blob/master/utils/app_utils.py, written by
# pyimagesearch to imporve camera FPS
from utils.app_utils import FPS, WebcamVideoStream
# Needed to optimize the FPS and detection
from multiprocessing import Queue, Pool
# Not sure if needed
from collections import defaultdict

 # Improt object_detection module
from utils import label_map_util
from utils import visualization_utils as vis_util

if tf.__version__ < '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')

# --------- Globals -------------------------
MODEL_PATH = '/home/rtl55/tensorflow/models/research/object_detection/models/model_zoo/ssd_mobilenet_v1_coco_2017_11_17'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_PATH + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

# Coco classes that need to be mapped to categories
NUM_CLASSES = 90

# Count the number of people
num_people = 0
person_in_frame = False

# Label maps connect the classes to the categories names
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# ---------- Classes ----------------
class WebcamVideoStream:
    """Class defined to handle the running of the webcam in a seperate thread"""
    def __init__(self, src=0):
    # Send in video source to start and grab initial frame
        self.stream = cv2.VideoCapture(src)
        # Assume that the camera is 1080
        self.stream.set(3, 1280)
        self.stream.set(4, 720)
        (self.isGrabbed, self.frame) = self.stream.read()

        # Variable to indicate if thread should be stopped
        self.stopped = False

    # Start thread to read frames in from stream
    def start(self):
        threading.Thread(target=self.updateFrame, args=()).start()
        return self

    def updateFrame(self):
        while True:
            # Break thread if stopped
            if self.stopped:
                return
            (self.isGrabbed, self.frame) = self.stream.read()

    def getFrame(self):
        return self.isGrabbed, self.frame

    def stop(self):
        self.stopped = True

# ------------- Functions -----------------------------------
def detect_objects(image, graph, sess):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image, axis=0)
    image_tensor = graph.get_tensor_by_name('image_tensor:0')

    # Each box is a something thats been detected
    boxes = graph.get_tensor_by_name('detection_boxes:0')

    # Score is how conifident we are that the object is classified correctly
    scores = graph.get_tensor_by_name('detection_scores:0')
    # Classes are what objects are recognized
    classes = graph.get_tensor_by_name('detection_classes:0')
    # Number of detections found
    num_detections = graph.get_tensor_by_name('num_detections:0')

    # Run the detection
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    output_dict = {}
    output_dict['boxes'] = boxes
    output_dict['classes'] = classes
    output_dict['scores'] = scores
    # Might need this, but I don't think so
    # output_dict['num_detections'] = num_detections

    # Run the visualization
    vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=4)

    return image, output_dict

def worker_node(input_frame_q, output_frame_q, output_dict_q):
    """Use for parrallelizing the frame detections"""
    # This needs to be done everytime as each has its own new space
    detection_graph = tf.Graph()
    with detection_graph.as_default():
      od_graph_def = tf.GraphDef()
      with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    # Start the TF Session
    sess = tf.Session(graph=detection_graph)

    while True:
        frame = input_frame_q.get()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image, output_dict = detect_objects(frame_rgb, detection_graph, sess)
        output_frame_q.put(image)
        output_dict_q.put(output_dict)

    sess.close()

if __name__ == '__main__':
    # Start the multiprocessing
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(multiprocessing.SUBDEBUG)

    # Set queue sizes
    input_frame_q = Queue(maxsize=5 )
    output_frame_q = Queue(maxsize=5)
    output_dict_q = Queue(maxsize=5)

    # Set the Pool size and number of workers
    pool = Pool(2 , worker_node, (input_frame_q, output_frame_q, output_dict_q))

    # Start the Webcam
    webcam = WebcamVideoStream(src=0).start()
    # Start the tensorflow session
    while(1):
        err, img = webcam.getFrame()
        if err == True:
            input_frame_q.put(img)

            # Retreive the dicts and break out the useful ones
            out_dict = output_dict_q.get()
            classes = out_dict['classes']
            scores = out_dict['scores']

            # Break open the NP array so that we can compare the objects to their scores
            classes_index = np.nditer(classes, flags=['f_index'])
            found_obj = []
            for id in classes_index:
                current_index = classes_index.index
                # There's almost always a 1, just very low probablility. Ensure i is greater than 50%
                if scores[0][current_index] > 0.50:
                    # Add all found objects to a List
                    found_obj.append(id)

            # If a person was found and they weren't there before, add 1
            if 1 in found_obj:
                if person_in_frame != True:
                    num_people += 1
                    person_in_frame = True
                    print(num_people)
            else:
                person_in_frame = False

            img_brg   = cv2.cvtColor(output_frame_q.get(), cv2.COLOR_RGB2BGR)
            cv2.imshow("img", img_brg)
        else:
            print("Check if the camera is connected to the system!")
            break

        k = cv2.waitKey(60) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    webcam.stop()
    pool.terminate()
