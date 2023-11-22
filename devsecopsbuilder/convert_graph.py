import yaml
import networkx as nx
import matplotlib.pyplot as plt

def create_workflow_graph(steps):
    # Create a directed graph
    G = nx.DiGraph()

    # Organize steps by their step numbers
    steps_by_number = {}
    for step in steps:
        step_number = step['stepno']
        if step_number not in steps_by_number:
            steps_by_number[step_number] = []
        steps_by_number[step_number].append(step['name'])

    # Add the nodes to the graph
    for step_no, names in steps_by_number.items():
        for name in names:
            G.add_node(name, subset=step_no)

    # Sort the step numbers to determine the sequence
    sorted_step_numbers = sorted(steps_by_number.keys())

    # Add edges to represent sequential and parallel steps
    for i, step_no in enumerate(sorted_step_numbers[:-1]):
        next_step_no = sorted_step_numbers[i + 1]
        for name in steps_by_number[step_no]:
            for next_name in steps_by_number[next_step_no]:
                G.add_edge(name, next_name)

    return G

def parse_yaml_and_create_graph(file_path):
    # Load the YAML file
    with open(file_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)

    # Extract the steps
    steps = []
    for step in data_loaded['commands_to_run']['steps']:
        steps.append({'name': step['name'], 'stepno': step['stepno']})

    # Use the previously defined function to create a graph
    return create_workflow_graph(steps)

if __name__ == '__main__':
    # Replace with the actual path to your YAML file
    file_path = 'file.yaml'
    output_img_path = 'command_outputs/graphs/graph.png'
    workflow_graph = parse_yaml_and_create_graph(file_path)

    # Draw the graph
    plt.figure(figsize=(14, 10))
    pos = nx.multipartite_layout(workflow_graph, subset_key="subset")
    nx.draw(workflow_graph, pos, with_labels=True, node_color='lightblue', node_size=2500, edge_color='gray', linewidths=1, font_size=8)
    plt.title("Workflow Graph from YAML File")
    plt.savefig(output_img_path) 
    # if you want to see the graph, uncomment the following line
    #plt.show()
