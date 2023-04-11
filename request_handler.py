import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import (
    get_all_metals,
    get_single_metal,
    create_metal,
    delete_metal,
    update_metal,
    get_all_styles,
    get_single_style,
    create_style,
    delete_style,
    update_style,
    get_all_orders,
    get_single_order,
    create_order,
    # delete_order,
    update_order,
    get_all_sizes,
    get_single_size,
    create_size,
    delete_size,
    update_size
)


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        """This function splits the client path string into parts to isolate the requested id"""
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        try:
            id = int(path_params[2])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id)  # This is a tuple

    def do_GET(self):
        """Handles GET requests to the server """
        # self._set_headers(200)

        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            if id is not None:
                response = get_single_metal(id)

                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = "message: That metal is not currently in stock for jewelry"
            else:
                self._set_headers(200)
                response = get_all_metals()

        if resource == "orders":
            if id is not None:
                response = get_single_order(id)

                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = "message: That order is not currently in stock for jewelry"
            else:
                self._set_headers(200)
                response = get_all_orders()

        if resource == "sizes":
            if id is not None:
                response = get_single_size(id)

                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = "message: That size is not currently in stock for jewelry"
            else:
                self._set_headers(200)
                response = get_all_sizes()

        if resource == "styles":
            if id is not None:
                response = get_single_style(id)

                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = "message: That style is not currently in stock for jewelry"
            else:
                self._set_headers(200)
                response = get_all_styles()

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server """
        # self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new order
        new_order = None
        new_metal = None
        new_size = None
        new_style = None

        # Add a new order to the list. Don't worry about
        # the orange squiggle, you'll define the create_order
        # function next.
        if resource == "orders":
            orders_list = ["metal_id", "size_id",
                           "style_id", "jewelry_id", "timestamp"]
            if all(orders_list_item in post_body for orders_list_item in orders_list):
                self._set_headers(201)
                new_order = create_order(post_body)
            else:
                self._set_headers(400)
                new_order = {
                    "message": f"{'metal_id is required' if 'metal_id' not in post_body else ''}{'size_id is required' if 'size_id' not in post_body else ''}{'style_id is required' if 'style_id' not in post_body else ''}{'jewelry_id is required' if 'jewelry_id' not in post_body else ''}{'timestamp is required' if 'timestamp' not in post_body else ''}"
                }
            self.wfile.write(json.dumps(new_order).encode())

        if resource == "metals":
            metals_list = ["metal", "price"]
            if all(metals_list_item in post_body for metals_list_item in metals_list):
                self._set_headers(201)
                new_metal = create_metal(post_body)
            else:
                self._set_headers(400)
                new_metal = {
                    "message": f"{'metal is required' if 'metal' not in post_body else ''}{'price is required' if 'price' not in post_body else ''}"
                }
            self.wfile.write(json.dumps(new_metal).encode())

        if resource == "sizes":
            sizes_list = ["carets", "price"]
            if all(sizes_list_item in post_body for sizes_list_item in sizes_list):
                self._set_headers(201)
                new_size = create_size(post_body)
            else:
                self._set_headers(400)
                new_size = {
                    "message": f"{'carets is required' if 'carets' not in post_body else ''}{'price is required' if 'price' not in post_body else ''}"
                }
            self.wfile.write(json.dumps(new_size).encode())

        if resource == "styles":
            styles_list = ["style", "price"]
            if all(styles_list_item in post_body for styles_list_item in styles_list):
                self._set_headers(201)
                new_style = create_style(post_body)
            else:
                self._set_headers(400)
                new_style = {
                    "message": f"{'style is required' if 'style' not in post_body else ''}{'price is required' if 'price' not in post_body else ''}"
                }
            self.wfile.write(json.dumps(new_style).encode())

    def do_PUT(self):
        """Handles PUT requests to the server """
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Update a single order in the list
        if resource == "orders":
            update_order(id, post_body)
        if resource == "metals":
            update_metal(id, post_body)
        if resource == "sizes":
            update_size(id, post_body)
        if resource == "styles":
            update_style(id, post_body)

        # Encode the order and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handles DELETE requests to server"""

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single order from the list
        if resource == "orders":
            self._set_headers(405)
            error_message = {
                "message": "Deleting orders requires contacting the company directly."
            }
            self.wfile.write(json.dumps(error_message).encode())
        if resource == "metals":
            self._set_headers(204)
            delete_metal(id)
            self.wfile.write("".encode())
        if resource == "sizes":
            self._set_headers(204)
            delete_size(id)
            self.wfile.write("".encode())
        if resource == "styles":
            self._set_headers(204)
            delete_style(id)
            self.wfile.write("".encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
