import datetime
import subprocess
import yaml
import os
from string import Template
import argparse


def load_configuration(filepath):
    with open(filepath, "r") as yaml_file:
        return yaml.safe_load(yaml_file)


def create_output_directory(directory):
    os.makedirs(directory, exist_ok=True)


def install_tools(tools):
    for tool_info in tools:
        tool_name = tool_info.get("name")
        install_command = tool_info.get("install")
        if tool_name and install_command:
            print(
                "Runnning ==> ", install_command
            )  # Replace with subprocess.run(...) to execute
            subprocess.run(install_command, shell=True, check=True)


# def install_tools(tools):
#     for tool_info in tools:
#         tool_name = tool_info.get("name")
#         install_command = tool_info.get("install")
#         help_command = tool_info.get(
#             "help"
#         )  # Command to display help, used to check if installed

#         if tool_name and install_command and help_command:
#             try:
#                 # Check if the tool is already installed by running its help command   # noqa: E501
#                 subprocess.run(
#                     help_command,
#                     shell=True,
#                     check=True,
#                     stdout=subprocess.DEVNULL,
#                     stderr=subprocess.DEVNULL,
#                 )
#                 print(f"{tool_name} is already installed.")
#             except subprocess.CalledProcessError:
#                 # Tool is not installed, proceed with installation
#                 print(f"Installing {tool_name}...")
#                 subprocess.run(install_command, shell=True, check=True)
#         else:
#             print(f"Missing information for {tool_name}")

def update_tools(tools):
    for tool_info in tools:
        tool_name = tool_info.get("name")
        update_command = tool_info.get("update")
        if tool_name and update_command:
            print(
                "Updating with ==>", update_command
            )  # Replace with subprocess.run(...) to execute
            subprocess.run(update_command, shell=True, check=True)


def run_command(step, output_dir, **kwargs):
    step_name = step.get("name", "Unnamed step")
    command_template = Template(step.get("command", ""))
    # Create a combined dictionary of default and override parameters
    command_parameters = {**kwargs, **step.get("parameters", {})}
    templated_command = command_template.safe_substitute(command_parameters)
    output_file = get_output_file_path(output_dir, step_name)
    result = execute_command(templated_command)
    save_command_output(result, output_file, step_name, templated_command)
    # Execute post_command if present
    post_command_result = execute_post_command(step, **command_parameters)
    if post_command_result and post_command_result.returncode != 0:
        print(
            f"Error executing post command for '{step_name}': {post_command_result.stderr}"   # noqa: E501
        )


def execute_post_command(step, **kwargs):
    post_command_template = Template(step.get("post_command", ""))
    # Use combined dictionary of default and override parameters
    command_parameters = {**kwargs, **step.get("post_parameters", {})}
    templated_post_command = post_command_template.safe_substitute(command_parameters)   # noqa: E501
    if templated_post_command:
        print(f"Executing post command for {step.get('name')}...")
        result = execute_command(templated_post_command)
        return result
    return None


def get_output_file_path(output_dir, step_name):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(output_dir, f"output_{step_name}_{current_date}.txt")


def execute_command(command):
    return subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True   # noqa: E501
    )


def save_command_output(result, output_file, step_name, command):
    with open(output_file, "w") as output:
        output.writelines(
            [
                f"Step: {step_name}\n",
                f"Command: {command}\n",
                f"Exit Code: {result.returncode}\n",
                "--- STDOUT ---\n",
                result.stdout,
                "--- STDERR ---\n",
                result.stderr,
            ]
        )
    if result.returncode == 0:
        print(
            f"Step '{step_name}' executed successfully. Output saved to {output_file}"   # noqa: E501
        )
    else:
        print(f"Error executing step '{step_name}': {result.stderr}")


def get_repository_languages(repository_path):
    """
    Retrieves the languages used in a repository.

    Args:
        repository_path (str): The path to the repository.

    Returns:
        list: A list of language names used in the repository.

    Raises:
        subprocess.CalledProcessError: If an error occurs while running github-linguist.   # noqa: E501
    """
    try:
        # Change to the repository directory and run github-linguist
        result = subprocess.run(
            ["github-linguist"],
            cwd=repository_path,
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        )

        # Parse the output
        output = result.stdout.strip().split("\n")
        languages = [
            line.split()[-1] for line in output
        ]  # Extracting the language names
        return languages
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
# repository_path = './WebGoat.NET'  # Replace with the actual repository path
# print(get_repository_languages(repository_path))
# result = ['C#', 'ASP.NET', 'CSS', 'JavaScript']


def main():
    parser = argparse.ArgumentParser(description="Tool Installation and Update Script")   # noqa: E501
    parser.add_argument("--install", action="store_true", help="Install tools")
    parser.add_argument("--update", action="store_true", help="Update tools")
    parser.add_argument("--execute", action="store_true", help="Run playbook.yaml")   # noqa: E501
    args = parser.parse_args()

    # Check if no arguments were provided
    if not (args.install or args.update or args.execute):
        parser.print_help()
        return
    # Load tool configuration from the YAML file
    tools_config = load_configuration("./tools/tools.yaml")
    all_tools = tools_config["tools_to_install"]["tools"]
    default_tools = [tool for tool in all_tools if tool.get("default", False)]

    if args.install:
        print("----------------------")
        print("Running pipeline executer: Installing tools...")
        print("----------------------")
        # print(default_tools)
        install_tools(default_tools)
        print("----------------------")
        print("Tools installed")

    if args.update:
        print("----------------------")
        print("Running pipeline executer: Updating tools...")
        print("----------------------")
        update_tools(default_tools)
        print("----------------------")
        print("Tools updated")
    if args.execute:
        print("----------------------")
        print("Running pipeline executer: Executing playbook.yaml...")
        print("----------------------")
        config = load_configuration("./playbooks/playbook.yaml")
        output_dir = "command_outputs/outputs"
        create_output_directory(output_dir)

        # Define default paths and other variables as a dictionary
        default_variables = {
            # Default variable values go here
        }

        # Run configured commands
        commands_to_run = config.get("commands_to_run", {}).get("steps", [])
        for step in commands_to_run:
            if isinstance(step, dict):
                # Update default variables with step-specific ones if they exist  # noqa: E501
                step_variables = {**default_variables, **step.get("parameters", {})}  # noqa: E501
                run_command(step, output_dir, **step_variables)
            else:
                print(f"Invalid step format: {step}")
        print("----------------------")
        print("pipeline executer: playbook.yaml executed")


if __name__ == "__main__":
    main()
# Main execution
# python devsecopsbuilder/pipeline_executer.py
# if __name__ == "__main__":
# Test for main function default playbook runner
# config = load_configuration('./playbooks/playbook.yaml')
# output_dir = 'command_outputs/outputs'
# create_output_directory(output_dir)
#
# Define default paths and other variables as a dictionary
# default_variables = {
#    # Default variable values go here
# }
#
# Run configured commands
# commands_to_run = config.get('commands_to_run', {}).get('steps', [])
# for step in commands_to_run:
#    if isinstance(step, dict):
#        # Update default variables with step-specific ones if they exist
#        step_variables = {**default_variables, **step.get('parameters', {})}
#        run_command(step, output_dir, **step_variables)
#    else:
#        print(f"Invalid step format: {step}")
