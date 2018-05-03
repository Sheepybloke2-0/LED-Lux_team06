import numpy as np
import os
import cv2
import time
import six.moves.urllib as urllib
import sys
import tensorflow as tf
import threading
import multiprocessing
import serial

# Append the current dir to the syspath so that it finds the correct modules
sys.path.append("..")

# Needed to optimize the FPS and detection
from multiprocessing import Queue, Pool, Manager
# Not sure if needed
from collections import defaultdict

 # Improt object_detection module
from utils import label_map_util
from utils import visualization_utils as vis_util

if tf.__version__ < '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')

# --------- Globals -------------------------
# Development Environment
MODEL_PATH = '/home/rtl55/tensorflow/models/research/object_detection/models/model_zoo/ssd_mobilenet_v2_coco_2018_03_29'
# TK1 Environment
# MODEL_PATH = '/media/ubuntu/extraSpace/tensorflow/models/research/object_detection/models/model_zoo/ssd_mobilenet_v2_coco_2018_03_29'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_PATH + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

# Coco classes that need to be mapped to categories
NUM_CLASSES = 90

# Configs for connecting to ZigBee
PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

# OpenCV camera args
HEIGHT = 720
WIDTH  = 1280

# Count the number of people
TIME_OUT = 25
BOOK_RECOG_THRESHOLD = 25
book_in_frame = False
light_changed_book = False
TV_RECOG_THRESHOLD = 25
tv_in_frame = False
light_changed_tv = False
old_lights = { 'light1': False, 'light2': False, 'light3': False}
current_lights = { 'light1': False, 'light2': False, 'light3': False}

# Directional Constants
FWD = 0
BAK = 1
LFT = 0
RGT = 1

AREA_THRESHOLD = 1000
X_THRESHOLD  = 15
Y_THRESHOLD  = 1

# Regions
region1_start = (0,0)
region1_end = (int(WIDTH/4), HEIGHT)
region1_area = (int(WIDTH/4)) * HEIGHT

region2_start = (int(WIDTH/4), HEIGHT)
region2_end = (int(WIDTH*3/4), HEIGHT)
region2_area = (int(WIDTH*3/4)) * HEIGHT

region3_start = (int(WIDTH*3/4),0)
region3_end = (WIDTH, HEIGHT)
region3_area = (int(WIDTH/4)) * HEIGHT

region_dist_start = (854, 340)
region_dist_end = (954, 440)
region_dist_depth = 5

total_area = region1_area + region2_area + region3_area

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
        self.stream.set(3, WIDTH)
        self.stream.set(4, HEIGHT)
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

