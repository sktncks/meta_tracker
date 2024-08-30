import cv2
import os
import time
from functions import main_function, detection_point_check, load_object_data, get_data_size
from sub_functions import printProgress, print_input_info, print_output_info

def video_editing(metadata_list, video_file, # input path info
                  output_save_path, output_filename, video_extension, output_size_rate,# output info
                  record_start, record_end, # recording time info
                  init_box_color, BorderThickness, # box info
                  init_tail_color, tail_size, tail_thickness, # tail info
                  init_text_color, text_scale, text_thickness, # text info
                  visualization, visualization_speed):
    
    print_input_info(metadata_list, video_file, "Video")
    
    print('\033[35m' + 'Initial setting process (2/3)' + '\033[0m')
    start = time.time()

    # Load detection point and all object data
    detection_point = detection_point_check(metadata_list[0])
    all_data = [load_object_data(fp) for fp in metadata_list]
    all_timestamps = [list(data.keys()) for data in all_data]

    # Video setup
    cap = cv2.VideoCapture(video_file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    dps = get_data_size(metadata_list, 10)
    width, hight = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Output video name checking
    out_path = output_save_path
    os.makedirs(out_path, exist_ok=True)
    while output_filename + video_extension in os.listdir(out_path):
        output_filename += "1"

    # Output video setting
    
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
    count_f = 0
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
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        #사이즈 조절 -- 영상이 안만들어짐.
        frame = cv2.resize(frame, None, fx = output_size_rate, fy = output_size_rate)
        
        next_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if current_frame + int(fps / dps[file_index]) == next_frame:
            timestamp_index += 1
            current_frame = next_frame

        if timestamp_index == len(timestamp_list):
            file_index += 1
            if file_index >= len(metadata_list):
                break
            timestamp_index = 0
            timestamp_list = all_timestamps[file_index]

        current_timestamp = timestamp_list[timestamp_index]
        box_data = all_data[file_index][current_timestamp]

        main_function(frame, box_data, hight, width, detection_point,
                      color_list, input_list,
                      object_trails, bf_frame_ids, frame_count)

        if start_frame <= next_frame < end_frame:
            count += 1
            out.write(frame)
            printProgress(count, set_frame, "Progress:", "Complete")
        elif next_frame < start_frame:
            count_f += 1
            printProgress(count_f, start_frame, "Loading:", "Done")
        elif end_frame == next_frame:
            break

        if visualization:
            cv2.imshow('frame', frame)
            if cv2.waitKey(visualization_speed) & 0xFF == ord('q'):
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Total Time: {time.time() - start} seconds")
    print("---------------------------------------------------------------------------------")
    print_output_info(output_save_path, output_filename)