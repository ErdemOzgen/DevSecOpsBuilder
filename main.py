import argparse
from devsecopsbuilder import pipeline_executer

def main():
    parser = argparse.ArgumentParser(description="Pipeline Execution Script")
    parser.add_argument('--install', action='store_true', help='Install tools')
    parser.add_argument('--update', action='store_true', help='Update tools')
    parser.add_argument('--execute', action='store_true', help='Execute commands from playbook')
    parser.add_argument('--config', default='./playbooks/playbook.yaml', help='Path to configuration file')
    parser.add_argument('--output_dir', default='command_outputs/outputs', help='Path to output directory')

    args = parser.parse_args()

    # Check if no arguments were provided
    if not (args.install or args.update or args.execute):
        parser.print_help()
        return

    # Load configuration from specified or default path
    config = pipeline_executer.load_configuration(args.config)

    # Create specified or default output directory
    pipeline_executer.create_output_directory(args.output_dir)

    # Load tool configuration from the YAML file
    tools_config = pipeline_executer.load_configuration("./tools/tools.yaml")
    all_tools = tools_config["tools_to_install"]["tools"]
    default_tools = [tool for tool in all_tools if tool.get('default', False)]

    # Define default paths and other variables as a dictionary
    default_variables = {
        # Default variable values go here
    }

    if args.install or args.update:
        # Assuming 'tools' is the relevant section in the configuration for install/update
        tools = config.get('tools', [])
        if args.install:
            # Install tools
            pipeline_executer.install_tools(default_tools)
        elif args.update:
            # Update tools
            pipeline_executer.update_tools(default_tools)

    if args.execute:
        # Execute configured commands
        commands_to_run = config.get('commands_to_run', {}).get('steps', [])
        for step in commands_to_run:
            if isinstance(step, dict):
                # Update default variables with step-specific ones if they exist
                step_variables = {**default_variables, **step.get('parameters', {})}
                pipeline_executer.run_command(step, args.output_dir, **step_variables)
            else:
                print(f"Invalid step format: {step}")

if __name__ == "__main__":
    main()
