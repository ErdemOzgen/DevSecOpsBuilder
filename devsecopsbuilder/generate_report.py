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


def bandit_results(bandit_file_path):
    story = []
    bandit_heading = Paragraph("<b>Bandit Scan Results</b>", styles["Heading1"])  # noqa: E501
    story.append(bandit_heading)
    if bandit_file_path is None:
        no_result = Paragraph("There is no result under this scan.", styles["Normal"])  # noqa: E501
        story.append(no_result)
        story.append(PageBreak())
        return story
    with open(bandit_file_path, "r") as file:
        bandit_data = json.load(file)

    for result in bandit_data["results"]:
        code_snippet = result["code"]
        filename = result["filename"]
        line_number = result["line_number"]
        issue_severity = result["issue_severity"]
        issue_text = result["issue_text"]
        code_snippet = code_snippet.replace("\n", "<br/>")
        # Create a paragraph
        paragraph = (
            f"<b>File:</b> {filename}, <b>Line:</b> {line_number}<br/>"
            f"<b>Severity:</b> {issue_severity}<br/>"
            f"<b>Issue:</b> {issue_text}<br/>"
            f"<b>Code Snippet:</b> <code>{code_snippet}</code><br/><br/>"
        )

        # Add the paragraph to the story
        story.append(KeepTogether([Paragraph(paragraph, styles["Normal"])]))
    story.append(PageBreak())

    return story


def grype_results(grype_file_path):
    story = []
    grype_heading = Paragraph("<b>Grype Scan Results</b>", styles["Heading1"])
    story.append(grype_heading)

    if grype_file_path is None:
        no_result = Paragraph("There is no result under this scan.", styles["Normal"])  # noqa: E501
        story.append(no_result)
        story.append(PageBreak())
        return story
    
    with open(grype_file_path, "r") as file:
        grype_data = json.load(file)

    for match in grype_data["matches"]:
        vulnerability = match["vulnerability"]
        vulnerability_id = vulnerability["id"]
        severity = vulnerability["severity"]
        description = vulnerability["description"]
        fix_versions = vulnerability["fix"]["versions"]
        urls = vulnerability["urls"]
        related_vulns = match["relatedVulnerabilities"]
        related_vulns_id = []
        if related_vulns:
            for i in related_vulns:
                related_vulns_id.append(i["id"])
        else:
            related_vulns_id.append(
                "No related vulnerabilities have been found."
            )  # noqa: E501

        related_vulns_id = ", ".join(related_vulns_id)

        # Create a paragraph with vulnerability information
        paragraph = (
            f"<b>Vulnerability ID:</b> {vulnerability_id}<br/>"
            f"<b>Severity:</b> {severity}<br/>"
            f"<b>Description:</b> {description}<br/>"
            f"<b>Fix Versions:</b> {', '.join(fix_versions)}<br/>"
            f"<b>URLs:</b> {', '.join(urls)}<br/>"
            f"<b>Related Vulnerability ID:</b> {related_vulns_id}<br/><br/>"
        )

        # Add the paragraph to the story with KeepTogether
        story.append(KeepTogether([Paragraph(paragraph, styles["Normal"])]))
    story.append(PageBreak())

    return story


def safety_results(safety_file_path):
    story = []
    safety_heading = Paragraph("<b>Safety Dependency Scan Results</b>", styles["Heading1"])  # noqa: E501
    story.append(safety_heading)

    if safety_file_path is None:
        no_result = Paragraph("There is no result under this scan.", styles["Normal"])  # noqa: E501
        story.append(no_result)
        story.append(PageBreak())
        return story
    
    with open(safety_file_path, "r") as file:
        safety_data = json.load(file)

    pkgs = []

    for package_name, package_info in safety_data.get("scanned_packages", {}).items():  # noqa: E501
        pkgs.append(f"{package_name} {package_info.get('version')}")

    pkgs_str = ", ".join(pkgs)
    pkgs_paragraph = Paragraph(f"<b>Scanned Packages: </b>{pkgs_str}<br/><br/>", styles["Normal"])  # noqa: E501
    story.append(pkgs_paragraph)

    vuln_list = Paragraph("<b>Vulnerabilities Found in Packages: </b><br/><br/>", styles["Normal"])  # noqa: E501
    story.append(vuln_list)

    for vuln in safety_data.get("vulnerabilities", []):
        if vuln:
            pkg_name = vuln.get("package_name")
            vuln_id = vuln.get("vulnerability_id")
            cve = vuln.get("CVE")
            analyzed_version = vuln.get("analyzed_version")
            advisory = vuln.get("advisory")
            more_info = vuln.get("more_info_url")

            paragraph = (
                f"<b>Package Name:</b> {pkg_name}<br/>"
                f"<b>Vulnerability ID:</b> {vuln_id}<br/>"
                f"<b>CVE:</b> <code>{cve}</code><br/>"
                f"<b>Analyzed Version:</b> {analyzed_version}<br/>"
                f"<b>Advisory:</b> <code>{advisory}</code><br/>"
                f"<b>More info:</b> <code>{more_info}</code><br/><br/>"
            )

            story.append(KeepTogether([Paragraph(paragraph, styles["Normal"])]))  # noqa: E501
    story.append(PageBreak())

    return story


def secret_results(secret_file_path):
    story = []
    secret_heading = Paragraph("<b>Detect Secrets Scan Results</b>", styles["Heading1"])  # noqa: E501
    story.append(secret_heading)

    if secret_file_path is None:
        no_result = Paragraph("There is no result under this scan.", styles["Normal"])  # noqa: E501
        story.append(no_result)
        story.append(PageBreak())
        return story
    
    with open(secret_file_path, "r") as file:
        secret_data = json.load(file)

    for _, results_list in secret_data["results"].items():
        for result in results_list:
            result_type = result.get("type")
            filename = result.get("filename")
            line_number = result.get("line_number")
            hashed_secret = result.get("hashed_secret")

            paragraph = (
                f"<b>Secret Type:</b> {result_type}<br/>"
                f"<b>File Path:</b> {filename}<br/>"
                f"<b>Line:</b> {line_number}<br/>"
                f"<b>Hashed Secret:</b> {hashed_secret}<br/><br/>"
            )

            story.append(KeepTogether([Paragraph(paragraph, styles["Normal"])]))  # noqa: E501
    story.append(PageBreak())

    return story


def sbom_results(sbom_file_path):
    story = []
    sbom_heading = Paragraph("<b>SBOM with Syft</b>", styles["Heading1"])
    story.append(sbom_heading)

    with open(sbom_file_path, "r") as file:
        sbom_data = json.load(file)

    for component in sbom_data["components"]:
        component_name = component["name"]
        component_type = component["type"]
        component_version = component["version"]
        component_cpe = component.get("cpe", "N/A")  # Added a default value for CPE since it is not always present in the SBOM.   # noqa: E501

        paragraph = (
            f"<b>Type:</b> {component_type}<br/>"
            f"<b>Name:</b> {component_name}<br/>"
            f"<b>Version:</b> <code>{component_version}</code><br/>"
            f"<b>CPE:</b> {component_cpe}<br/><br/>"
        )
        story.append(KeepTogether([Paragraph(paragraph, styles["Normal"])]))
    story.append(PageBreak())

    return story


def generate_pdf(output_filename, **scan_files):  # noqa: E501
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    story = []

    story += bandit_results(scan_files["bandit_file_path"])
    story += grype_results(scan_files["grype_file_path"])
    story += safety_results(scan_files["safety_file_path"])
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
