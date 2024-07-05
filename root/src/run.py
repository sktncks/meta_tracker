import typer
from main_video import video_editing
from main_img import imgtovideo
from input_check import input_checking_process

def main(metadata_path: str, video_path: str, start_time: str, end_time: str, set_output_path: str,
         output_name: str = "output", output_extension: str = ".avi",
         box_boundary_thickness: int = 2,
         tail_size: int = 25, tail_thickness: int = 2,
         text_scale: float = 0.5, text_thickness: int = 1,
         visualization_on: bool = False, visualization_speed: int = 50):
    box_color = (0, 255, 255)
    tail_color = (0, 255, 255)
    text_color = (0, 255, 255)
    metadata_file, background = input_checking_process(metadata_path, video_path)
    if background[-4:] == ".mp4" or background[-4:] == ".avi":
          video_editing(metadata_file, background,
                set_output_path, output_name, output_extension,
                start_time, end_time,
                box_color, box_boundary_thickness,
                tail_color, tail_size, tail_thickness,
                text_color, text_scale, text_thickness,
                visualization_on, visualization_speed)
    elif background[-4:] == ".jpg":
          imgtovideo(metadata_file, background,
                set_output_path, output_name, output_extension,
                start_time, end_time,
                box_color, box_boundary_thickness,
                tail_color, tail_size, tail_thickness,
                text_color, text_scale, text_thickness,
                visualization_on, visualization_speed)

typer.run(main)


# /home/user1/Documents/meta.tracker/meta_data
# /home/user1/Documents/meta.tracker/video_data box_color = (0, 255, 255), tail_color = (0, 255, 255), text_color = (0, 255, 255), 