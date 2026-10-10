"""
Depreciation Job — YEARLY JOB
Apply annual depreciation to all active tax assets.
Mirrors sp_update_depreciation stored procedure.
"""


def run():
    # For all active tax assets with depreciation_rate > 0
    #   where acquired_date year < current year:
    # current_value = current_value * (1 - depreciation_rate)
    # Update updated_at timestamp
    # Log count of assets updated
    pass
