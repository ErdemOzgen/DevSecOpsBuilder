import json
import os
import glob
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    KeepTogether,
    PageBreak,
)  # noqa: E501

styles = getSampleStyleSheet()


def get_file_path(base_dir, scan_type, file_name):
    """
    Constructs a file path for a given scan type and file name.

    Args:
        base_dir (str): The base directory where the scan results are stored.
        scan_type (str): The type of scan (e.g., 'python-scan').
        file_name (str): The name of the file (e.g., 'bandit_result.json').

    Returns:
        str: The full file path.
    """
    return os.path.join(base_dir, scan_type, file_name)


def process_json_data(file_path, heading_title, item_processor, data_tag, addHeader=True, giveInfo=True):  # noqa: E501
    story = []
    if addHeader:
        heading = Paragraph(f"<b>{heading_title}</b>", styles["Heading1"])
        story.append(heading)
    if file_path is None:
        if giveInfo:
            no_result = Paragraph("There is no result under this scan.", styles["Normal"])  # noqa: E501
            story.append(no_result)
            story.append(PageBreak())
        return story
    
    with open(file_path, "r") as file:
        data = json.load(file)

    if heading_title == "Detect Secrets Scan Results":
        story += item_processor(data)
        return story
    
    if heading_title == "Safety Extra Info":
        story.append(item_processor(data))
        return story
        
    results = data.get(data_tag, [])

    if isinstance(results, list):
        # If results is a list, process each item
        for item in results:
            paragraph = item_processor(item)
            story.append(KeepTogether([Paragraph(paragraph, styles["Normal"])]))  # noqa: E501
    elif isinstance(results, dict):
        # If results is a dictionary, process its values
        for item in results.values():
            paragraph = item_processor(item)
            story.append(KeepTogether([Paragraph(paragraph, styles["Normal"])]))  # noqa: E501

    return story


def bandit_item_processor(item):
    code_snippet = item["code"].replace("\n", "<br/>")
    return (
        f"<b>File:</b> {item['filename']}, <b>Line:</b> {item['line_number']}<br/>"  # noqa: E501
        f"<b>Severity:</b> {item['issue_severity']}<br/>"
        f"<b>Issue:</b> {item['issue_text']}<br/>"
        f"<b>Code Snippet:</b> <code>{code_snippet}</code><br/><br/>"
    )


def grype_item_processor(item):
    vulnerability = item["vulnerability"]
    fix_versions = vulnerability["fix"]["versions"]
    related_vulns = item["relatedVulnerabilities"]
    related_vulns_id = [vuln["id"] for vuln in related_vulns] if related_vulns else ["No related vulnerabilities found."]   # noqa: E501
    related_vulns_id_str = ", ".join(related_vulns_id)

    return (
        f"<b>Vulnerability ID:</b> {vulnerability['id']}<br/>"
        f"<b>Severity:</b> {vulnerability['severity']}<br/>"
        f"<b>Description:</b> {vulnerability['description']}<br/>"
        f"<b>Fix Versions:</b> {', '.join(fix_versions)}<br/>"
        f"<b>URLs:</b> {', '.join(vulnerability['urls'])}<br/>"
        f"<b>Related Vulnerability ID:</b> {related_vulns_id_str}<br/><br/>"
    )


def safety_item_processor(item):
    paragraph = (
        f"<b>Package Name:</b> {item.get('package_name')}<br/>"
        f"<b>Vulnerability ID:</b> {item.get('vulnerability_id')}<br/>"
        f"<b>CVE:</b> <code>{item.get('CVE')}</code><br/>"
        f"<b>Analyzed Version:</b> {item.get('analyzed_version')}<br/>"
        f"<b>Advisory:</b> <code>{item.get('advisory')}</code><br/>"
        f"<b>More info:</b> <code>{item.get('more_info_url')}</code><br/><br/>"
    )
    return paragraph


def secret_item_processor(result):
    return (
        f"<b>Secret Type:</b> {result.get('type')}<br/>"
        f"<b>File Path:</b> {result.get('filename')}<br/>"
        f"<b>Line:</b> {result.get('line_number')}<br/>"
        f"<b>Hashed Secret:</b> {result.get('hashed_secret')}<br/><br/>"
    )


def sbom_item_processor(component):
    return (
        f"<b>Type:</b> {component['type']}<br/>"
        f"<b>Name:</b> {component['name']}<br/>"
        f"<b>Version:</b> <code>{component['version']}</code><br/>"
        f"<b>CPE:</b> {component.get('cpe', 'N/A')}<br/><br/>"
    )


def bandit_results(bandit_file_path):
    return process_json_data(bandit_file_path, "Bandit Scan Results", bandit_item_processor, "results")  # noqa: E501


def grype_results(grype_file_path):
    return process_json_data(grype_file_path, "Grype Scan Results", grype_item_processor, "matches")  # noqa: E501


