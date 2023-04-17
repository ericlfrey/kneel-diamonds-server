import json
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from repository import (get_all, retrieve, update, create, get_single_order)
from views import get_all_orders


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        """This function splits the client path string into parts to isolate the requested id"""
        url_components = urlparse(path)
        print(f"URL {url_components}")
        path_params = url_components.path.strip("/").split("/")
        print(f"PATH {path_params}")
        query_params = url_components.query.split("&")
        print(f"QUERY {query_params}")
        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id, query_params)

    def get_all_or_single(self, resource, id, query_params):
        """Tests whether to get All items, or get Single item"""
        if id is not None:
            if resource == "orders":
                response = get_single_order(id, query_params)
            else:
                response = retrieve(resource, id)
        else:
            if resource == "orders":
                response = get_all_orders()
            else:
                response = get_all(resource)
        if response is not None:
            self._set_headers(200)
        else:
            self._set_headers(404)
            response = {"message": "Not found"}
        return response

    def do_GET(self):
        """Handles GET requests to the server """
        response = None
        (resource, id, query_params) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id, query_params)
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id, query_params) = self.parse_url(self.path)
        new_order = None

        if resource == "orders":
            orders_list = (["metal_id",
                            "size_id",
                            "style_id",
                            "jewelry_id",
                            "timestamp"])
            if all(orders_list_item in post_body for orders_list_item in orders_list):
                self._set_headers(201)
                new_order = create(post_body, resource)
            else:
                self._set_headers(400)
                key_list = [
                    key_item for key_item in orders_list if key_item not in post_body]
                key_string = ', '.join([str(item) for item in key_list])
                new_order = {
                    "message": f"{key_string} is required"
                }
            self.wfile.write(json.dumps(new_order).encode())
        else:
            self._set_headers(405)
            error_message = {
                "message": "That function is not allowed."
            }
            self.wfile.write(json.dumps(error_message).encode())

    def do_PUT(self):
        """Handles PUT requests to the server """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id, query_params) = self.parse_url(self.path)

        if resource == "metals":
            metal_dict = retrieve(resource, id)
            if post_body["metal"] == metal_dict["metal"]:
                self._set_headers(204)
                update(id, post_body, resource)
                self.wfile.write("".encode())
            else:
                self._set_headers(405)
                error_message = {"message": "Only price can be updated."}
                self.wfile.write(json.dumps(error_message).encode())
        else:
            self._set_headers(405)
            error_message = {
                "message": "That function is not allowed."
            }
            self.wfile.write(json.dumps(error_message).encode())

    def do_DELETE(self):
        """Handles DELETE requests to server"""
        (resource, id, query_params) = self.parse_url(self.path)
        self._set_headers(405)
        error_message = {
            "message": f"Deleting {resource.lower()} requires contacting the company directly."
        }
        self.wfile.write(json.dumps(error_message).encode())

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
