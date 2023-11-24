import argparse
from devsecopsbuilder import pipeline_executer
from devsecopsbuilder import convert_graph
from devsecopsbuilder import convert_pipeline
import networkx as nx
import matplotlib.pyplot as plt
def main():
    parser = argparse.ArgumentParser(description="Pipeline Execution Script")
    parser.add_argument('--install', action='store_true', help='Install tools')
    parser.add_argument('--update', action='store_true', help='Update tools')
    parser.add_argument('--execute', action='store_true', help='Execute commands from playbook')
    parser.add_argument('--config', default='./playbooks/playbook.yaml', help='Path to configuration file')
    parser.add_argument('--output_dir', default='command_outputs/outputs', help='Path to output directory')
    parser.add_argument('--tools_config', default='./tools/tools.yaml', help='Path to tools configuration file')
    parser.add_argument('--generate_graph', action='store_true', help='Generate graph of defined yaml workflow')
    parser.add_argument('--graph_yaml', default='./playbooks/playbook.yaml', help='Path to yaml file for generating graph')
    parser.add_argument('--graph_output_dir', default='command_outputs/graphs/graph.png', help='Path to graph output directory')
    parser.add_argument('--convert_pipeline', action='store_true', help='Convert yaml to pipeline')
    parser.add_argument('--pipeline_yaml', default='./playbooks/playbook.yaml', help='Path to workflow yaml file to pipeline')
    parser.add_argument('--pipeline_output_dir', default='command_outputs/jenkinsFiles/Jenkinsfile', help='Path to pipeline output directory')
    args = parser.parse_args()

    # Check if no arguments were provided
    if not any(vars(args).values()):
        parser.print_help()
        return

    # Load configuration from specified or default path
    config = pipeline_executer.load_configuration(args.config)

    # Create specified or default output directory
    pipeline_executer.create_output_directory(args.output_dir)


    # Define default paths and other variables as a dictionary
    default_variables = {
        # Default variable values go here
    }

    if args.install or args.update:
        # Load tool configuration from the YAML file
        tools_config = pipeline_executer.load_configuration(args.tools_config)
        all_tools = tools_config["tools_to_install"]["tools"]
        default_tools = [tool for tool in all_tools if tool.get('default', False)]
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
    
    if args.generate_graph:
        try:
            workflow_graph = convert_graph.parse_yaml_and_create_graph(args.graph_yaml)
            plt.figure(figsize=(14, 10))
            pos = nx.multipartite_layout(workflow_graph, subset_key="subset")
            nx.draw(workflow_graph, pos, with_labels=True, node_color='lightblue', node_size=2500, edge_color='gray', linewidths=1, font_size=8)
            plt.title("Workflow Graph from YAML File")
            plt.savefig(args.graph_output_dir)
            print("Graph generated successfully.")
        except Exception as e:
            print(f"Error generating graph: {e}")

    if args.convert_pipeline:
        try:
            convert_pipeline.generate_jenkinsfile(args.pipeline_yaml, args.pipeline_output_dir)
            print("Pipeline converted successfully.")
        except Exception as e:
            print(f"Error converting pipeline: {e}")
if __name__ == "__main__":
    main()
