# import subprocess

# def create_and_activate_environment(environment_file):
#     # Create Conda environment from the environment file
#     subprocess.run(["conda", "env", "create", "-f", environment_file], check=True)

#     # Activate the Conda environment and run a command
#     subprocess.run(["conda", "activate", "myenv"], check=True)
#     subprocess.run(["python", "main.py"], check=True)

#     # Deactivate the Conda environment (optional, depending on your requirements)
#     subprocess.run(["conda", "deactivate"], check=True)

# # Example usage
# create_and_activate_environment("environment.yml")