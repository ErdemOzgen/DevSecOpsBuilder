# DevSecOpsBuilder

## Overview

DevSecOpsBuilder is a comprehensive tool designed to facilitate the setup and testing of DevSecOps environments. It is equipped with Makefile, Dockerfile, and Python scripts to automatically install necessary software and libraries, creating an effective testbed for DevSecOps practices. This solution streamlines the process of setting up a DevSecOps pipeline, making it easier for users to implement and test various security practices in their development workflows.

**Note**: DevSecOpsBuilder is intended for testing and development purposes and is not production-ready.

## Features

1. **YAML-Based Pipeline Creation**: Users can utilize YAML files to construct their DevSecOps pipeline, tailoring it to their specific needs.

2. **Predefined YAML Templates**: The repository includes a range of predefined YAML templates for specific tasks such as SAST, DAST, SCA, and secret scanning, allowing for quick setup and deployment.

3. **Execution and Logging**: By running `python main.py`, users can execute their chosen or custom playbook.yaml and view the outputs and logs generated during the process.

4. **Jenkinsfile Generation**: DevSecOpsBuilder can automatically generate Jenkinsfiles from the provided YAML configurations, integrating seamlessly with Jenkins CI/CD pipelines.

5. **Visualization Tools**: The tool generates graphical representations of the YAML and Jenkinsfile, providing a visual overview of the pipeline's structure and flow.

6. **Docker Container Deployment**: It supports the deployment of Docker containers for key DevSecOps tools like SonarQube, Dependency Track, NodeJsScan, enhancing the security testing capabilities.

7. **GitHub Integration**: DevSecOpsBuilder can clone test repositories from GitHub, making it a versatile tool for testing existing tools and pipelines in a controlled environment.

## Getting Started

### Prerequisites

- Docker
- Python 3.x
- Access to a GitHub account (for cloning repositories)

### Installation

1. Clone the DevSecOpsBuilder repository:
   ```bash
   git clone [repository URL]
   ```

2. Navigate to the repository directory:
   ```bash
   cd DevSecOpsBuilder
   ```

3. Run the setup script:
   ```bash
   make setup
   ```

### Usage

1. Choose or create a playbook YAML file based on your testing requirements.

2. Run the main script to start the pipeline:
   ```bash
   python main.py
   ```

3. Follow the on-screen instructions to view outputs and logs.

To include a guide on how to use the `playbook.yaml` file in your README.md, you can incorporate the following explanation. This guide will help users understand the structure and functionality of the playbook and how to customize it for their needs.

```markdown
## Using the playbook.yaml

The `playbook.yaml` file is a crucial part of the DevSecOpsBuilder, defining the sequence of commands and actions to be executed in your DevSecOps pipeline. Here's how you can use and understand it:

### Structure of playbook.yaml

The playbook is composed of a series of steps, each representing a command to be executed. Here's an example of what a typical step looks like:

```yaml
- name: "Name of the Step"
  command: "command to execute"
  parameters:
    param1: "value1"
    param2: "value2"
  post_command: "command to execute after the main command"
  stepno: Step Number
```

- `name`: A descriptive name for the step.
- `command`: The main command to be executed.
- `parameters`: Key-value pairs that provide additional parameters to the command.
- `post_command`: An optional command to be executed after the main command.
- `stepno`: The step number, for ordering and reference.

### Customizing playbook.yaml

You can customize the playbook according to your project needs. For instance:

1. **Change Commands**: Replace the command in each step with the one you need to execute. For example, change `pwd` to any other command like `ls`.

2. **Modify Parameters**: Adjust the `parameters` for each command to suit your environment or requirements. For example, change `scan_directory` to the directory you want to scan.

3. **Add or Remove Steps**: You can add new steps or remove existing ones. To add a new step, copy the format of an existing step and modify it accordingly.

4. **Reorder Steps**: Change the `stepno` values to reorder the steps. Ensure that the steps are in the sequence you want them to be executed.

### Example Usage

Let's break down the example given in the playbook:

- **Step 1 - PWD**: This step executes the `pwd` command, showing the current working directory.

- **Step 2 - SYFT-SCAN**: Performs a Syft scan on the specified directory and saves the results in JSON format.

- **Step 3 - Grype Scanner Git Repo**: Runs Grype scan on a specified git repository and outputs the results in JSON format.

- **Step 4 - Grype Scanner Docker Container**: Executes Grype scan on a Docker container.

- **Step 5 - Grype Scanner SBOM Scan**: First generates a Software Bill of Materials (SBOM) with Syft, then runs a Grype scan on it.

- **Step 6 - Finished**: Echoes a custom message indicating the completion of the DevSecOps Builder process.

```yaml
commands_to_run:
  steps:
    - name: "PWD"
      command: pwd
      stepno: 1

    - name: "SYFT-SCAN"
      command: syft ${scan_directory} --output cyclonedx-json >> ${output_path}/syft-results.json
      parameters:
        scan_directory: "./lab/WebGoat/"
        output_path: "./command_outputs/SBOM/"
      post_command: "echo Syft Scan Complete. Results stored in ${output_path}"
      stepno: 2
    - name: "Grype Scanner Git Repo"
      command: "grype ${lab_path} -o ${output_type} >> ${output_path}"
      parameters:
        lab_path: "./lab/NodeGoat/"
        output_type: "json"
        output_path: "command_outputs/scanner/grype-repo-scan.json"
      stepno: 3
          

    - name: "Grype Scanner Docker Container"
      command: "grype ${docker_path} -o ${output_type} >> ${output_path}"
      parameters:
        docker_path: "zricethezav/gitleaks:latest"
        output_type: "json"
        output_path: "command_outputs/scanner/grype-gitleaks-docker-scan.json"
      stepno: 4
      

    - name: "Grype Scanner SBOM Scan"
      command: "syft ${repo_path} -o ${output_type} > vulnado-sbom.json >> ${sbom_path}"
      parameters:
        repo_path: "./lab/NodeGoat/"
        output_type: "syft-json"
        sbom_path: "command_outputs/scanner/syft-sbom.json"
      stepno: 5
      post_command: "grype ${sbom_path} -o ${output_type} >> ${output_path}"
      post_parameters:
        sbom_path: "command_outputs/scanner/syft-sbom.json"
        output_type: "json"
        output_path: "command_outputs/scanner/grype-sbom-scan.json"
    - name: "Finished"
      command: "echo DevSecOps Builder has been finished ${echo_text}"
      parameters:
        echo_text: "This is a test echo."
      stepno: 6

```


### Running the Playbook

To run the playbook, execute the `main.py` script in your DevSecOpsBuilder setup:

```bash
python main.py
```

This will sequentially execute the steps defined in your `playbook.yaml`, automating your DevSecOps pipeline process.

Remember, you can always tailor the playbook to better fit your project's requirements. Experiment with different commands and configurations to optimize your DevSecOps workflow.


![pipeline](./imgs/pipeline1.png)



```bash
python devsecopsbuilder/convert_pipeline.py
```

This will convert existing yaml file to Jenkinsfile. 

![jenkins](./imgs/pipeline2.png)

```bash
python devsecopsbuilder/convert_graph.py 
```

This will create graph representation of your pipeline.

![graph](./imgs/pipeline3.png)



## Contributing

Contributions to DevSecOpsBuilder are welcome! Please read our [contributing guidelines](./CONTRIBUTING) for more information on how to get involved.

## License

This project is licensed under [GNU GENERAL PUBLIC LICENSE]. See the [LICENSE](./LICENSE) file for more details.
