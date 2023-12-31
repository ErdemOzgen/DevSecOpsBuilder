import yaml
from collections import defaultdict


def generate_jenkinsfile(yaml_path, jenkinsfile_path):
    with open(yaml_path, "r") as file:
        config = yaml.safe_load(file)

    # Group steps by 'stepno'
    steps_by_stepno = defaultdict(list)
    for step in config["commands_to_run"]["steps"]:
        steps_by_stepno[step["stepno"]].append(step)

    with open(jenkinsfile_path, "w") as jfile:
        # Write the pipeline header to the Jenkinsfile
        jfile.write("pipeline {\n")
        jfile.write("    agent any\n\n")
        jfile.write("    stages {\n")

        # Write stages that run in sequence or parallel
        for stepno, steps in sorted(steps_by_stepno.items()):
            if len(steps) > 1:
                # Multiple steps for the same stepno, run in parallel
                jfile.write(f"        stage('Step_{stepno}') {{\n")
                jfile.write("            parallel {\n")
                for step in steps:
                    write_step(jfile, step)
                jfile.write("            }\n")
                jfile.write("        }\n")
            else:
                # Single step, run sequentially
                for step in steps:
                    write_step(jfile, step)

        # Write the pipeline footer to the Jenkinsfile
        jfile.write("    }\n")
        jfile.write("    post {\n")
        jfile.write("        success {\n")
        jfile.write("            echo 'Success!'\n")
        jfile.write("        }\n")
        jfile.write("        failure {\n")
        jfile.write("            echo 'Failure!'\n")
        jfile.write("        }\n")
        jfile.write("    }\n")
        jfile.write("}\n")


def write_step(jfile, step):
    stage_name = step["name"].replace(" ", "_")
    jfile.write(f"            stage('{stage_name}') {{\n")
    jfile.write("                steps {\n")

    # Check for parameters and substitute them in the command
    command = step["command"]
    if "parameters" in step:
        for param_key, param_value in step["parameters"].items():
            command = command.replace("${" + param_key + "}", param_value)

    jfile.write(f"                    sh '{command}'\n")

    # Check for post_command and add it
    if "post_command" in step:
        post_command = step["post_command"]
        if "parameters" in step:
            for param_key, param_value in step["parameters"].items():
                post_command = post_command.replace("${" + param_key + "}", param_value)  # noqa: E501

        jfile.write(f"                    sh '{post_command}'\n")

    jfile.write("                }\n")
    jfile.write("            }\n")


if __name__ == "__main__":
    generate_jenkinsfile(
        "./playbooks/playbook.yaml", "./command_outputs/jenkinsFiles/Jenkinsfile"  # noqa: E501
    )
