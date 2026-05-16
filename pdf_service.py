from jinja2 import Environment
from jinja2 import FileSystemLoader

from playwright.sync_api import sync_playwright

import os


def generate_pdf(data, submission_id):
    output_dir = "generated_pdfs"

    os.makedirs(output_dir, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template("certificate.html")

    background_image = os.path.abspath(
        "templates/certificate-template.png"
    )

    html_content = template.render(
        name=data.name,
        purpose=data.purpose,
        strengths=data.strengths,
        skills=data.skills,
        values=data.values,
        passions=data.passions,
        background_image=background_image
    )

    temp_html_path = os.path.join(
        output_dir,
        f"temp_{submission_id}.html"
    )

    with open(temp_html_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    safe_name = data.name.strip().replace(" ", "_")

    output_pdf_path = os.path.join(
        output_dir,
        f"{submission_id}_Purpose_card_{safe_name}.pdf"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch()

        page = browser.new_page()

        page.goto(
            f"file:///{os.path.abspath(temp_html_path)}"
        )

        page.pdf(
            path=output_pdf_path,
            format="A4",
            landscape=True,
            print_background=True,
            margin={
                "top": "0mm",
                "right": "0mm",
                "bottom": "0mm",
                "left": "0mm"
            }
        )

        browser.close()

    return output_pdf_path