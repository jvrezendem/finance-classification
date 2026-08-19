import hashlib
from app.models.statement import Transacao

def normalize_description(description: str) -> str:
    return " ".join(description.lower().split())

def create_transaction_fingerprint(transaction: Transacao) -> str:
    components = [
        str(transaction.date or ""),
        normalize_description(transaction.description_raw),
        str(transaction.amount_cents or ""),
        transaction.direction,
        str(transaction.document_number or ""),
        str(transaction.balance_after_cents or ""),
    ]
    raw_value = "|".join(components)
    return hashlib.sha256(raw_value.encode("utf-8")).hexdigest()

def mark_possible_duplicates(transactions: list[Transacao]) -> list[Transacao]:
    known_fingerprints: set[str] = set()
    for transaction in transactions:
        fingerprint = create_transaction_fingerprint(transaction)
        if fingerprint in known_fingerprints:
            transaction.warnings.append("possible_duplicate")
        else:
            known_fingerprints.add(fingerprint)
        transaction.warnings = sorted(set(transaction.warnings))
    return transactions

    
