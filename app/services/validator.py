from datetime import date
from app.models.statement import Transacao
def validate_transaction(transaction: Transacao,period_start: date | None = None, period_end: date | None = None,):
    
    warnings = list(transaction.warnings)
    if transaction.date is None:
        warnings.append("missing_date")
    if transaction.amount_cents is None:
        warnings.append("missing_amount")
    elif transaction.amount_cents <= 0:
        warnings.append("invalid_amount")
    if not transaction.description_raw.strip():
        warnings.append("missing_description")
    if transaction.direction == "unknown":
        warnings.append("unknown_direction")
    if transaction.source_page < 1:
        warnings.append("invalid_source_page")
    if not transaction.source_text.strip():
        warnings.append("missing_source_text")
    if (
        transaction.date
        and period_start
        and transaction.date < period_start
    ):
        warnings.append("date_before_statement_period")
    return transaction.model_copy(update={"warnings": warnings})
    if (
        transaction.date
        and period_end
        and transaction.date > period_end
    ):
        warnings.append("date_after_statement_period")

    transaction.warnings = sorted(set(warnings))
    return transaction

def get_signed_amount_cents(transaction: Transacao):
    if transaction.amount_cents is None:
        return None
    if transaction.direction == "debit":
        return -abs(transaction.amount_cents)
    if transaction.direction == "credit":
        return abs(transaction.amount_cents)
    return transaction.amount_cents

def validate_balance_transition(previous_balance_cents: int, transaction: Transacao, current_balance_cents: int, tolerance_cents: int = 2,):
    signed_amount = get_signed_amount_cents(transaction)
    if signed_amount is None:
        return False
    expected_balance = previous_balance_cents + signed_amount
    difference = abs(current_balance_cents - expected_balance)
    return difference <= tolerance_cents

    