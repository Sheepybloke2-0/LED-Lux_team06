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

AREA_THRESHOLD = 2000
X_THRESHOLD  = 15
Y_THRESHOLD  = 1

# Regions
region1_start = (0,0)
region1_end = (320,720)
region1_area = 230400

region2_start = (320,0)
region2_end = (960,720)
region2_area = 460800

region3_start = (960,0)
region3_end = (1280,720)
region3_area = 230400

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
    # logger.setLevel(multiprocessing.SUBDEBUG)

    # Set queue sizes
    input_frame_q = Queue(maxsize=5 )
    output_frame_q = Queue(maxsize=5)
    output_dict_q = Queue(maxsize=5)

    # Set the Pool size and number of workers
    pool = Pool(2 , worker_node, (input_frame_q, output_frame_q, output_dict_q))

    # Start the Webcam
    webcam = WebcamVideoStream(src=0).start()

    # Init the serial
    xbee = serial.Serial(PORT, BAUD_RATE)

    # To compensate for distance, draw middle a little larger
    # TODO move to top?

    print("Quick XBee test")
    xbee.write(b'0o0\n')
    time.sleep(2)
    xbee.write(b'0b1')
    time.sleep(2)
    xbee.write(b'0f0\n')

    delay_counter = 0
    book_under_recog_frames = 0
    tv_under_recog_frames = 0
    old_mid_x = [0]
    old_mid_y = [0]
    old_area = [0]
    old_reg_bbox_area = [{'reg1': 0, 'reg2': 0, 'reg3': 0}]
    # Assume
    direction = [[ LFT, LFT, LFT]]
    depth = [[ FWD, FWD, FWD]]
    dist = [ 0 ]

    # Start the tensorflow session
    while(1):
        err, img = webcam.getFrame()
        if err == True:
            input_frame_q.put(img)

            # Retreive the dicts and break out the useful ones
            out_dict = output_dict_q.get()
            classes = out_dict['classes']
            scores = out_dict['scores']
            boxes = out_dict['boxes']

            # Break open the NP array so that we can compare the objects to their scores
            classes_index = np.nditer(classes, flags=['f_index'])
            found_obj = []
            person_idx = []
            tv_in_frame = False
            book_in_frame = False
            for id in classes_index:
                current_index = classes_index.index
                if id == 84 and scores[0][current_index] > 0.25 and book_under_recog_frames <= BOOK_RECOG_THRESHOLD: #book
                    book_under_recog_frames += 1
                    book_in_frame = True
                elif id == 72 and scores[0][current_index] > 0.25 and tv_under_recog_frames <= TV_RECOG_THRESHOLD: #tv
                    tv_under_recog_frames += 1
                    tv_in_frame = True

                # There's almost always a 1, just very low probablility. Ensure i is greater than 50%
                if scores[0][current_index] > 0.50:
                    # Add all found objects to a List
                    found_obj.append(id)
                    if id == 1:
                        person_idx.append(current_index)

            img_brg   = cv2.cvtColor(output_frame_q.get(), cv2.COLOR_RGB2BGR)

            # Draw ROI we want.
            cv2.rectangle(img_brg, region1_start, region1_end, (125, 0, 125), 2)
            cv2.rectangle(img_brg, region2_start, region2_end, (125, 0, 125), 2)
            cv2.rectangle(img_brg, region3_start, region3_end, (125, 0, 125), 2)

            # If there is person found, do some checking to get their location and turn on the proper lights
            if 1 in found_obj:
                # Normazile the image to work with the scale. Tensorflow coords are (ymin, xmin, ymax, xmax)
                mid_diff_x = []
                mid_diff_y = []
                diff_area = []
                # Forward = 0,0; backward = 0,1; left = 1,0; right = 1,1; respectively
                cur_dir = [0, 0]
                array_idx = 0
                person_in_reg1 = False
                person_in_reg2 = False
                person_in_reg3 = False

                for box_idx in person_idx:
                    # TODO: Break into a function and multiplex?
                    bounding_box = []
                    bounding_box.append(boxes[0][box_idx][0] * HEIGHT)
                    bounding_box.append(boxes[0][box_idx][1] * WIDTH)
                    bounding_box.append(boxes[0][box_idx][2] * HEIGHT)
                    bounding_box.append(boxes[0][box_idx][3] * WIDTH)

                    dif_y = bounding_box[2] - bounding_box[0]
                    dif_x = bounding_box[3] - bounding_box[1]

                    # Draw point halfway down the image in the center of the box
                    mid_y = bounding_box[0] + (dif_y/2)
                    mid_x = bounding_box[1] + (dif_x/2)
                    # Calc area
                    area = dif_x * dif_y

                    # Draw the mid point
                    cv2.circle(img_brg, (int(mid_x), int(mid_y)), 10, (0,255,120), -1)

                    reg_total_area_dict, reg_bbox_area_dict, total_percent_area = get_regions(bounding_box, area, dif_x, dif_y)

                    try:
                        temp = old_reg_bbox_area[array_idx]['reg1']
                    except IndexError:
                        old_reg_bbox_area.append({'reg1': 0, 'reg2': 0, 'reg3': 0})

                    # If there is a person in the ROI flip to true
                    # Ensure theres activity in the ROI
                    if reg_bbox_area_dict['reg1'] != 0:
                        person_in_reg1 = True

                    # Ensure theres activity in the ROI
                    if reg_bbox_area_dict['reg2'] != 0:
                        person_in_reg2 = True

                    # Ensure theres activity in the ROI
                    if reg_bbox_area_dict['reg3'] != 0:
                        person_in_reg3 = True

                    if total_percent_area <= 0.70:
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
                                cur_dir[0] = 1
                            # If negative and area is increasing, means (often) moving towards the camera
                            elif mid_diff_y[array_idx] < -Y_THRESHOLD and diff_area[array_idx] < -AREA_THRESHOLD:
                                    cur_dir[0] = 0
                            # Send a null set if nothing changed
                            else:
                                cur_dir[0] = None

                            if mid_diff_x[array_idx] > X_THRESHOLD and diff_area[array_idx] < AREA_THRESHOLD:
                                cur_dir[1] = 1
                            elif mid_diff_x[array_idx] < -X_THRESHOLD and diff_area[array_idx] > -AREA_THRESHOLD:
                                cur_dir[1] = 0
                            else:
                                cur_dir[1] = None

                        except IndexError:
                            continue

                        if cur_dir[1] != None:
                            try:
                                if cur_dir[1] == 0:
                                    direction[array_idx].append(LFT)
                                elif cur_dir[1] == 1:
                                    direction[array_idx].append(RGT)
                                direction[array_idx].pop(0)
                                avg_direction = np.mean(direction[array_idx])
                            except IndexError:
                                direction.append([ LFT, LFT, LFT])
                                print(array_idx)
                                print(direction)
                                if cur_dir[1] == 0:
                                    direction[array_idx].append(LFT)
                                elif cur_dir[1] == 1:
                                    direction[array_idx].append(RGT)
                                direction[array_idx].pop(0)
                                avg_direction = np.mean(direction[array_idx])

                            if avg_direction > 0.5:
                                print("Person %s: Right" % (array_idx))
                            elif avg_direction < 0.5:
                                print("Person %s: Left" % (array_idx))

                        if cur_dir[0] != None:
                            try:
                                if cur_dir[0] == 0:
                                    depth[array_idx].append(FWD)
                                elif cur_dir[0] == 1:
                                    depth[array_idx].append(BAK)
                                depth[array_idx].pop(0)
                                avg_depth = np.mean(depth[array_idx])
                            except IndexError:
                                depth.append([ FWD, FWD, FWD])
                                if cur_dir[0] == 0:
                                    depth[array_idx].append(FWD)
                                elif cur_dir[0] == 1:
                                    depth[array_idx].append(BAK)
                                depth[array_idx].pop(0)
                                avg_depth = np.mean(depth[array_idx])

                            # This sort of distance tracking works decent for a single person, but breaks down with more
                            if avg_depth > 0.5:
                                print("Person %s: Backward" % (array_idx))
                            elif avg_depth < 0.5:
                                print("Person %s: Forward" % (array_idx))

                    array_idx += 1

                # Use the bit to change whether or not the light should turn on
                if person_in_reg1 is True:
                    current_lights['light1'] = True
                else:
                    current_lights['light1'] = False

                if person_in_reg2 is True:
                    current_lights['light2'] = True
                else:
                    current_lights['light2'] = False

                if person_in_reg3 is True:
                    current_lights['light3'] = True
                else:
                    current_lights['light3'] = False

                print(current_lights)
                print(old_lights)
            else:
                delay_counter += 1

            if 72 in found_obj:
                if light_changed_tv == False:
                    xbee.write(b'0b1')
                    time.sleep(0.1)
                    print("Changing Lights cause TV")
                tv_under_recog_frames = 0
                light_changed_tv = True
            elif tv_in_frame != True:
                tv_under_recog_frames += 1

            if 84 in found_obj:
                if light_changed_book == False:
                    xbee.write(b'0c1')
                    time.sleep(0.1)
                    xbee.write(b'0w5')
                    print("Changing Lights cause book")
                book_under_recog_frames = 0
                light_changed_book = True
            elif book_in_frame != True:
                book_under_recog_frames += 1

            if book_under_recog_frames > BOOK_RECOG_THRESHOLD and book_in_frame == True:
                print("Changing Lights cause no book")
                xbee.write(b'0c4')
                time.sleep(0.1)
                xbee.write(b'0w4')
                book_in_frame = False

            if tv_under_recog_frames > TV_RECOG_THRESHOLD and tv_in_frame == True:
                xbee.write(b'0b4')
                time.sleep(0.1)
                tv_in_frame = False
                print("Changing Lights cause no TV")

            if current_lights['light1'] == True:
                # Send the write command only if they're not on
                if old_lights['light1'] == False:
                    print("light on")
                    xbee.write(b'1o0')
                    old_lights['light1'] = True
            elif current_lights['light1'] == False:
                # Send the write command only if they're on to turn them off
                if old_lights['light1'] == True:
                    print("light off")
                    xbee.write(b'1f0')
                    old_lights['light1'] = False

            if current_lights['light2'] == True:
                if old_lights['light2'] == False:
                    print("light on")
                    xbee.write(b'2o0')
                    old_lights['light2'] = True
            elif current_lights['light2'] == False:
                if old_lights['light2'] == True:
                    print("light off")
                    xbee.write(b'2f0')
                    old_lights['light2'] = False

            if current_lights['light3'] == True:
                if old_lights['light3'] == False:
                    print("light on")
                    xbee.write(b'3o0')
                    old_lights['light3'] = True
            elif current_lights['light3'] == False:
                if old_lights['light3'] == True:
                    print("light off")
                    xbee.write(b'3f0')
                    old_lights['light3'] = False

            if delay_counter == TIME_OUT:
                xbee.write(b'0f0')
                delay_counter = 0
                current_lights = { 'light1': False, 'light2': False, 'light3': False}

            # old_lights = current_lights
            cv2.imshow("img", img_brg)
        else:
            print("Check if the camera is connected to the system!")
            break

        k = cv2.waitKey(60) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    xbee.write(b'0f0\n')
    time.sleep(1)
    webcam.stop()
    pool.terminate()
