import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field

def latest_financial_index(data: dict):
    for index, financial in enumerate(data.get("financials", [])):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index):
    try:
        return data["financials"][financial_index]["pnl"]["lineItems"]["netRevenue"]
    except (KeyError, IndexError):
        return 0.0

def total_borrowing(data: dict, financial_index):
    try:
        borrowings = (
            data["financials"][financial_index]["bs"]["longTermBorrowings"] +
            data["financials"][financial_index]["bs"]["shortTermBorrowings"]
        )
        return borrowings / total_revenue(data, financial_index) if total_revenue(data, financial_index) > 0 else 0
    except (KeyError, IndexError):
        return 0.0

def iscr(data: dict, financial_index):
    try:
        profit_before_interest_tax = data["financials"][financial_index]["pnl"]["profitBeforeInterestTax"]
        depreciation = data["financials"][financial_index]["pnl"]["depreciation"]
        interest_expenses = data["financials"][financial_index]["pnl"]["interestExpenses"]

        return (profit_before_interest_tax + depreciation + 1) / (interest_expenses + 1)
    except (KeyError, IndexError):
        return 0.0

def iscr_flag(data: dict, financial_index):
    if iscr(data, financial_index) >= 2:
        return FLAGS.GREEN
    else:
        return FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index):
    if total_revenue(data, financial_index) >= 50_000_000:
        return FLAGS.GREEN
    else:
        return FLAGS.RED

def borrowing_to_revenue_flag(data: dict, financial_index):
    if total_borrowing(data, financial_index) <= 0.25:
        return FLAGS.GREEN
    else:
        return FLAGS.AMBER
