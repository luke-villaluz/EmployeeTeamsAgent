# src/ragagent/load_excel.py

from langchain_core.documents import Document
import pandas as pd
from typing import List

def load_excel_data(filepath: str) -> List[Document]:
    """
    Load rows from the first sheet of an Excel file and convert each row into a LangChain Document.
    Each row is converted into a pipe-delimited string with metadata for row index.
    """
    df = pd.read_excel(filepath, sheet_name=0)  # Load only the first sheet
    df = df.dropna(how="all")  # Drop rows where all values are NaN

    documents = []
    for index, row in df.iterrows():
        row_text = " | ".join(
            f"{col}: {str(val)}" for col, val in row.items() if pd.notna(val)
        )
        if row_text.strip():
            documents.append(
                Document(
                    page_content=row_text,
                    metadata={"row_index": index}
                )
            )

    return documents
