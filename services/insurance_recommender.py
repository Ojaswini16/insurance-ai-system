def recommend_insurance(data):

    if data["family_members"] > 3:
        return "Family Health Insurance Plan"

    if data["age"] < 30:
        return "Young Adult Health Insurance"

    if data["risk_segmentation"] == 3:
        return "High Risk Coverage Plan"

    return "Standard Health Insurance Plan"