import pandas as pd 
from app.models.statement import Transacao
from app.services.validator import get_signed_amount_cents
from pathlib import Path

def transaction_to_dataframe(transactions: list[Transacao]):

    records = []

    for transaction in transactions:

        records.append(
            {
            "date": transaction.date_time,
            "description_raw": transaction.description_raw,
            "description_normalized": transaction.description_normalized,
            "amount_cents": transaction.amount_cents,
            "signed_amount_cents": get_signed_amount_cents(transaction),
            "direction": transaction.direction,
            "transaction_type": transaction.transaction_type,
            "balance_after_cents": transaction.balance_after_cents,
            "doc_number": transaction.document_number,
            "transaction_code": transaction.transaction_code,
            "source_page": transaction.source_page,
            "source_text": transaction.source_text,
            "extraction_method": transaction.extraction_method,
            "warnings": "|".join(transaction.warnings),
            "review_required": len(transaction.warnings) > 0,
            }
        )

    df = pd.DataFrame(records)

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.sort_values(by=["date","source_page"], ascending=[True,True]).reset_index(drop=True)

    return df

def export_df(df: pd.DataFrame, file_name:str, output_directory: Path):

    output_directory.mkdir(parents=True, exist_ok=True)

    csv_path = (output_directory/f"{file_name}.csv")
    json_path = (output_directory/f"{file_name}.json")

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    df.to_json(json_path, orient="records", indent=2, force_ascii=False)

    return {"csv_path":csv_path, "json_path":json_path}
