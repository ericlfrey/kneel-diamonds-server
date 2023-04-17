import sqlite3
import json
from models import Order, Metal, Size, Style

# from .metals_requests import get_single_metal
# from .sizes_requests import get_single_size
# from .styles_requests import get_single_style

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
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.jewelry_id,
            o.timestamp,
            m.metal metal_name,
            m.price metal_price,
            sz.carets size_carets,
            sz.price size_price,
            st.style style_name,
            st.price style_price
        FROM Orders o
        JOIN Metals m
            ON m.id = o.metal_id
        JOIN Sizes sz
            ON sz.id = o.size_id
        JOIN Styles st
            ON st.id = o.style_id
        """)

        orders = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            order = Order(row['id'], row['metal_id'], row['size_id'],
                          row['style_id'], row['jewelry_id'], row['timestamp'])

            metal = Metal(
                row['metal_id'], row['metal_name'], row['metal_price'])
            size = Size(
                row['size_id'], row['size_carets'], row['size_price'])
            style = Style(
                row['style_id'], row['style_name'], row['style_price'])

            order.metal = metal.__dict__
            order.size = size.__dict__
            order.style = style.__dict__

            orders.append(order.__dict__)

    return orders


def get_single_order(id):
    """gets a single order"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.jewelry_id,
            o.timestamp
        FROM orders o
        WHERE o.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        order = Order(data['id'], data['metal_id'], data['size_id'],
                      data['style_id'], data['jewelry_id'], data['timestamp']
                      )

        return order.__dict__
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


def create_order(new_order):
    """Creates a new order"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Orders
            ( metal_id, size_id, style_id, jewelry_id, timestamp )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_order['metal_id'], new_order['size_id'],
              new_order['style_id'], new_order['jewelry_id'], new_order['timestamp'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_order['id'] = id

    return new_order

    # # Get the id value of the last order in the list
    # max_id = ORDERS[-1]["id"]

    # # Add 1 to whatever that number is
    # new_id = max_id + 1

    # # Add an `id` property to the order dictionary
    # order["id"] = new_id

    # # Add the order dictionary to the list
    # ORDERS.append(order)

    # # Return the dictionary with `id` property added
    # return order


def delete_order(id):
    """Deletes single order"""
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM orders
        WHERE id = ?
        """, (id, ))
    # # Initial -1 value for order index, in case one isn't found
    # order_index = -1

    # # Iterate the ORDERS list, but use enumerate() so that you
    # # can access the index value of each item
    # for index, order in enumerate(ORDERS):
    #     if order["id"] == id:
    #         # Found the order. Store the current index.
    #         order_index = index

    # # If the order was found, use pop(int) to remove it from list
    # if order_index >= 0:
    #     ORDERS.pop(order_index)


def update_order(id, new_order):
    """Updates order with Replacement"""
    # Iterate the ORDERS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break
