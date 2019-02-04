from mvnc import mvncapi as mvnc
import cv2
import numpy as np
import sys
import threading
import copy

class Camera:
    def sigmoid(self, x):
        return 1.0 / (1 + np.exp(x * -1.0))


    def calculate_overlap(self, x1, w1, x2, w2):
        box1_coordinate = max(x1 - w1 / 2.0, x2 - w2 / 2.0)
        box2_coordinate = min(x1 + w1 / 2.0, x2 + w2 / 2.0)
        overlap = box2_coordinate - box1_coordinate
        return overlap


    def calculate_iou(self, box, truth):
        # calculate the iou intersection over union by first calculating the overlapping height and width
        width_overlap = calculate_overlap(box[0], box[2], truth[0], truth[2])
        height_overlap = calculate_overlap(box[1], box[3], truth[1], truth[3])
        # no overlap
        if width_overlap < 0 or height_overlap < 0:
            return 0

        intersection_area = width_overlap * height_overlap
        union_area = box[2] * box[3] + truth[2] * truth[3] - intersection_area
        iou = intersection_area / union_area
        return iou


    def apply_nms(self, boxes):
        # sort the boxes by score in descending order
        sorted_boxes = sorted(boxes, key=lambda d: d[7])[::-1]
        high_iou_objs = dict()
        # compare the iou for each of the detected objects
        for current_object in range(len(sorted_boxes)):
            if current_object in high_iou_objs:
                continue

            truth = sorted_boxes[current_object]
            for next_object in range(current_object + 1, len(sorted_boxes)):
                if next_object in high_iou_objs:
                    continue
                box = sorted_boxes[next_object]
                iou = calculate_iou(box, truth)
                if iou >= self.IOU_THRESHOLD:
                    high_iou_objs[next_object] = 1

        # filter and sort detected items
        filtered_result = list()
        for current_object in range(len(sorted_boxes)):
            if current_object not in high_iou_objs:
                filtered_result.append(sorted_boxes[current_object])
        return filtered_result


    def post_processing(self, output, original_img):
        num_classes = 1
        num_grids = 13
        num_anchor_boxes = 5
        original_results = output.astype(np.float32)

        # Tiny Yolo V2 uses a 13 x 13 grid with 5 anchor boxes for each grid cell.
        # This specific model was trained with the VOC Pascal data set and is comprised of 20 classes

        original_results = np.reshape(original_results, (13, 13, 30))

        # The 125 results need to be re-organized into 5 chunks of 25 values
        # 20 classes + 1 score + 4 coordinates = 25 values
        # 25 values for each of the 5 anchor bounding boxes = 125 values
        reordered_results = np.zeros((13 * 13, 5, 6))

        index = 0
        for row in range( num_grids ):
            for col in range( num_grids ):
                for b_box_voltron in range(30):
                    b_box = row * num_grids + col
                    b_box_num = int(b_box_voltron / 6)
                    b_box_info = b_box_voltron % 6
                    reordered_results[b_box][b_box_num][b_box_info] = original_results[row][col][b_box_voltron]

        # shapes for the 5 Tiny Yolo v2 bounding boxes
        anchor_boxes = [1.08,1.19, 3.42,4.41, 6.63,11.38, 9.42,5.11, 16.62,10.52]

        boxes = list()
        # iterate through the grids and anchor boxes and filter out all scores which do not exceed the self.DETECTION_THRESHOLD
        for row in range(num_grids):
            for col in range(num_grids):
                for anchor_box_num in range(num_anchor_boxes):
                    box = list()
                    class_list = list()
                    current_score_total = 0
                    # calculate the coordinates for the current anchor box
                    box_x = (col + sigmoid(reordered_results[row * 13 + col][anchor_box_num][0])) / 13.0
                    box_y = (row + sigmoid(reordered_results[row * 13 + col][anchor_box_num][1])) / 13.0
                    box_w = (np.exp(reordered_results[row * 13 + col][anchor_box_num][2]) *
                             anchor_boxes[2 * anchor_box_num]) / 13.0
                    box_h = (np.exp(reordered_results[row * 13 + col][anchor_box_num][3]) *
                             anchor_boxes[2 * anchor_box_num + 1]) / 13.0

                    # find the class with the highest score
                    for class_enum in range(num_classes):
                        class_list.append(reordered_results[row * 13 + col][anchor_box_num][5 + class_enum])

                    # perform a Softmax on the classes
                    highest_class_score = max(class_list)
                    for current_class in range(len(class_list)):
                        class_list[current_class] = np.exp(class_list[current_class] - highest_class_score)

                    current_score_total = sum(class_list)
                    for current_class in range(len(class_list)):
                        class_list[current_class] = class_list[current_class] * 1.0 / current_score_total

                    # probability that the current anchor box contains an item
                    object_confidence = sigmoid(reordered_results[row * 13 + col][anchor_box_num][4])
                    # highest class score detected for the object in the current anchor box
                    highest_class_score = max(class_list)
                    # index of the class with the highest score
                    class_w_highest_score = class_list.index(max(class_list)) + 1
                    # the final score for the detected object
                    final_object_score = object_confidence * highest_class_score

                    box.append(box_x)
                    box.append(box_y)
                    box.append(box_w)
                    box.append(box_h)
                    box.append(class_w_highest_score)
                    box.append(object_confidence)
                    box.append(highest_class_score)
                    box.append(final_object_score)

                    # filter out all detected objects with a score less than the threshold
                    if final_object_score > self.DETECTION_THRESHOLD:
                        boxes.append(box)

        # gets rid of all duplicate boxes using non-maximal suppression
        results = apply_nms(boxes)

        print(results)

        image_width = original_img.shape[1]
        image_height = original_img.shape[0]

        j = 0

        _results = copy.deepcopy(results)
        for box in _results:
            box_xmin = (box[0] - box[2] / 2.0)
            box_xmax = (box[0] + box[2] / 2.0)

            avg = (box_xmin + box_xmax) / 2

            if avg < 0.35 or avg > 0.65:
                print("Result removed at avg x: " + avg)
                del results[j]

            j += 1


        gymin = 100

        for box in results:
            ymin = (box[1] - box[3] / 2.0) # essentially box y min divided by image height (percent from bottom of view)

            if ymin < gymin:
                gymin = ymin

        return (0 if (len(results) == 0) else gymin)

    def __init__(self, _gp, _dt, _iou, _lab):
        """
        GRAPH_PATH = "../files/main.graph"
        DETECTION_THRESHOLD = 0.20
        IOU_THRESHOLD = 0.20
        LABELS = {0: "bg", 1: "dandelion"}
        """

        self.GRAPH_PATH = _gp
        self.DETECTION_THRESHOLD = _dt
        self.IOU_THRESHOLD = _iou
        self.LABELS = _lab

        mvnc.global_set_option(mvnc.GlobalOption.RW_LOG_LEVEL, 2)

        # enumerate all devices
        devices = mvnc.enumerate_devices()
        if len(devices) == 0:
            print("No devices found")
            quit()

        # use the first device found
        self.device = mvnc.Device(devices[0])
        # open the device
        self.device.open()

        # load the model from the disk
        with open(self.GRAPH_PATH, mode="rb") as f:
            graph_in_memory = f.read()

        self.graph = mvnc.Graph(self.GRAPH_PATH)

        # create the input and output fifos
        self.fifo_in, self.fifo_out = graph.allocate_with_fifos(device, graph_in_memory)

        self.cap = cv2.VideoCapture(0)

    def run():
        #while True:

        # read an image in bgr format
        ret, img = self.cap.read()
        original_img = img

        # bgr input scaling
        img = np.divide(img, 255.0)
        resized_img = cv2.resize(img, (416, 416), cv2.INTER_LINEAR)

        # transpose the image to rgb
        resized_img = resized_img[:, :, ::-1]
        resized_img = resized_img.astype(np.float32)

        # make an inference
        self.graph.queue_inference_with_fifo_elem(self.fifo_in, self.fifo_out, resized_img, "user object")
        # get the result
        output, userobj = self.fifo_out.read_elem()

        # Tiny Yolo V2 requires post processing to filter out duplicate objects and low score objects
        return self.post_processing(output, original_img)
