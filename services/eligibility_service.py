def check_claim_eligibility(data):

    age = data["age"]
    tenure = data["tenure"]
    premium = data["premium_amount"]
    claim = data["claim_amount"]
    family = data["family_members"]
    risk = data["risk_segmentation"]

    # Rule 1: Policy must be active for at least 1 year
    if tenure < 1:
        return False, "Policy tenure too short to claim insurance."

    # Rule 2: Claim amount should not exceed 10x premium
    if claim > premium * 10:
        return False, "Claim amount unusually high compared to premium."

    # Rule 3: Age validation
    if age < 18 or age > 100:
        return False, "Age not valid for insurance claim."

    # Rule 4: Family members check
    if family <= 0:
        return False, "Invalid family member count."

    # Rule 5: Risk segmentation check
    if risk not in [1,2,3]:
        return False, "Invalid risk segmentation value."

    # If all checks pass
    return True, "Claim is eligible for fraud analysis."