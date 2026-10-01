import streamlit as st
import requests
from io import BytesIO
from docx import Document
from fpdf import FPDF


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.write(
    "Generate customizable legal documents using Generative AI."
)

# -----------------------------
# INPUT SECTION
# -----------------------------

document_type = st.selectbox(
    "Document Type",
    [
        "Non-Disclosure Agreement",
        "Employment Contract",
        "Lease Agreement",
        "Service Agreement",
        "Business Agreement"
    ]
)

parties = st.text_area(
    "Parties",
    placeholder="Example: Company: ABC Technologies, Employee: John"
)

terms = st.text_area(
    "Terms and Conditions",
    placeholder="Enter the important terms and conditions..."
)

dates = st.text_input(
    "Effective Date / Dates",
    placeholder="Example: Effective Date: 30 September 2026"
)

# -----------------------------
# GENERATE DOCUMENT
# -----------------------------

if st.button("Generate Legal Document"):

    if not parties or not terms or not dates:
        st.warning("Please fill in all required fields.")
    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/generate",
                json=payload
            )

            if response.status_code == 200:

                data = response.json()
                document = data["document"]

                st.success("Legal document generated successfully!")

                # -----------------------------
                # DOCUMENT PREVIEW
                # -----------------------------

                st.subheader("Generated Legal Document")

                edited_document = st.text_area(
                    "Preview / Edit Document",
                    value=document,
                    height=500
                )

                # -----------------------------
                # DOWNLOAD TXT
                # -----------------------------

                st.download_button(
                    "Download TXT",
                    edited_document,
                    file_name="LegalEase_Document.txt",
                    mime="text/plain"
                )

                # -----------------------------
                # DOWNLOAD DOCX
                # -----------------------------

                docx_file = BytesIO()

                doc = Document()

                for line in edited_document.split("\n"):
                    doc.add_paragraph(line)

                doc.save(docx_file)

                docx_file.seek(0)

                st.download_button(
                    "Download DOCX",
                    data=docx_file.getvalue(),
                    file_name="LegalEase_Document.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

                # -----------------------------
                # DOWNLOAD PDF
                # -----------------------------

                pdf = FPDF()
                pdf.add_page()

                pdf.set_font("Arial", size=11)

                for line in edited_document.split("\n"):

                    safe_line = line.encode(
                        "latin-1",
                        "replace"
                    ).decode("latin-1")

                    pdf.multi_cell(
                        0,
                        7,
                        safe_line
                    )

                pdf_output = pdf.output(dest="S")

                if isinstance(pdf_output, str):
                    pdf_bytes = pdf_output.encode("latin-1")
                else:
                    pdf_bytes = bytes(pdf_output)

                st.download_button(
                    "Download PDF",
                    data=pdf_bytes,
                    file_name="LegalEase_Document.pdf",
                    mime="application/pdf"
                )

            else:

                st.error(
                    f"Document generation failed: {response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "FastAPI server is not running. "
                "Please start Uvicorn first."
            )

        except Exception as e:

            st.error(f"Error: {e}")