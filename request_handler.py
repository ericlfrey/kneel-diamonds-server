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
    delete_order,
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
        self._set_headers(200)

        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            if id is not None:
                response = get_single_metal(id)
            else:
                response = get_all_metals()

        if resource == "orders":
            if id is not None:
                response = get_single_order(id)
            else:
                response = get_all_orders()

        if resource == "sizes":
            if id is not None:
                response = get_single_size(id)
            else:
                response = get_all_sizes()

        if resource == "styles":
            if id is not None:
                response = get_single_style(id)
            else:
                response = get_all_styles()

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server """
        self._set_headers(201)
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
            new_order = create_order(post_body)
            self.wfile.write(json.dumps(new_order).encode())

        if resource == "metals":
            new_metal = create_metal(post_body)
            self.wfile.write(json.dumps(new_metal).encode())

        if resource == "sizes":
            new_size = create_size(post_body)
            self.wfile.write(json.dumps(new_size).encode())

        if resource == "styles":
            new_style = create_style(post_body)
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
        # set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single order from the list
        if resource == "orders":
            delete_order(id)
        if resource == "metals":
            delete_metal(id)
        if resource == "sizes":
            delete_size(id)
        if resource == "styles":
            delete_style(id)

        # Encode the new order and send in a response
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
