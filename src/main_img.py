import cv2
import os
import time
from datetime import datetime
from functions import main_function,detection_point_check, load_object_data, get_data_size, time_to_second
from sub_functions import printProgress, print_input_info, print_output_info

def imgtovideo(metadata_list, image_file, # input path info
                   output_save_path, output_filename, video_extension, output_size_rate, # output info
                   record_start, record_end, # recording time info
                   init_box_color, BorderThickness, # box info
                   init_tail_color, tail_size, tail_thickness, # tail info
                   init_text_color, text_scale, text_thickness, # text info
                   visualization, visualization_speed):
    
    print_input_info(metadata_list, image_file, "Snapshot")
    
    print('\033[35m' + 'Initial setting process (2/3)' + '\033[0m')
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
    image = cv2.resize(image, None, fx = output_size_rate, fy = output_size_rate) 
    if image is None:
        raise FileNotFoundError(f"Image file {image_file} not found.")
    dps = get_data_size(metadata_list, 10)
    hight, width = image.shape[:2]
    
    # Output img name checking
    out_path = output_save_path
    os.makedirs(out_path, exist_ok=True)
    while output_filename + video_extension in os.listdir(out_path):
        output_filename += "1"

    # Output img setting
    
    output_file = os.path.join(out_path, output_filename + video_extension)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, hight))

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
    timestamp_list = all_timestamps[file_index]

    # Trail
    object_trails = {}
    bf_frame_ids = []
    frame_count = {}
    color_list = [init_box_color, init_text_color, init_tail_color]
    input_list = [BorderThickness, text_scale, text_thickness, tail_size, tail_thickness]
    print('\033[31m' + 'DONE' + '\033[0m')
    print("--------------------------------------------------------------------------------------------")
    print('\033[35m' + 'Main process (3/3)' + '\033[0m')
    while current_frame < end_frame:
        frame = image.copy()
        current_timestamp = timestamp_list[timestamp_index]
        box_data = all_data[file_index][current_timestamp]
        
        #time print on video
        current_datetime = str(datetime.fromtimestamp(float(current_timestamp)))
        cv2.putText(frame, current_datetime, (5, 20), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 153, 255), 1, cv2.LINE_AA)

        main_function(frame, box_data, hight, width, detection_point,
                      color_list, input_list,
                      object_trails, bf_frame_ids, frame_count)

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

    out.release()
    cv2.destroyAllWindows()
    print(f"Total Time: {time.time() - start} seconds")
    print("---------------------------------------------------------------------------------")
    print_output_info(output_save_path, output_filename)