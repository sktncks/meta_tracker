import cv2
import os
import time
from datetime import datetime
from extraction_from_metadata import detection_point_check, load_object_data, get_data_size, box_point_gen, time_to_second
from input_check import calculate_total_time
from progressbar import printProgress

def imgtovideo(metadata_list, image_file, # input path info
                   output_save_path, output_filename, video_extension, # output info
                   record_start, record_end, # recording time info
                   init_box_color, BorderThickness, # box info
                   init_tail_color, tail_size, tail_thickness, # tail info
                   init_text_color, text_scale, text_thickness, # text info
                   visualization, visualization_speed):
    print("Initial process")
    start = time.time()

    # Load detection point and all object data
    detection_point = detection_point_check(metadata_list[0])
    all_data = [load_object_data(fp) for fp in metadata_list]
    all_timestamps = [list(data.keys()) for data in all_data]
    
    stamp_count = 0
    for x in all_timestamps:
        stamp_count += len(x)
    total_second  = time_to_second(metadata_list)
    fps= int(stamp_count / total_second)

    # Image setup
    image = cv2.imread(image_file)
    if image is None:
        raise FileNotFoundError(f"Image file {image_file} not found.")
    h, w = image.shape[:2]
    dps = get_data_size(metadata_list, 10)

    # Output video name checking
    out_path = output_save_path
    os.makedirs(out_path, exist_ok=True)
    while output_filename + video_extension in os.listdir(out_path):
        output_filename += "1"

    # Output video setting
    output_file = os.path.join(out_path, output_filename + video_extension)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter(output_file, fourcc, fps, (w, h))

    # Time calculations
    start_frame = (int(record_start[:2]) * 3600 + int(record_start[2:4]) * 60 + int(record_start[4:6])) * fps
    end_frame = (int(record_end[:2]) * 3600 + int(record_end[2:4]) * 60 + int(record_end[4:6])) * fps
    set_frame = end_frame - start_frame

    # Frame processing
    current_frame = 0
    timestamp_index = 0
    file_index = 0
    count = 0
    new_count = 0
    h_rate = h / 65535
    w_rate = w / 65535
    timestamp_list = all_timestamps[file_index]

    # Trail
    object_trails = {}
    bf_frame_ids = []
    frame_count = {}
    print("Done")
    ####
    while current_frame < end_frame:
        frame = image.copy()
        current_timestamp = timestamp_list[timestamp_index]
        box_data = all_data[file_index][current_timestamp]
        
        #time print on video
        current_datetime = str(datetime.fromtimestamp(float(current_timestamp)))
        cv2.putText(frame, current_datetime, (5, 20), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 153, 255), 1, cv2.LINE_AA)

        for box in box_data:
            obj_id = box['id']
            x, w_box = map(lambda val: val * w_rate, [box['x'], box['w']])
            y, h_box = map(lambda val: val * h_rate, [box['y'], box['h']])
            center_point = (int(x), int(y))

            if detection_point == "2":
                pt_lu = (int(x - w_box / 2), int(y - h_box))
                pt_ld = (int(x - w_box / 2), int(y))
                pt_rd = (int(x + w_box / 2), int(y))
                pt_ru = (int(x + w_box / 2), int(y - h_box))
            else:
                pt_lu = (int(x - w_box / 2), int(y - h_box / 2)) 
                pt_ld = (int(x - w_box / 2), int(y + h_box / 2))
                pt_rd = (int(x + w_box / 2), int(y + h_box / 2)) 
                pt_ru = (int(x + w_box / 2), int(y - h_box / 2))

            pt_lu_r, pt_lu_d, pt_ld_r, pt_ld_u, pt_ru_l, pt_ru_d, pt_rd_l, pt_rd_u = box_point_gen(pt_lu, pt_ld, pt_ru, pt_rd, w_box, h_box)

            box_color = init_box_color
            text_color = init_text_color
            tail_color = init_tail_color

            # Draw bounding box and text for object
            if obj_id in bf_frame_ids and obj_id not in frame_count:
                cv2.line(frame, pt_lu, pt_lu_r, box_color, BorderThickness)
                cv2.line(frame, pt_lu, pt_lu_d, box_color, BorderThickness)
                cv2.line(frame, pt_ld, pt_ld_r, box_color, BorderThickness)
                cv2.line(frame, pt_ld, pt_ld_u, box_color, BorderThickness)
                cv2.line(frame, pt_rd, pt_rd_l, box_color, BorderThickness)
                cv2.line(frame, pt_rd, pt_rd_u, box_color, BorderThickness)
                cv2.line(frame, pt_ru, pt_ru_l, box_color, BorderThickness)
                cv2.line(frame, pt_ru, pt_ru_d, box_color, BorderThickness)
                cv2.putText(frame, box['id'], pt_lu, cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, text_thickness, cv2.LINE_AA)
            elif obj_id not in bf_frame_ids and obj_id not in frame_count:
                frame_count[obj_id] = 10
                cv2.rectangle(frame, pt_lu, pt_rd, (0, 0, 255), BorderThickness)
                cv2.putText(frame, box['id'], pt_lu, cv2.FONT_HERSHEY_SIMPLEX, text_scale, (0, 0, 255), text_thickness, cv2.LINE_AA)
            else:
                frame_count[obj_id] -= 1
                if frame_count[obj_id] == 0:
                    del frame_count[obj_id]
                cv2.rectangle(frame, pt_lu, pt_rd, (0, 0, 255), BorderThickness)
                cv2.putText(frame, box['id'], pt_lu, cv2.FONT_HERSHEY_SIMPLEX, text_scale, (0, 0, 255), text_thickness, cv2.LINE_AA)

            # Track object trails
            if obj_id not in object_trails:
                object_trails[obj_id] = []
            object_trails[obj_id].append((x, y))
            if len(object_trails[obj_id]) > tail_size:
                object_trails[obj_id].pop(0)

            for k in range(1, len(object_trails[obj_id])):
                tail_pt1 = (int(object_trails[obj_id][k - 1][0]), int(object_trails[obj_id][k - 1][1]))
                tail_pt2 = (int(object_trails[obj_id][k][0]), int(object_trails[obj_id][k][1]))
                cv2.line(frame, tail_pt1, tail_pt2, tail_color, tail_thickness)

            bf_frame_ids.append(obj_id)

        if start_frame <= current_frame < end_frame:
            new_count += 1
            out.write(frame)
            printProgress(new_count, set_frame, "Progress:", "Complete")
        elif current_frame < start_frame:
            count += 1
            printProgress(count, start_frame, "Loading:", "Done")
        
        current_frame += 1
        timestamp_index = (timestamp_index + 1) % len(timestamp_list)
        if timestamp_index == 0:
            file_index = (file_index + 1) % len(metadata_list)
            timestamp_list = all_timestamps[file_index]

        if visualization:
            cv2.imshow('frame', frame)
            if cv2.waitKey(visualization_speed) & 0xFF == ord('q'):
                break
                ##
    out.release()
    cv2.destroyAllWindows()
    print(f"Total Time: {time.time() - start} seconds")