DATABASE = {
    "ORDERS": [
        {
            "id": 1,
            "metal_id": 3,
            "size_id": 2,
            "style_id": 3,
            "jewelry_id": 2,
            "timestamp": 1614659931693
        }
    ],
    "METALS": [
        {
            "id": 1,
            "metal": "Sterling Silver",
            "price": 12.42
        },
        {
            "id": 2,
            "metal": "14K Gold",
            "price": 736.4
        },
        {
            "id": 3,
            "metal": "24K Gold",
            "price": 1258.9
        },
        {
            "id": 4,
            "metal": "Platinum",
            "price": 795.45
        },
        {
            "id": 5,
            "metal": "Palladium",
            "price": 1241
        }
    ],
    "SIZES": [
        {
            "id": 1,
            "carets": 0.5,
            "price": 405
        },
        {
            "id": 2,
            "carets": 0.75,
            "price": 782
        },
        {
            "id": 3,
            "carets": 1,
            "price": 1470
        },
        {
            "id": 4,
            "carets": 1.5,
            "price": 1997
        },
        {
            "id": 5,
            "carets": 2,
            "price": 3638
        }
    ],
    "STYLES": [
        {
            "id": 1,
            "style": "Classic",
            "price": 500
        },
        {
            "id": 2,
            "style": "Modern",
            "price": 710
        },
        {
            "id": 3,
            "style": "Vintage",
            "price": 965
        }
    ]
}


def get_all(db_key):
    """For GET requests to collection"""
    return DATABASE[db_key.upper()]


def retrieve(db_key, id):
    """For GET requests to a single resource"""
    requested_dict = None

    for dict in DATABASE[db_key.upper()]:
        if dict["id"] == id:
            requested_dict = dict

    return requested_dict


def get_single_order(id, query_params):
    """gets a single order"""
    requested_order = None
    for order in DATABASE["ORDERS"]:
        if order["id"] == id:
            requested_order = order.copy()
    if query_params is not None:
        for param in query_params:
            with_id = param + "_id"
            if param or with_id in requested_order:
                        #then i want to expand the order on the fk

                        #get the fk
                fk = requested_order[with_id]
                        #get the resource
                database_key = param + "S"
                resource = retrieve(database_key, fk)
                        #add the resource to the order
                requested_order[param] = resource
                del requested_order[with_id]

            # # get the foreign keys









            # resources = ["metals", "sizes", "styles"]
            # foreign_keys = ["metal_id", "size_id", "style_id"]
            # resources_fks = {
            #     "metals": "metal_id",
            #     "sizes": "size_id",
            #     "styles": "style_id"
            # }
            # if len(query_params) > 0:
            #     searched_params = {
            #         res in resources_fks[res] for res in query_params if res in resources_fks[res]}
            #     print(f"SEARCHED {searched_params}")

            # # for param in query_params:
            # #     if param

            # price = 0
            # for index, resource in enumerate(resources):
            #     # gets corresponding resources by foreign keys
            #     matching_resource = retrieve(
            #         resource, requested_order[foreign_keys[index]])
            #     # sets them inside the order dictionary
            #     requested_order[resource] = matching_resource
            #     # gets the prices from the corresponding resources and adds them
            #     price += requested_order[resource]["price"]
            #     requested_order["price"] = price

            # for param in foreign_keys:
            #     if param is not None:
            #         del requested_order[param]

    return requested_order


def create(new_dict, db_key):
    """For POST requests to a collection"""
    cap_db_key = db_key.upper()
    max_id = DATABASE[cap_db_key][-1]["id"]
    new_id = max_id + 1
    new_dict["id"] = new_id
    DATABASE[cap_db_key].append(new_dict)

    return new_dict


def update(id, new_dict, db_key):
    """For PUT requests to a single resource"""
    cap_db_key = db_key.upper()
    for index, dict in enumerate(DATABASE[cap_db_key]):
        if dict["id"] == id:
            DATABASE[cap_db_key][index] = new_dict
            break


def delete(db_key, id):
    """For DELETE requests to a single resource"""
    cap_db_key = db_key.upper()
    key_index = -1

    for index, dict in enumerate(DATABASE[cap_db_key]):
        if dict["id"] == id:
            key_index = index

    if key_index >= 0:
        DATABASE[cap_db_key].pop(key_index)
