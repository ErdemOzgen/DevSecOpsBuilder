import argparse
from devsecopsbuilder import pipeline_executer

def main():
    parser = argparse.ArgumentParser(description="Pipeline Execution Script")
    parser.add_argument('--install', action='store_true', help='Install tools')
    parser.add_argument('--update', action='store_true', help='Update tools')
    parser.add_argument('--execute', action='store_true', help='Execute commands from playbook')

    args = parser.parse_args()

    # Check if no arguments were provided
    if not (args.install or args.update or args.execute):
        parser.print_help()
        return

    # Common operations
    config = pipeline_executer.load_configuration('./playbooks/playbook.yaml')
    output_dir = 'command_outputs/outputs'
    pipeline_executer.create_output_directory(output_dir)

    # Define default paths and other variables as a dictionary
    default_variables = {
        # Default variable values go here
    }

    if args.install or args.update:
        # Assuming 'tools' is the relevant section in the configuration for install/update
        tools = config.get('tools', [])
        if args.install:
            # Install tools
            pipeline_executer.install_tools(tools)
        elif args.update:
            # Update tools
            pipeline_executer.update_tools(tools)

    if args.execute:
        # Execute configured commands
        commands_to_run = config.get('commands_to_run', {}).get('steps', [])
        for step in commands_to_run:
            if isinstance(step, dict):
                # Update default variables with step-specific ones if they exist
                step_variables = {**default_variables, **step.get('parameters', {})}
                pipeline_executer.run_command(step, output_dir, **step_variables)
            else:
                print(f"Invalid step format: {step}")

if __name__ == "__main__":
    main()
