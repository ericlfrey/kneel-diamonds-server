from .metals_requests import get_single_metal
from .sizes_requests import get_single_size
from .styles_requests import get_single_style

ORDERS = [
    {
        "id": 1,
        "metal_id": 3,
        "size_id": 2,
        "style_id": 3,
        "jewelry_id": 2,
        "timestamp": 1614659931693
    }
]


def get_all_orders():
    """Handles Server request for all ORDERS"""
    return ORDERS


def get_single_order(id):
    """gets a single order"""
    # requested_order = None

    # for order in ORDERS:
    #     if order["id"] == id:
    #         requested_order = order.copy()

    #         matching_metal = get_single_metal(requested_order["metal_id"])
    #         matching_size = get_single_size(requested_order["size_id"])
    #         matching_style = get_single_style(requested_order["style_id"])

    #         requested_order["metal"] = matching_metal
    #         requested_order["size"] = matching_size
    #         requested_order["style"] = matching_style

    #         if matching_metal is not None:
    #             del requested_order["metal_id"]
    #         if matching_size is not None:
    #             del requested_order["size_id"]
    #         if matching_style is not None:
    #             del requested_order["style_id"]

    # return requested_order


def create_order(order):
    """Creates a new order"""
    # Get the id value of the last order in the list
    max_id = ORDERS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the order dictionary
    order["id"] = new_id

    # Add the order dictionary to the list
    ORDERS.append(order)

    # Return the dictionary with `id` property added
    return order


def delete_order(id):
    """Deletes single order"""
    # Initial -1 value for order index, in case one isn't found
    order_index = -1

    # Iterate the ORDERS list, but use enumerate() so that you
    # can access the index value of each item
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Store the current index.
            order_index = index

    # If the order was found, use pop(int) to remove it from list
    if order_index >= 0:
        ORDERS.pop(order_index)


def update_order(id, new_order):
    """Updates order with Replacement"""
    # Iterate the ORDERS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break
