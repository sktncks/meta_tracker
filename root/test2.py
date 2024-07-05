import subprocess
import os

def run_commands():
    # 1. Create virtual environment directory
    env_dir_gen = "virtualenv env"
    subprocess.run(env_dir_gen, shell=True, check=True)

    # 2. Activate virtual environment
    activate_env = "source env/bin/activate"
    # Note: `source` is a shell built-in command, it won't work directly with subprocess in non-interactive shell
    # We will execute subsequent commands in the activated environment using a shell script
    # 3. Install libraries in requirements.txt
    requirements_install = "pip install -r root/requirements.txt"

    # Create a shell script to activate the virtual environment and install the requirements
    script_content = f"""
    {activate_env}
    {requirements_install}
    """
    
    script_path = "install_requirements.sh"
    with open(script_path, "w") as script_file:
        script_file.write(script_content)
    
    # Make the script executable
    os.chmod(script_path, 0o775)
    
    # Run the script
    subprocess.run(f"./{script_path}", shell=True, check=True)

    # Clean up the script
    os.remove(script_path)
    
if __name__ == "__main__":
    run_commands()


    