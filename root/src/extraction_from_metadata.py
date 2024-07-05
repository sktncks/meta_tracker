import xml.etree.ElementTree as ET

def detection_point_check(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    detection_point = root.find("vca/vca_cfg/detection_point").text
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

def box_point_gen(pt_lu, pt_ld, pt_ru, pt_rd, w, h):
    w_r = w / 5
    h_r = h / 5

    return (
        (int(pt_lu[0] + w_r), pt_lu[1]),  # pt_lu_r
        (pt_lu[0], int(pt_lu[1] + h_r)),  # pt_lu_d
        (int(pt_ld[0] + w_r), pt_ld[1]),  # pt_ld_r
        (pt_ld[0], int(pt_ld[1] - h_r)),  # pt_ld_u
        (int(pt_ru[0] - w_r), pt_ru[1]),  # pt_ru_l
        (pt_ru[0], int(pt_ru[1] + h_r)),  # pt_ru_d
        (int(pt_rd[0] - w_r), pt_rd[1]),  # pt_rd_l
        (pt_rd[0], int(pt_rd[1] - h_r)),  # pt_rd_u
    )

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