def get_regions( bounding_box, area, dif_x, dif_y):
    reg_bbox_area_dict = {'reg1': 0, 'reg2': 0, 'reg3': 0}
    reg_total_area_dict = {'reg1': 0, 'reg2': 0, 'reg3': 0}
    # Assign regionality to the box
    # Check percentage against total area. If greater than 70%, we'll assume too close for judgement and just assume on.
    total_percent_area = abs(area / total_area)
    if total_percent_area <= 0.70:
        # Catagorize the regionality using the X values
        # Start by checking region 1
        if bounding_box[1] <= region1_end[0]:
            # Find the area of the other regions
            if bounding_box[3] < region1_end[0]:
                # Case when both are in the region1 box. Get percentage, then assign region
                reg_total_area_dict['reg1'] = area / region1_area
                reg_bbox_area_dict['reg1'] = 1

            elif bounding_box[3] > region3_start[0]:
                reg_total_area_dict['reg1'] = ((region1_end[0] - bounding_box[1]) * dif_y) / region1_area
                reg_bbox_area_dict['reg1'] = ((region1_end[0] - bounding_box[1]) * dif_y) / area

                # If the largest x is in region3, spans all of region 2
                reg_total_area_dict['reg2'] = (640 * dif_y) / region2_area
                reg_bbox_area_dict['reg2'] = (640 * dif_y) / area

                reg_total_area_dict['reg3'] = ((bounding_box[3] - 960) * dif_y) / region3_area
                reg_bbox_area_dict['reg3'] = ((bounding_box[3] - 960) * dif_y) / area

            elif bounding_box[3] < region2_end[0] and bounding_box[3] > region2_start[0]:
                # No region 3
                reg_total_area_dict['reg1'] = ((region1_end[0] - bounding_box[1]) * dif_y) / region1_area
                reg_bbox_area_dict['reg1'] = ((region1_end[0] - bounding_box[1]) * dif_y) / area

                reg_total_area_dict['reg2'] = ((bounding_box[3] - region2_start[0]) * dif_y) / region2_area
                reg_bbox_area_dict['reg2'] = ((bounding_box[3] - region2_start[0]) * dif_y) / area

        elif bounding_box[1] <= region2_end[0]:
            if bounding_box[3] <= region2_end[0]:
                reg_total_area_dict['reg2'] = area / region2_area
                reg_bbox_area_dict['reg2'] = 1

            elif bounding_box[3] > region3_start[0]:
                reg_total_area_dict['reg2'] = ((region2_end[0] - bounding_box[1]) * dif_y) / region2_area
                reg_bbox_area_dict['reg2'] = ((region2_end[0] - bounding_box[1]) * dif_y) / area

                reg_total_area_dict['reg3'] = ((bounding_box[3] - 960) * dif_y) / region3_area
                reg_bbox_area_dict['reg3'] = ((bounding_box[3] - 960) * dif_y) / area

        # If the smallest x is in region3, all will be in region 3
        elif bounding_box[1] > region3_start[0]:
            reg_total_area_dict['reg3'] = area / region2_area
            reg_bbox_area_dict['reg3'] = 1
    else:
        # If the person is too close to track, set everything to 1
        reg_bbox_area_dict = {'reg1': 1, 'reg2': 1, 'reg3': 1}
        reg_total_area_dict = {'reg1': 1, 'reg2': 1, 'reg3': 1}

    return reg_total_area_dict, reg_bbox_area_dict, total_percent_area

def get_dif(cur_value, dif_array, old_value_array, idx):
    try:
        dif_array.append(old_value_array[idx] - cur_value)
    except IndexError:
        old_value_array.append(0)
        dif_array.append(old_value_array[idx] - cur_value)
    old_value_array[idx] = cur_value
    return dif_array, old_value_array

