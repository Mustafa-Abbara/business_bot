"""Generate me/about_business.pdf (Stage 1). Run from the repo root: python scripts/build_business_pdf.py

Dev-only dependency: fpdf2. Text is plain ASCII (core PDF fonts) and there are no tables,
so pypdf can extract it cleanly in Stage 2.
"""
from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).resolve().parent.parent / "me" / "about_business.pdf"

# Each section: (heading, [paragraphs]); a paragraph starting with "- " is a bullet.
SECTIONS = [
    ("Mission", [
        "Cedar Code Academy makes practical programming and STEM skills accessible to students aged "
        "12 to 25 in Lebanon through small-group, project-based learning. We believe every student can "
        "learn to build real software when classes are small, hands-on and patient.",
    ]),
    ("Services and Prices", [
        "- Python Foundations: an 8-week group course for complete beginners, two 90-minute sessions per "
        "week. Price: $240 for the full course.",
        "- University CS Tutoring: one-on-one help with university courses such as data structures, "
        "algorithms and programming labs. Price: $25 per hour.",
        "- Web Development Bootcamp: a 12-week course covering HTML, CSS, JavaScript and React. "
        "Price: $450. Open to students aged 16 and above.",
        "- Robotics & Arduino Club: a Saturday club for ages 12 to 16 where students build and program "
        "small robots. Price: $60 per month.",
        "- Corporate & School Workshops: custom trainings designed for companies and schools. These do not "
        "have a fixed price; each workshop is quoted after a consultation with the client.",
    ]),
    ("Team", [
        "- Rami Haddad, Co-founder and Director. A former full-stack software engineer with six years of "
        "industry experience. Rami teaches the Web Development Bootcamp.",
        "- Lina Khoury, Co-founder and Head of Curriculum. Lina holds an MSc in Computer Engineering and "
        "designs all course material. She leads Python Foundations and University CS Tutoring.",
        "- Omar Saade, Co-founder and Robotics Lead. An electrical engineer who previously worked in "
        "industrial automation. Omar runs the Robotics & Arduino Club.",
    ]),
    ("Unique Value Proposition", [
        "- Small groups: never more than 6 students per group.",
        "- Project-based: every course ends with a real project that students can show in a portfolio.",
        "- Bilingual teaching: classes are taught in English, with explanations in Arabic whenever needed.",
        "- Free trial: the first session of any group course is free.",
        "- Reliable classroom: the centre has generator backup power and a backup internet line, so "
        "sessions are not interrupted by power cuts.",
    ]),
    ("Location and Hours", [
        "Address: Makdessi Street, Hamra, Beirut, 3rd floor.",
        "Opening hours: Monday to Friday, 2:00 PM to 9:00 PM. Saturday, 9:00 AM to 5:00 PM. Closed on Sundays.",
    ]),
    ("Frequently Asked Questions", [
        "Q: Do I need my own laptop?",
        "A: No. We lend laptops to students during sessions at the centre. For online sessions you need "
        "your own computer.",
        "Q: Can I study online?",
        "A: Yes. Python Foundations and University CS Tutoring are available online. The Web Development "
        "Bootcamp and the Robotics & Arduino Club are in person only.",
        "Q: Is there a free trial?",
        "A: Yes. The first session of any group course is free.",
        "Q: Can I pay in installments?",
        "A: The Web Development Bootcamp can be paid in 3 monthly installments of $150. Other services are "
        "paid in full at registration.",
        "Q: What is your refund policy?",
        "A: You get a full refund if you cancel before the second session of a course. After the second "
        "session, fees are not refundable.",
        "Q: Do you give certificates?",
        "A: Yes. Students who complete Python Foundations or the Web Development Bootcamp receive a "
        "certificate of completion.",
        "Q: What ages do you accept?",
        "A: The Robotics & Arduino Club is for ages 12 to 16. The Web Development Bootcamp is for ages 16 "
        "and above. Python Foundations and University CS Tutoring are open to students aged 12 to 25.",
    ]),
    ("Contact Policy", [
        "To book a course or request a workshop quote, leave your name and email with our assistant. "
        "Our team replies within one business day. We never share your contact details with third parties.",
    ]),
]


def build():
    pdf = FPDF(format="A4")
    pdf.set_title("About Cedar Code Academy")
    pdf.set_author("Cedar Code Academy")
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, "Cedar Code Academy", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 12)
    pdf.cell(0, 8, "Coding and robotics tutoring in Beirut", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    for heading, paragraphs in SECTIONS:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 9, heading, new_x="LMARGIN", new_y="NEXT")
        for para in paragraphs:
            bold = para.startswith("Q: ")
            pdf.set_font("Helvetica", "B" if bold else "", 11)
            if para.startswith("- "):
                pdf.set_x(pdf.l_margin + 4)
                pdf.multi_cell(0, 6, "-  " + para[2:], new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.multi_cell(0, 6, para, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        pdf.ln(3)

    OUT.parent.mkdir(exist_ok=True)
    pdf.output(str(OUT))
    print(f"Wrote {OUT} ({pdf.pages_count} pages)")


if __name__ == "__main__":
    build()
