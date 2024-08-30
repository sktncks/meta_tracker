import subprocess
import os

def run_commands():
    requirements_install = "pip install -r packages/requirements.txt"

    # Create a shell script to activate the virtual environment and install the requirements
    script_content = f"""
    {requirements_install}
    """
    
    script_path = "install_requirements.sh"
    print_help = "python3 ./src/run.py --help"
    
    with open(script_path, "w") as script_file:
        script_file.write(script_content)
    
    # Make the script executable
    os.chmod(script_path, 0o775)
    
    # Run the script
    subprocess.run(f"./{script_path}", shell=True, check=True)

    # Clean up the script
    os.remove(script_path)
    
    subprocess.run(print_help, shell=True, check=True)
    
if __name__ == "__main__":
    run_commands()


    