def classification_node(input_frame_q, output_frame_q, output_dict_q, old_mid_x, old_mid_y, old_area):
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
        print( multiprocessing.current_process())
        print(output_frame_q.qsize())
        # We want to reinit this dictionary every frame
        frame_dict = {
            'person_in_frame' : False, # Connected to delay_counter
            'num_people'      : 0,
            'person_in_reg1'  : False, # Tells which of the three lights to turn on
            'person_in_reg2'  : False,
            'person_in_reg3'  : False,
            'direction'       : LFT,   # What's the direction and depth in this frame
            'depth'           : FWD,
            'book_recog'      : False, # Is there a book in frame? Must be above 50%
            'book_under_recog': False, # There may be a book in frame. 25% < book < 50%
            'tv_recog'        : False,
            'tv_under_recog': False,

            'reg_total_area_dict' : {'reg1': 1, 'reg2': 1, 'reg3': 1},
            'reg_bbox_area_dict'  : {'reg1': 1, 'reg2': 1, 'reg3': 1}
        }

        # Take in image and classify
        frame = input_frame_q.get()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image, out_dict = detect_objects(frame_rgb, detection_graph, sess)
        # Image needed to be converted to RGB, but openCV uses BGR.
        image_brg   = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw ROIs
        image_brg = cv2.rectangle(image_brg, region1_start, region1_end, (125, 0, 125), 2)
        image_brg = cv2.rectangle(image_brg, region2_start, region2_end, (125, 0, 125), 2)
        image_brg = cv2.rectangle(image_brg, region3_start, region3_end, (125, 0, 125), 2)

        # Start the image processing by getting the information from the classification
        classes = out_dict['classes']
        scores = out_dict['scores']
        boxes = out_dict['boxes']

        # Break open the NP array so that we can compare the objects to their scores
        classes_index = np.nditer(classes, flags=['f_index'])

        # Reset these every time to ensure accurate current data
        found_obj = []
        person_idx = []
        for id in classes_index:
            # Scores, classes and boxes all have the same index in their respective lists
            current_index = classes_index.index
            # Grab all the objects detected
            if scores[0][current_index] > 0.50:
                found_obj.append(id)
                # We need the index of each human to get their bounding boxes.
                if int(id) is 1:
                    person_idx.append(current_index)
                # If it's a book or TV, say that recognized them
                elif int(id) is 84: # Book
                    frame_dict['book_recog'] = True
                elif int(id) is 72: # TV
                    frame_dict['tv_recog'] = True

            # If a book or TV is detected over 25%, let's say it might be true
            elif id is 84 and scores[0][current_index] > 0.25: # Book
                frame_dict['book_under_recog'] = True
            elif id is 72 and scores[0][current_index] > 0.25: # TV
                frame_dict['tv_under_recog'] = True

        # If we find a person, track their location
        if 1 in found_obj:
            frame_dict['person_in_frame'] = True
            # Normazile the image to work with the scale. Tensorflow coords are (ymin, xmin, ymax, xmax)
            mid_diff_x = []
            mid_diff_y = []
            diff_area = []
            # Forward = 0,0; backward = 0,1; left = 1,0; right = 1,1; respectively
            cur_dir = [0, 0]
            array_idx = 0

            for box_idx in person_idx:
                bounding_box = []
                bounding_box.append(boxes[0][box_idx][0] * HEIGHT)
                bounding_box.append(boxes[0][box_idx][1] * WIDTH)
                bounding_box.append(boxes[0][box_idx][2] * HEIGHT)
                bounding_box.append(boxes[0][box_idx][3] * WIDTH)

                dif_y = bounding_box[2] - bounding_box[0]
                dif_x = bounding_box[3] - bounding_box[1]

                mid_y = bounding_box[0] + (dif_y/2)
                mid_x = bounding_box[1] + (dif_x/2)

                area = dif_x * dif_y

                # Draw the mid point
                image_brg = cv2.circle(image_brg, (int(mid_x), int(mid_y)), 10, (0,255,120), -1)

                frame_dict['reg_total_area_dict'], frame_dict['reg_bbox_area_dict'], total_percent_area = get_regions(bounding_box, area, dif_x, dif_y)

                # If there is a person in the ROI flip to true
                if frame_dict['reg_bbox_area_dict']['reg1'] != 0:
                    frame_dict['person_in_reg1'] = True
                    print('reg1')

                if frame_dict['reg_bbox_area_dict']['reg2'] != 0:
                    frame_dict['person_in_reg2'] = True
                    print('reg2')

                if frame_dict['reg_bbox_area_dict']['reg3'] != 0:
                    frame_dict['person_in_reg3'] = True
                    print('reg3')

                if total_percent_area <= 0.70:
                    # TODO: We may need a semiphore here, but I think that a queue will work.

                    # Assume 1 to 1 indx to person
                    # If is positive, person is moving to their left
                    # If is negative, person is moving to their right
                    mid_diff_x,  old_mid_x = get_dif(mid_x, mid_diff_x, old_mid_x, array_idx)

                    # If is positive, this means that y is decreasing aka moving up in the frame.
                    # If is negative, this means that y is increasing aka moving down in the frame.
                    mid_diff_y,  old_mid_y = get_dif(mid_y, mid_diff_y, old_mid_y, array_idx)

                    # If is positive, this means that area is decreasing aka moving backwards  in the frame.
                    # If is negative, this means that area is increasing aka moving forwardin the frame.
                    diff_area, old_area = get_dif(area, diff_area, old_area, array_idx)

                    try:
                        # If positive and box area is shrinking, means (often) moving back into the distance
                        if mid_diff_y[array_idx] > Y_THRESHOLD and diff_area[array_idx] > AREA_THRESHOLD:
                            frame_dict['depth'] = BAK
                        # If negative and area is increasing, means (often) moving towards the camera
                        elif mid_diff_y[array_idx] < -Y_THRESHOLD and diff_area[array_idx] < -AREA_THRESHOLD:
                            frame_dict['depth'] = FWD
                        # Send a null set if nothing changed
                        else:
                            frame_dict['depth'] = None

                        if mid_diff_x[array_idx] > X_THRESHOLD and diff_area[array_idx] < AREA_THRESHOLD:
                            frame_dict['direction'] = RGT
                        elif mid_diff_x[array_idx] < -X_THRESHOLD and diff_area[array_idx] > -AREA_THRESHOLD:
                            frame_dict['direction'] = LFT
                        else:
                            frame_dict['direction'] = None

                    except IndexError:
                        frame_dict['depth'] = None
                        frame_dict['direction'] = None
                array_idx += 1
                frame_dict['num_people'] += 1
        else:
            frame_dict['person_in_frame'] = False

        output_frame_q.put(image_brg)
        output_dict_q.put(frame_dict)

    sess.close()

