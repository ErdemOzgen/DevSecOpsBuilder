from devsecopsbuilder import pipeline_executer

# Main code execution
if __name__ == "__main__":
    config = pipeline_executer.load_configuration('./playbooks/playbook.yaml')
    output_dir = 'command_outputs/outputs'
    pipeline_executer.create_output_directory(output_dir)

    # Define default paths and other variables as a dictionary
    default_variables = {
        # Default variable values go here
    }

    # Run configured commands
    commands_to_run = config.get('commands_to_run', {}).get('steps', [])
    for step in commands_to_run:
        if isinstance(step, dict):
            # Update default variables with step-specific ones if they exist
            step_variables = {**default_variables, **step.get('parameters', {})}
            pipeline_executer.run_command(step, output_dir, **step_variables)
        else:
            print(f"Invalid step format: {step}")
