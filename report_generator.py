class ReportGenerator:
    def generate(self, findings, filename="WebSec_Report.pdf"):
        from fpdf import FPDF
        import textwrap

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'WebSec_AutoGuard Vulnerability Report', ln=True, align='C')
        pdf.ln(10)

        pdf.set_font('Arial', size=12)
        pdf.multi_cell(0, 8, "This report summarizes the findings from a web security scan. It lists detected vulnerabilities, their risk levels, and recommended actions.")
        pdf.ln(10)

        col_widths = [70, 90, 30]
        row_height = 8

        # Table headers
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(col_widths[0], row_height, "Form", border=1)
        pdf.cell(col_widths[1], row_height, "Vulnerability", border=1)
        pdf.cell(col_widths[2], row_height, "Risk", border=1)
        pdf.ln(row_height)

        # Table rows
        pdf.set_font('Arial', '', 10)
        for f in findings:
            form = textwrap.wrap(str(f.get("form", "N/A")), 35)
            vuln = textwrap.wrap(str(f.get("vuln", "N/A")), 45)
            risk = f.get("risk", "N/A")

            max_lines = max(len(form), len(vuln))
            for i in range(max_lines):
                pdf.cell(col_widths[0], row_height, form[i] if i < len(form) else "", border=1)
                pdf.cell(col_widths[1], row_height, vuln[i] if i < len(vuln) else "", border=1)
                pdf.cell(col_widths[2], row_height, risk if i == 0 else "", border=1, align='C')
                pdf.ln(row_height)

        # Save file
        pdf.output(filename)
        print(f"PDF Report saved as {filename}")
