from sub_functions import box_point_gen
import xml.etree.ElementTree as ET
import cv2


def main_function(frame, 
                  box_data, hight, width, detection_point,
                  color_list, #[box_color , text_color, tail_color]
                  input_list, #[BorderThickness, text_scale, text_thickness, tail_size, tail_thickness]
                  object_trails, bf_frame_ids, frame_count):
    
    h_rate = hight / 65535
    w_rate = width / 65535

    for box in box_data:
        obj_id = box['id']
        x, w = map(lambda val: val * w_rate, [box['x'], box['w']])
        y, h = map(lambda val: val * h_rate, [box['y'], box['h']])
        if detection_point == "2":
            pt_lu = (int(x - w / 2), int(y - h))
            pt_ld = (int(x - w / 2), int(y))
            pt_rd = (int(x + w / 2), int(y))
            pt_ru = (int(x + w / 2), int(y - h))
        else:
            pt_lu = (int(x - w / 2), int(y - h / 2))
            pt_ld = (int(x - w / 2), int(y + h / 2))
            pt_rd = (int(x + w / 2), int(y + h / 2)) 
            pt_ru = (int(x + w / 2), int(y - h / 2))

        pt_lu_r, pt_lu_d, pt_ld_r, pt_ld_u, pt_ru_l, pt_ru_d, pt_rd_l, pt_rd_u = box_point_gen(pt_lu, pt_ld, pt_ru, pt_rd, w, h)

        box_color = color_list[0]
        text_color = color_list[1]
        tail_color = color_list[2]

        if obj_id in bf_frame_ids and obj_id not in frame_count:
            cv2.line(frame, pt_lu, pt_lu_r, box_color, input_list[0])
            cv2.line(frame, pt_lu, pt_lu_d, box_color, input_list[0])
            cv2.line(frame, pt_ld, pt_ld_r, box_color, input_list[0])
            cv2.line(frame, pt_ld, pt_ld_u, box_color, input_list[0])
            cv2.line(frame, pt_rd, pt_rd_l, box_color, input_list[0])
            cv2.line(frame, pt_rd, pt_rd_u, box_color, input_list[0])
            cv2.line(frame, pt_ru, pt_ru_l, box_color, input_list[0])
            cv2.line(frame, pt_ru, pt_ru_d, box_color, input_list[0])
            cv2.putText(frame, box['id'], pt_lu, cv2.FONT_HERSHEY_SIMPLEX, input_list[1], text_color, input_list[2], cv2.LINE_AA)
        elif obj_id not in bf_frame_ids and obj_id not in frame_count:
            frame_count[obj_id] = 10
            cv2.rectangle(frame, pt_lu, pt_rd, (0, 0, 255), input_list[0])
            cv2.putText(frame, box['id'], pt_lu, cv2.FONT_HERSHEY_SIMPLEX, input_list[1], (0, 0, 255), input_list[2], cv2.LINE_AA)
        else:
            frame_count[obj_id] -= 1
            if frame_count[obj_id] == 0:
                del frame_count[obj_id]
            cv2.rectangle(frame, pt_lu, pt_rd, (0, 0, 255), input_list[0])
            cv2.putText(frame, box['id'], pt_lu, cv2.FONT_HERSHEY_SIMPLEX, input_list[1], (0, 0, 255), input_list[2], cv2.LINE_AA)
        
        if obj_id not in object_trails:
            object_trails[obj_id] = []
        object_trails[obj_id].append((x, y))
        if len(object_trails[obj_id]) > input_list[3]:
            object_trails[obj_id].pop(0)

        for k in range(1, len(object_trails[obj_id])):
            tail_pt1 = (int(object_trails[obj_id][k - 1][0]), int(object_trails[obj_id][k - 1][1]))
            tail_pt2 = (int(object_trails[obj_id][k][0]), int(object_trails[obj_id][k][1]))
            cv2.line(frame, tail_pt1, tail_pt2, tail_color, input_list[4])

        bf_frame_ids.append(obj_id)

def detection_point_check(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    detection_point = 1
    try:
        detection_point = root.find("vca/vca_cfg/detection_point").text
    except Exception:
        detection_point = 1
    return detection_point

def load_timestamps(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    return [vca.find("vca_hdr/timestamp").text for vca in root.findall("vca")]

def load_object_data(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    data = {}
    for vca in root.findall("vca"):
        timestamp = vca.find("vca_hdr/timestamp").text
        objects = [
            {
                "id": obj.find("id").text,
                "x": int(obj.find("bb/x").text),
                "y": int(obj.find("bb/y").text),
                "w": int(obj.find("bb/w").text),
                "h": int(obj.find("bb/h").text),
            }
            for obj in vca.findall("objects/object")
        ]
        data[timestamp] = objects
    return data

def get_data_size(filepath_list, timeperfile):
    return [len(load_timestamps(fp)) / (timeperfile * 60) for fp in filepath_list]

def time_to_second(metadata_list):
    time_h, time_m, time_s = 0, 0, 0
    for metadata in metadata_list:
        time = metadata.split("_")[-1].split(".")[0]
        time_n = int(time[:-1])
        time_hms = time[-1]
        if time_hms == "h":
            time_h += time_n
        elif time_hms == "m":
            time_m += time_n
            if time_m >= 60: 
                time_m -= 60
                time_h += 1
        else:
            time_s += time_n
            if time_s >= 60:
                time_s -= 60
                time_m += 1
    total_second = ((time_h * 3600) + (time_m * 60) + time_s)

    return total_second