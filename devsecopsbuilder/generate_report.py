import json
import os
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
    with open(bandit_file_path, "r") as file:
        bandit_data = json.load(file)

    bandit_heading = Paragraph("<b>Bandit Scan Results</b>", styles["Heading1"])  # noqa: E501
    story.append(bandit_heading)

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
    with open(grype_file_path, "r") as file:
        grype_data = json.load(file)

    grype_heading = Paragraph("<b>Grype Scan Results</b>", styles["Heading1"])
    story.append(grype_heading)

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


def generate_pdf(output_filename, bandit_file_path, grype_file_path, safety_file_path, secret_file_path, sbom_file_path=None):  # noqa: E501
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    story = []

    story += bandit_results(bandit_file_path)
    story += grype_results(grype_file_path)
    story += safety_results(safety_file_path)
    story += secret_results(secret_file_path)
    
    # SBOM results can be enormous. Therefore, this segment is optional.
    if sbom_file_path:
        story += sbom_results(sbom_file_path)

    doc.build(story)


if __name__ == "__main__":
    # Define the base directory and scan type
    base_dir = "command_outputs"
    scan_type = "python-scan"

    # File names
    bandit_file = "bandit_result.json"
    grype_file = "grype.json"
    safety_file = "dependency_scan.json"
    secret_file = "secrets.json"
    sbom_file = "sbom.json"

    # Output filename
    output_filename = "output.pdf"

    # Construct file paths using base directory, scan type, and file names
    bandit_file_path = os.path.join(base_dir, scan_type, bandit_file)
    grype_file_path = os.path.join(base_dir, scan_type, grype_file)
    safety_file_path = os.path.join(base_dir, scan_type, safety_file)
    secret_file_path = os.path.join(base_dir, scan_type, secret_file)
    sbom_file_path = os.path.join(base_dir, scan_type, sbom_file)  # Optional

    generate_pdf(output_filename, bandit_file_path, grype_file_path, safety_file_path, secret_file_path)  # noqa: E501

    print("Report generated.")
