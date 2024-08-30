import typer
from main_video import video_editing
from main_img import imgtovideo
from input_check import input_checking_process, print_total_time

def main(metadata_path: str, background_path: str, start_time: str = "000000", end_time: str = "000000", output_path: str = "./",
         output_size_rate: float = 1, output_name: str = "output", output_extension: str = ".avi",
         box_boundary_thickness: int = 2,
         tail_size: int = 25, tail_thickness: int = 2,
         text_scale: float = 0.5, text_thickness: int = 1,
         visualization_on: bool = False, visualization_speed: int = 50):
      
    box_color, tail_color, text_color = (0, 255, 255), (0, 255, 255), (0, 255, 255) #temp
    
    metadata_file, background = input_checking_process(metadata_path, background_path)
    
    if end_time == "000000":
          end_time = print_total_time(metadata_file)
                 
    if background[-4:] == ".mp4" or background[-4:] == ".avi":
          video_editing(metadata_file, background,
                output_path, output_name, output_extension, output_size_rate,
                start_time, end_time,
                box_color, box_boundary_thickness,
                tail_color, tail_size, tail_thickness,
                text_color, text_scale, text_thickness,
                visualization_on, visualization_speed)
    elif background[-4:] == ".jpg":
          imgtovideo(metadata_file, background,
                output_path, output_name, output_extension, output_size_rate,
                start_time, end_time,
                box_color, box_boundary_thickness,
                tail_color, tail_size, tail_thickness,
                text_color, text_scale, text_thickness,
                visualization_on, visualization_speed)

typer.run(main)