def safety_info(safety_file_path):
    def safety_scanned_packages(item):
        pkgs = []

        for package_name, package_info in item.get("scanned_packages", {}).items():  # noqa: E501
            pkgs.append(f"{package_name} {package_info.get('version')}")

        pkgs_str = ", ".join(pkgs)
        pkgs_paragraph = Paragraph(f"<b>Scanned Packages: </b>{pkgs_str}<br/><br/>", styles["Normal"])  # noqa: E501
        return pkgs_paragraph
    
    return process_json_data(safety_file_path, "Safety Extra Info", safety_scanned_packages, "vulnerabilities", False, False)  # noqa: E501


def safety_results(safety_file_path):
    return process_json_data(safety_file_path, "Safety Dependency Scan Results", safety_item_processor, "vulnerabilities")   # noqa: E501


def secret_results(secret_file_path):
    def process_secrets(item):
        story = []
        for _, results_list in item["results"].items():
            for result in results_list:
                paragraph = secret_item_processor(result)
                story.append(KeepTogether([Paragraph(paragraph, styles["Normal"])]))  # noqa: E501
        story.append(PageBreak())

        return story

    return process_json_data(secret_file_path, "Detect Secrets Scan Results", process_secrets, "results")  # noqa: E501


def sbom_results(sbom_file_path):
    return process_json_data(sbom_file_path, "SBOM with Syft", sbom_item_processor, "components")  # noqa: E501


def generate_pdf(output_filename, **scan_files):  # noqa: E501
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    story = []

    story += bandit_results(scan_files["bandit_file_path"])
    story += grype_results(scan_files["grype_file_path"])
    story += safety_results(scan_files["safety_file_path"])
    story += safety_info(scan_files["safety_file_path"])
    story += secret_results(scan_files["secret_file_path"])
    
    # SBOM results can be enormous. Therefore, this segment is optional.
    if "sbom_file_path" in scan_files:
        story += sbom_results(scan_files["sbom_file_path"])

    doc.build(story)


def find_file_by_keyword(base_dir, scan_type, keyword):
    """
    Searches for the most recently modified file in the specified directory 
    that contains the given keyword. Excludes specific keywords from the search.  # noqa: E501
    Returns the path of that file.
    """
    excluded_keywords = ['armor', 'obf', 'obfuscated', 'pyarmor', 'hidden']
    
    # If the keyword is in the list of excluded keywords, return None
    if any(excluded_keyword in keyword.lower() for excluded_keyword in excluded_keywords):  # noqa: E501
        return None
    
    pattern = os.path.join(base_dir, scan_type, f"*{keyword}*")
    files = glob.glob(pattern)
    
    # Exclude files with specific keywords
    files = [file for file in files if not any(excluded_keyword in file.lower() for excluded_keyword in excluded_keywords)]   # noqa: E501
    
    if not files:
        return None
    
    # Sort files by modification time and return the most recent
    return max(files, key=os.path.getmtime)


def find_and_generate_report(base_dir, scan_type, output_filename):
    scan_files = {}

    scan_files["bandit_file_path"] = find_file_by_keyword(base_dir, scan_type, "bandit")  # noqa: E501
    scan_files["grype_file_path"] = find_file_by_keyword(base_dir, scan_type, "grype")  # noqa: E501
    scan_files["safety_file_path"] = find_file_by_keyword(base_dir, scan_type, "dependency_scan")  # noqa: E501
    scan_files["secret_file_path"] = find_file_by_keyword(base_dir, scan_type, "secrets")   # noqa: E501

    generate_pdf(output_filename, **scan_files)  # noqa: E501
    print("Report generated.")


if __name__ == "__main__":
    # Define the base directory
    base_dir = "command_outputs"

    # Define the scan type (can be changed for different projects)
    scan_type = "python-scan"

    # Output filename
    output_filename = "output.pdf"

    # Call the function to find files and generate the report
    find_and_generate_report(base_dir, scan_type, output_filename)

# if __name__ == "__main__":
#     # Define the base directory and scan type
#     base_dir = "command_outputs"
#     scan_type = "python-scan"

#     # File names
#     bandit_file = "bandit_result.json"
#     grype_file = "grype.json"
#     safety_file = "dependency_scan.json"
#     secret_file = "secrets.json"
#     sbom_file = "sbom.json"

#     # Output filename
#     output_filename = "output.pdf"

#     # Construct file paths using base directory, scan type, and file names
#     bandit_file_path = os.path.join(base_dir, scan_type, bandit_file)
#     grype_file_path = os.path.join(base_dir, scan_type, grype_file)
#     safety_file_path = os.path.join(base_dir, scan_type, safety_file)
#     secret_file_path = os.path.join(base_dir, scan_type, secret_file)
#     sbom_file_path = os.path.join(base_dir, scan_type, sbom_file)  # Optional

#     generate_pdf(output_filename, bandit_file_path, grype_file_path, safety_file_path, secret_file_path)  # noqa: E501

#     print("Report generated.")
