# 1. 메타 데이터가 폴더 주소인지, 리스트인지, 폴더 주소인경우 뒤에 *이 들어가있는지 확인
    # 1.1 폴더 주소면 파일 주소들을 리스트에 넣기 v
    # 1.2 리스트면 패스 v
    # 1.3 폴더 주소 뒤에 * 이 없으면 추가 v
        # 만약에 주소에 xml파일이 없으면 경고 v
# 2. video file 정보 확인
    # 2.1. 비디오 폴더 주소만 왔을때 비디오 풀 주소로 변경
    # 2.2. 비디오 파일이 폴더 안에 있는지
    # 2.3. 비디오 파일이 한개인지
# 3. 메타 데이터에 <root>가 있는지 확인, 없으면 추가 (main.py 에서 가져오기) v
# 4. 영상 인풋이 폴더 주소인지 영상 주소인지 확인 v
    # 4.1 폴더 주소면 영상 주소로 변경 v
    # 4.2 비디오 주소면 패스 v
    # 4.3. 메타 데이터의 시간과 영상 시간이 다르면 경고

import glob
import warnings

#1. 
def metadata_info_checking(input_metadata_info):
    edited_metadata_info = input_metadata_info
    if type(input_metadata_info) == str:
        last_letter = edited_metadata_info[-1]
        if last_letter != "*":
            if last_letter == "/":
                edited_metadata_info += "*.xml"
            else:
                edited_metadata_info += "/*.xml"
        edited_metadata_info = glob.glob(edited_metadata_info)
    if len(edited_metadata_info) == 0:
        warnings.warn("xml files are not exist!", FutureWarning)
        exit()
    else:
        edited_metadata_info = sorted(edited_metadata_info)
        return edited_metadata_info

# 2.
def video_info_checking(input_video_info):
    edited_video_info = input_video_info
    if edited_video_info[-4:] != ".avi" or edited_video_info[-4:] != ".mp4" or edited_video_info[-4:] != ".jpg":
        last_letter = edited_video_info[-1]
        if last_letter != "*":
            if last_letter == "/" :
                edited_video_info += "*"
            else:
                edited_video_info += "/*"
        edited_video_info = glob.glob(edited_video_info)
    if len(edited_video_info) == 0:
        warnings.warn("video file is not exist!", FutureWarning)
        exit()
    elif len(edited_video_info) > 1:
        warnings.warn("Only one vedio file allow as an input", FutureWarning)
        exit()
    else:
        return edited_video_info[0]

# 3.
def metadata_root_existence(file_list):
    for file_path in file_list:
        with open(file_path, "r") as f:
            content = f.read()
            if "<root>" not in content:
                content = "<root>" + content + "</root>"
        with open(file_path, "w") as f:
            f.write(content)


#4. 
def metadata_video_compare(input_metadata_list, video_file_path):
    video_path = video_file_path.split("/")[-1]
    metadata_path = []
    for metadata in input_metadata_list:
        temp = metadata.split("/")
        metadata_path.append(temp[-1])
    video_time = calculate_total_time(metadata_path)
    video_key, video_date, video_hour = split_video_title(video_path)
    video_time_end = str(int(video_hour) + int(video_time))
    for metadata in metadata_path:
        metadata_key, metadata_date, metadata_hour = split_metadata_title(metadata)
        if  video_key != metadata_key:
            warnings.warn("video and meta data has different key title", FutureWarning)
        if video_date != metadata_date:
            warnings.warn("video and meta data has different date", FutureWarning)
        if video_hour > metadata_hour or video_time_end < metadata_hour:
            warnings.warn("meta data time is out of video time", FutureWarning)


def split_video_title(video_title):
    video_title_list = video_title.split("_")
    video_key = video_title_list[0]
    video_dateThour = video_title_list[-1].split(".")[0].split("T")
    video_date = video_dateThour[0]
    video_hour = video_dateThour[1].split("+")[0]
    return video_key, video_date, video_hour

def split_metadata_title(metadata_title):
    metadata_title_list = metadata_title.split("_")
    metadata_key = metadata_title_list[0]
    metadata_dateThour = metadata_title_list[1].split("T")
    metadata_date = metadata_dateThour[0]
    metadata_hour = metadata_dateThour[1] + metadata_title_list[2] + metadata_title_list[3].split("+")[0]
    return metadata_key, metadata_date, metadata_hour

def calculate_total_time(metadata_list):
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
    total_time = ((time_h * 10000) + (time_m * 100) + time_s)

    return str(total_time)

#final
def input_checking_process(metadata_path, video_file_path):
    print("Input data checking")
    metadata_path_list = metadata_info_checking(metadata_path)
    metadata_root_existence(metadata_path_list)
    video_path = video_info_checking(video_file_path)
    metadata_video_compare(metadata_path_list, video_path)
    print("Done")
    return metadata_path_list, video_path