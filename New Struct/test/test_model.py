import sys 
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.loader import text_extract_from

pdf_text = text_extract_from("ReglementEvalEST.pdf")
print(pdf_text)