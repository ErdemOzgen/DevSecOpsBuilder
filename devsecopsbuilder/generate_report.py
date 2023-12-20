import json
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, KeepTogether, PageBreak

def generate_pdf(output_filename):
    # Load your JSON data from the file
    with open("command_outputs/python-scan/bandit_result.json", "r") as file:
        bandit_data = json.load(file)
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    bandit_heading = Paragraph("<b>Bandit Scan Results</b>", styles['Heading1'])
    story.append(bandit_heading)

    for result in bandit_data["results"]:
        code_snippet = result['code']
        filename = result['filename']
        line_number = result['line_number']
        issue_severity = result['issue_severity']
        issue_text = result['issue_text']
        code_snippet = code_snippet.replace("\n", "<br/>")
        # Create a paragraph
        paragraph = f"<b>File:</b> {filename}, <b>Line:</b> {line_number}<br/>" \
                    f"<b>Severity:</b> {issue_severity}<br/>" \
                    f"<b>Issue:</b> {issue_text}<br/>" \
                    f"<b>Code Snippet:</b> <code>{code_snippet}</code><br/><br/>"

        # Add the paragraph to the story
        story.append(KeepTogether([Paragraph(paragraph, styles['Normal'])]))
    story.append(PageBreak())

    grype_heading = Paragraph("<b>Grype Scan Results</b>", styles['Heading1'])
    story.append(grype_heading)

    with open("command_outputs/python-scan/grype.json", "r") as file:
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
            related_vulns_id.append("No related vulnerabilities have been found.")

        related_vulns_id = ", ".join(related_vulns_id)

        # Create a paragraph with vulnerability information
        paragraph = f"<b>Vulnerability ID:</b> {vulnerability_id}<br/>" \
                    f"<b>Severity:</b> {severity}<br/>" \
                    f"<b>Description:</b> {description}<br/>" \
                    f"<b>Fix Versions:</b> {', '.join(fix_versions)}<br/>" \
                    f"<b>URLs:</b> {', '.join(urls)}<br/>"\
                    f"<b>Related Vulnerability ID:</b> {related_vulns_id}<br/><br/>"

        # Add the paragraph to the story with KeepTogether
        story.append(KeepTogether([Paragraph(paragraph, styles['Normal'])]))
    story.append(PageBreak())

    safety_heading = Paragraph("<b>Safety Dependency Scan Results</b>", styles['Heading1'])
    story.append(safety_heading)
    with open("command_outputs/python-scan/dependency_scan.json", "r") as file:
        safety_data = json.load(file)

    pkgs = []

    for package_name, package_info in safety_data.get("scanned_packages", {}).items():
        pkgs.append(f"{package_name} {package_info.get('version')}")

    pkgs = ", ".join(pkgs)      
    pkgs = Paragraph(f"<b>Scanned Packages: </b>{pkgs}<br/><br/>", styles['Normal'])
    story.append(pkgs)

    vuln_list = Paragraph(f"<b>Vulnerabilities Found in Packages: </b><br/><br/>", styles['Normal'])
    story.append(vuln_list)

    for vuln in safety_data.get("vulnerabilities", []):
        if vuln:
            pkg_name = vuln.get("package_name")
            vuln_id = vuln.get("vulnerability_id")
            cve = vuln.get("CVE")
            analyzed_version = vuln.get("analyzed_version")
            advisory = vuln.get("advisory")
            more_info = vuln.get("more_info_url")

            paragraph = f"<b>Package Name:</b> {pkg_name}<br/>" \
                f"<b>Vulnerability ID:</b> {vuln_id}<br/>" \
                f"<b>CVE:</b> <code>{cve}</code><br/>"\
                f"<b>Analyzed Version:</b> {analyzed_version}<br/>" \
                f"<b>Advisory:</b> <code>{advisory}</code><br/>"\
                f"<b>More info:</b> <code>{more_info}</code><br/><br/>"

            story.append(KeepTogether([Paragraph(paragraph, styles['Normal'])]))
    story.append(PageBreak())

    secret_heading = Paragraph("<b>Detect Secrets Scan Results</b>", styles['Heading1'])
    story.append(secret_heading)
    with open("command_outputs/python-scan/secrets.json", "r") as file:
        secret_data = json.load(file)

    for _, results_list in secret_data["results"].items():
        
        for result in results_list:
            result_type = result.get("type")
            filename = result.get("filename")
            line_number = result.get("line_number")
            hashed_secret = result.get("hashed_secret")

            paragraph = f"<b>Secret Type:</b> {result_type}<br/>" \
                f"<b>File Path:</b> {filename}<br/>" \
                f"<b>Line:</b> {line_number}<br/>"\
                f"<b>Hashed Secret:</b> {hashed_secret}<br/><br/>"
            
            story.append(KeepTogether([Paragraph(paragraph, styles['Normal'])]))
    story.append(PageBreak())

    #SBOM results can be enormous. Therefore, this segment is commented but you can simply uncomment and use it.
    """sbom_heading = Paragraph("<b>SBOM with Syft</b>", styles['Heading1'])
    story.append(sbom_heading)
    with open("command_outputs/python-scan/sbom.json", "r") as file:
        sbom_data = json.load(file)

    for component in sbom_data["components"]:
        component_name = component["name"]
        component_type = component["type"]
        component_version = component["version"]
        component_cpe = component["cpe"]
        
        paragraph = f"<b>Type:</b> {component_type}<br/>" \
            f"<b>Name:</b> {component_name}<br/>" \
            f"<b>Version:</b> <code>{component_version}</code><br/>"\
            f"<b>CPE:</b> {component_cpe}<br/><br/>"
        story.append(KeepTogether([Paragraph(paragraph, styles['Normal'])]))
    """

    doc.build(story)
    


# Set the output filename
output_filename = "output.pdf"

# Generate the PDF
generate_pdf(output_filename)

print("Report generated.")





