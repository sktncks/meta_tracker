import sys

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
    
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 50):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()
    
def print_input_info(metadata_list, background_file, background_type):
    print('\033[34m' + '<Input Files>' + '\033[0m')
    print('\033[34m' + 'Metadata' + '\033[0m')
    for i, metadata_file in enumerate(metadata_list):
        print(f"({i}/{len(metadata_list)}) -> {metadata_file}")
    print('\033[34m' + background_type + '\033[0m')
    print(background_file)
    print("--------------------------------------------------------------------------------------------")
    
def print_output_info(output_save_path, output_file_name):
    print('\033[34m' + '<Output Video>' + '\033[0m')
    print(output_save_path + output_file_name)