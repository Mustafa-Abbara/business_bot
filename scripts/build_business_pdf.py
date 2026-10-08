"""Generate me/about_business.pdf (Stage 1). Run from the repo root: python scripts/build_business_pdf.py

Dev-only dependency: fpdf2. Text is plain ASCII (core PDF fonts) and there are no tables,
so pypdf can extract it cleanly in Stage 2.
"""
from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).resolve().parent.parent / "me" / "about_business.pdf"

TITLE = "EchoNest"
TAGLINE = "Your memories, told your way."

# Each section: (heading, [paragraphs]); a paragraph starting with "- " is a bullet,
# one starting with "Q: " is shown in bold.
SECTIONS = [
    ("1. Company Overview", [
        "EchoNest is a digital-memory studio. We transform a person's photos, voice recordings, written "
        "memories, important dates and captions into a personalized digital memory experience. Instead of "
        "leaving photos in a folder, we organize them into a story: a graduation journey, a family timeline, "
        "a relationship story, a travel memory or a personal life archive.",
        "EchoNest is an online studio. Our team is based in Beirut and works with clients anywhere.",
    ]),
    ("2. Mission", [
        "EchoNest helps people preserve meaningful moments by turning scattered digital memories into "
        "organized, personal stories that can be revisited and shared.",
    ]),
    ("3. How EchoNest Works", [
        "- Step 1, Consultation: a free 20-minute online call to understand the story you want to tell.",
        "- Step 2, Booking: you choose a service and pay a 50% deposit.",
        "- Step 3, Upload: we send you a secure upload link for your photos, recordings and written memories.",
        "- Step 4, Production: our designers build your story, captions and timeline.",
        "- Step 5, Review: you review the draft and request changes (two revision rounds are included).",
        "- Step 6, Delivery: you receive your private shareable page and pay the remaining balance.",
    ]),
    ("4. Services", [
        "Every project is delivered as a private shareable page with a chronological story, captions, "
        "short narratives, key milestones and a visual timeline.",
        "- Memory Capsule: a compact digital story built around one event. Includes up to 60 photos and "
        "up to 3 voice recordings.",
        "- Event Story: designed for weddings, graduations, anniversaries, reunions and similar events. "
        "Includes up to 150 photos and personal messages from guests.",
        "- Life Timeline: a larger project that combines memories from many years into one chronological story.",
        "- Legacy Edition: our premium service for preserving someone's life story. The customer provides "
        "photographs, documents and memories, and we include up to 3 recorded interview sessions, held online.",
        "- Corporate Story: a company-history package for startups and organizations, covering founder "
        "stories, milestones and employee anniversaries. Corporate Story projects are led by Maya Haddad.",
    ]),
    ("5. Pricing", [
        "- Memory Capsule: $79",
        "- Event Story: $149",
        "- Life Timeline: $299",
        "- Legacy Edition: $499",
        "- Corporate Story: no fixed price. Each Corporate Story is quoted after a consultation with the client.",
        "Payment: a 50% deposit is paid at booking and the remaining balance is paid on delivery.",
    ]),
    ("6. Target Customers", [
        "- Families: family histories, anniversaries, birthdays and reunions.",
        "- Individuals: graduations, relationships, travels and personal milestones.",
        "- Organizations: employee anniversaries, founder stories and company milestones.",
    ]),
    ("7. Team", [
        "- Maya Haddad, Founder & Creative Director. Specializes in digital storytelling and archival design.",
        "- Karim Saad, Memory Experience Designer. Creates the timelines, layouts and visual stories.",
        "- Lina Farhat, Client Experience Manager. Handles customer communication and project coordination, "
        "and is the first point of contact for every new client.",
    ]),
    ("8. Unique Value Proposition", [
        "EchoNest does not simply store memories. It gives them a narrative. A cloud-storage service answers "
        "\"Where are my photos?\" EchoNest answers \"What story do these photos tell?\"",
    ]),
    ("9. Supported Materials", [
        "- Photos in JPG, PNG or HEIC format.",
        "- Standard audio recordings in MP3, WAV or M4A format.",
        "- Written memories, captions and important dates.",
        "Materials are never collected through the chat. After booking, the team sends a secure upload link.",
    ]),
    ("10. Project Timeline", [
        "Typical projects take 5 to 10 business days from the moment all materials are uploaded. "
        "The Legacy Edition takes 3 to 4 weeks because it includes interviews.",
    ]),
    ("11. Revision Policy", [
        "Every project includes two revision rounds. Revision requests are made on the draft page during review.",
    ]),
    ("12. Privacy Policy", [
        "Customer-provided material is treated as private project material. It is used only to build the "
        "customer's project and is never shared with third parties. Each shareable page is password-protected "
        "and stays online for 5 years. Customers can ask us to delete their page and materials at any time.",
    ]),
    ("13. Refund Policy", [
        "Customers may cancel before production begins and receive a full refund of their deposit. "
        "Once production has started, the deposit is not refundable.",
    ]),
    ("14. Contact Information", [
        "To start a project or request a Corporate Story quote, leave your name and email with our assistant. "
        "Lina Farhat's team replies within one business day. Team hours: Monday to Friday, "
        "9:00 AM to 6:00 PM (Beirut time).",
    ]),
    ("15. Frequently Asked Questions", [
        "Q: What does EchoNest actually create?",
        "A: A private shareable page that tells your story with photos, captions, short narratives, "
        "milestones and a visual timeline.",
        "Q: How long does a project take?",
        "A: Typically 5 to 10 business days after all materials are uploaded. The Legacy Edition takes 3 to 4 weeks.",
        "Q: Can I send my photos in the chat?",
        "A: No. After booking, the team sends you a secure upload link.",
        "Q: Who can see my memory page?",
        "A: Only people you share it with. Every page is password-protected.",
        "Q: How long does my page stay online?",
        "A: 5 years. You can ask us to delete it earlier at any time.",
        "Q: Do I pay everything upfront?",
        "A: No. You pay a 50% deposit at booking and the rest on delivery.",
        "Q: Who will work on my project?",
        "A: Lina Farhat coordinates your project, Karim Saad designs it, and Maya Haddad oversees the "
        "creative direction.",
    ]),
    ("16. Services We Do Not Currently Offer", [
        "- Film restoration.",
        "- Physical photo restoration.",
        "- Professional videography.",
        "- Forensic recovery of deleted files.",
    ]),
    ("17. Example Projects", [
        "- A Memory Capsule for a 2026 university graduation, with photos from the ceremony and short "
        "messages from friends.",
        "- A Legacy Edition preserving a grandfather's life story, built from family photos, old letters "
        "and three recorded interviews.",
    ]),
]


def build():
    pdf = FPDF(format="A4")
    pdf.set_title(f"About {TITLE}")
    pdf.set_author(TITLE)
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 12, TITLE, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 13)
    pdf.cell(0, 8, TAGLINE, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    for heading, paragraphs in SECTIONS:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 9, heading, new_x="LMARGIN", new_y="NEXT")
        for para in paragraphs:
            pdf.set_font("Helvetica", "B" if para.startswith("Q: ") else "", 11)
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