# def webcam_controller(webcam, input_frame_q):
#     while(True):
#         err, img = webcam.getFrame()
#         if err == True:
#             input_frame_q.put(img)
#         time.sleep(0.05)

if __name__ == '__main__':
    # Start the multiprocessing
    logger = multiprocessing.log_to_stderr()
    manager = multiprocessing.Manager()
    # logger.setLevel(multiprocessing.SUBDEBUG)
    # Set the managed variables
    old_mid_x = manager.list()
    old_mid_y = manager.list()
    old_area = manager.list()
    # Set queue sizes
    input_frame_q = Queue(maxsize=5 )
    output_frame_q = Queue(maxsize=5 )
    output_dict_q = Queue(maxsize=5 )

    # Set the Pool size and number of workers
    pool = Pool(4 , classification_node, (input_frame_q,  output_frame_q, output_dict_q,
                                          old_mid_x, old_mid_y, old_area))
    # Start the Webcam
    webcam = WebcamVideoStream(src=0).start()
    # webcam_pool = Pool(1, webcam_controller, (webcam, input_frame_q))

    # Init the serial
    # xbee = serial.Serial(PORT, BAUD_RATE)

    # To compensate for distance, draw middle a little larger
    # TODO move to top?

   # print("Quick XBee test")
   # xbee.write(b'0o0\n')
   # time.sleep(2)
   # xbee.write(b'0b1')
   # time.sleep(2)
   # xbee.write(b'0f0\n')

    delay_counter = 0
    book_under_recog_frames = 0
    tv_under_recog_frames = 0

    skip_count = 0

    # Assume
    direction = [[ LFT, LFT, LFT]]
    depth = [[ FWD, FWD, FWD]]

    # Start the tensorflow session
    while(True):
        err, img = webcam.getFrame()
        input_frame_q.put(img)

        # Retreive the dicts and break out the useful ones
        frame_dict = output_dict_q.get()
        for array_idx in range(0, frame_dict['num_people']):
            if frame_dict['direction'] != None:
               # try:
               #     if frame_dict['direction'] == LFT:
               #         direction[array_idx].append(LFT)
               #     elif frame_dict['direction'] == RGT:
               #         direction[array_idx].append(RGT)
               #     direction[array_idx].pop(0)
               #     avg_direction = np.mean(direction[array_idx])
               # except IndexError:
               #     direction.append([ LFT, LFT, LFT])
               #     print('direction ' + direction)
               #     if frame_dict['direction'] == LFT:
               #         direction[array_idx].append(LFT)
               #     elif frame_dict['direction'] == RGT:
               #         direction[array_idx].append(RGT)
               #     direction[array_idx].pop(0)
               #     avg_direction = np.mean(direction[array_idx])

               # if avg_direction > 0.5:
               #     print("Person %s: Right" % (array_idx))
               # elif avg_direction < 0.5:
               #     print("Person %s: Left" % (array_idx))
                if frame_dict['direction'] > 0.5:
                    print("Person %s: Right" % (array_idx))
                elif frame_dict['direction'] < 0.5:
                    print("Person %s: Left" % (array_idx))

            if frame_dict['depth'] != None:
               # try:
               #     if frame_dict['depth'] == FWD:
               #         depth[array_idx].append(FWD)
               #     elif frame_dict['depth'] == BAK:
               #         depth[array_idx].append(BAK)
               #     depth[array_idx].pop(0)
               #     avg_depth = np.mean(depth[array_idx])
               # except IndexError:
               #     depth.append([ FWD, FWD, FWD])
               #     if frame_dict['depth'] == FWD:
               #         depth[array_idx].append(FWD)
               #     elif frame_dict['depth'] == BAK:
               #         depth[array_idx].append(BAK)
               #     depth[array_idx].pop(0)
               #     avg_depth = np.mean(depth[array_idx])

               # if avg_depth > 0.5:
               #     print("Person %s: Backward" % (array_idx))
               # elif avg_depth < 0.5:
               #     print("Person %s: Forward" % (array_idx))
                if frame_dict['depth'] > 0.5:
                    print("Person %s: Backward" % (array_idx))
                elif frame_dict['depth'] < 0.5:
                    print("Person %s: Forward" % (array_idx))

        # Use the bit to change whether or not the light should turn on
        if frame_dict['person_in_reg1'] is True:
            current_lights['light1'] = True
        else:
            current_lights['light1'] = False

        if frame_dict['person_in_reg2'] is True:
            current_lights['light2'] = True
        else:
            current_lights['light2'] = False

        if frame_dict['person_in_reg3'] is True:
            current_lights['light3'] = True
        else:
            current_lights['light3'] = False

        if current_lights['light1'] == True:
        # Send the write command only if they're not on
            if old_lights['light1'] == False:
                print("light 1 on")
                # xbee.write(b'1o0')
                old_lights['light1'] = True
        elif current_lights['light1'] == False:
        # Send the write command only if they're on to turn them off
            if old_lights['light1'] == True:
                print("light 1 off")
                # xbee.write(b'1f0')
                old_lights['light1'] = False

        if current_lights['light2'] == True:
            if old_lights['light2'] == False:
                print("light 2 on")
                # xbee.write(b'2o0')
                old_lights['light2'] = True
        elif current_lights['light2'] == False:
            if old_lights['light2'] == True:
                print("light 2 off")
                # xbee.write(b'2f0')
                old_lights['light2'] = False

        if current_lights['light3'] == True:
            if old_lights['light3'] == False:
                print("light 3 on")
                # xbee.write(b'3o0')
                old_lights['light3'] = True
        elif current_lights['light3'] == False:
            if old_lights['light3'] == True:
                print("light 3 off")
                # xbee.write(b'3f0')
                old_lights['light3'] = False

        if frame_dict['tv_recog'] is True:
            if light_changed_tv == False:
                # xbee.write(b'0b1')
                time.sleep(0.1)
                print("Changing Lights cause TV")

            tv_under_recog_frames = 0
            light_changed_tv = True
        elif frame_dict['tv_under_recog'] is True:
            tv_under_recog_frames += 1

        if (tv_under_recog_frames > TV_RECOG_THRESHOLD and frame_dict['tv_under_recog'] is True) \
            or (frame_dict['tv_under_recog'] is False and frame_dict['tv_recog'] is False):

            if light_changed_tv == True:
                # xbee.write(b'0b4')
                time.sleep(0.1)
                light_changed_tv = False
                print("Changing Lights cause no TV")

        if frame_dict['book_recog'] is True:
            if light_changed_book == False:
                # xbee.write(b'0c1')
                time.sleep(0.1)
                # xbee.write(b'0w5')
                print("Changing Lights cause book")

            book_under_recog_frames = 0
            light_changed_book = True
        elif frame_dict['book_under_recog'] is True:
            book_under_recog_frames += 1

        if (book_under_recog_frames > BOOK_RECOG_THRESHOLD and frame_dict['book_under_recog'] is True) \
            or (frame_dict['book_under_recog'] is False and frame_dict['book_recog'] is False):

            if light_changed_book == True:
                print("Changing Lights cause no book")
                # xbee.write(b'0c4')
                time.sleep(0.1)
                # xbee.write(b'0w4')
                light_changed_book = False

        if delay_counter == TIME_OUT:
            # xbee.write(b'0f0')
            delay_counter = 0
            current_lights = { 'light1': False, 'light2': False, 'light3': False}
        elif frame_dict['person_in_frame'] is False:
            delay_counter += 1

        img = output_frame_q.get()
        cv2.imshow("img", img)

        k = cv2.waitKey(60) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    # xbee.write(b'0f0\n')
    time.sleep(1)
    webcam.stop()
    pool.terminate()
