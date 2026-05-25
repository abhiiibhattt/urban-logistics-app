def humanize_status(status: str) -> str:
    """
    Convert status constants like IN_TRANSIT -> In Transit
    """
    if not status:
        return ""
    return status.replace("_", " ").title()
