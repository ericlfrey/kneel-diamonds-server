ORDERS = [
    {
        "id": 1,
        "metalId": 3,
        "sizeId": 2,
        "styleId": 3,
        "jewelryId": 2,
        "timestamp": 1614659931693
    }
]


def get_all_orders():
    """Handles Server request for all ORDERS"""
    return ORDERS


def get_single_order(id):
    """gets a single order"""
    requested_order = None

    for order in ORDERS:
        if order["id"] == id:
            requested_order = order

    return requested_order
