import os
import sys
import win32com.client

def convert_to_pdf(docx_path="Design Analysis Report.docx", pdf_path="Design Analysis Report.pdf"):
    abs_docx = os.path.abspath(docx_path)
    abs_pdf = os.path.abspath(pdf_path)
    
    print(f"Converting DOCX to PDF...")
    print(f"  Source: {abs_docx}")
    print(f"  Target: {abs_pdf}")
    
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    word.AutomationSecurity = 3  # msoAutomationSecurityForceDisable
    
    try:
        doc = word.Documents.Open(abs_docx, ReadOnly=True, AddToRecentFiles=False)
        doc.SaveAs(abs_pdf, FileFormat=17) # 17 = wdFormatPDF
        doc.Close(False)
        print(f"Conversion successful! PDF size: {os.path.getsize(abs_pdf)} bytes")
    finally:
        word.Quit()

if __name__ == "__main__":
    convert_to_pdf()
