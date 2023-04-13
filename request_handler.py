import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import get_all_entries, get_single_entry, delete_entry, get_entry_by_word,create_new_entry, update_entry, get_all_tags, get_single_tag, get_single_mood, get_all_moods

class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
       

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
     
       
        if '?' not in self.path:
            ( resource, id ) = parsed
            if resource == "moods":
                 if id is not None:
                    response = get_single_mood(id)
                    if response is not None:
                        self._set_headers(200)
                    else:
                        self._set_headers(404)
                        response = {
                            "message": "There is no mood for that id"}

                 else:
                    self._set_headers(200)
                    response = get_all_moods()
            if resource == "tags":
                 if id is not None:
                    response = get_single_tag(id)
                    if response is not None:
                        self._set_headers(200)
                    else:
                        self._set_headers(404)
                        response = {
                            "message": "There is no tag for that id"}

                 else:
                    self._set_headers(200)
                    response = get_all_tags()
            if resource == "entries":
                if id is not None:
                    response = get_single_entry(id)
                    if response is not None:
                        self._set_headers(200)
                    else:
                        self._set_headers(404)
                        response = {
                            "message": "There is no entry for that id"}

                else:
                    self._set_headers(200)
                    response = get_all_entries()

        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed
            self._set_headers(200)
            if query.get('q'):
                response = get_entry_by_word(query['q'][0])
            # see if the query dictionary has an email key
            # if query.get('email') and resource == 'customers':
            #     response = get_customers_by_email(query['email'][0])
            # elif query.get('name') and resource == 'customers':
            #     response = get_customers_by_name(query['name'][0])
            # elif query.get('location_id') and resource == 'animals':
            #     response = get_animal_by_location(query['location_id'][0])
            # elif query.get('status') and resource == 'animals':
            #     response = get_animal_by_status(query['status'][0])
            # elif query.get('location_id') and resource == 'employees':
            #     response = get_employee_by_location(query['location_id'][0])

        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_entry = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "entries":
            new_entry = create_new_entry(post_body)
       
        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_entry).encode())

        # if resource == "locations":
        #     new_location = create_location(post_body)

        # # Encode the new animal and send in response
        # self.wfile.write(json.dumps(new_location).encode())

        # if resource == "employees":
        #     new_employee = create_employee(post_body)

        # # Encode the new animal and send in response
        # self.wfile.write(json.dumps(new_employee).encode())

        # if resource == "customers":
        #     new_customer = create_customer(post_body)

        # # Encode the new animal and send in response
        # self.wfile.write(json.dumps(new_customer).encode())
    # A method that handles any PUT request.
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        success = False

        if resource == "entries":
            success = update_entry(id, post_body)
    # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

    # Encode the new animal and send in response
        self.wfile.write("".encode())
    #     if resource == "locations":
    #         update_location(id, post_body)

    # # Encode the new animal and send in response
    #     self.wfile.write("".encode())
    #     if resource == "employees":
    #         update_employee(id, post_body)

    # # Encode the new animal and send in response
    #     self.wfile.write("".encode())
    #     if resource == "customers":
    #         update_customer(id, post_body)

    # # Encode the new animal and send in response
    #     self.wfile.write("".encode())
    
    def do_DELETE(self):
    # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)


        if resource == "entries":
            delete_entry(id)

    # Encode the new animal and send in response
        self.wfile.write("".encode())
    #     if resource == "locations":
    #         delete_location(id)

    # # Encode the new animal and send in response
    #     self.wfile.write("".encode())

    #     if resource == "employees":
    #         delete_employee(id)

    # # Encode the new animal and send in response
    #     self.wfile.write("".encode())
    #     if resource == "customers":
    #         delete_customer(id)

    # Encode the new animal and send in response
        self.wfile.write("".encode())
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
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

    # add this import to the top of the file


    # replace the parse_url function in the class
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            print(query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)
# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
