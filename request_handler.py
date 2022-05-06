from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views.entry_requests import get_all_entries, get_single_entry,create_entry, delete_entry, get_entries_by_search, update_entry
from views.mood_requests import get_all_moods, get_single_mood
from views.tag_requests import get_all_tags


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)
    
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response
        
        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
    def do_OPTIONS(self):
        """Sets the options headers"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()
    def do_GET(self):
        self._set_headers(200)

        response = {}

        parsed = self.parse_url(self.path)
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"
                else:
                    response = f"{get_all_entries()}"
            if resource == "moods":
                if id is not None:
                    response = f"{get_single_mood(id)}"
                else:
                    response = f"{get_all_moods()}"
            if resource == "tags":
                response = f"{get_all_tags()}"
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed
            if key == "q" and resource == "entries":
                response = get_entries_by_search(value)
        self.wfile.write(response.encode())
    def do_POST(self):
        # Set response code to 'Created'
        self._set_headers(201)
        # Q: what is happening here?
        # A:
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        # string to dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_entry = None

        # Add a new animal to the list. 
        if resource == "entries":
            new_entry = create_entry(post_body)

        # Encode the new animal and send in response
            self.wfile.write(f"{new_entry}".encode())
    
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "entries":
            success = update_entry(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())   
            # elif resource == "customers":
            #     if id is not None:
            #         response = f"{get_single_customer(id)}"
            #     else:
            #         response = f"{get_all_customers()}"
            # elif resource == "employees":
            #     if id is not None:
            #         response = f"{get_single_employee(id)}"
            #     else:
            #         response = f"{get_all_employees()}"
            # elif resource == "locations":
            #     if id is not None:
            #         response = f"{get_single_location(id)}"
            #     else:
            #         response = f"{get_all_locations()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        # elif len(parsed) == 3:
        #     ( resource, key, value ) = parsed

        #     # Is the resource `customers` and was there a
        #     # query parameter that specified the customer
        #     # email as a filtering value?
        #     if key == "email" and resource == "customers":
        #         response = get_customers_by_email(value)
        #     if key == "location_id" and resource == "animals":
        #         response = get_animals_by_location(value)
        #     if key == "location_id" and resource == "employees":
        #         response = get_employees_by_location(value)
        #     if key == "status" and resource == "animals":
        #         response = get_animals_by_status(value)

#     # Here's a method on the class that overrides the parent's method.
#     # Q: what method is being overidden
#     # It handles any GET request.
#     # def do_GET(self):
#     #     """Handles GET requests to the server"""
#     #     # Set the response code to 'Ok'
#     #     # uses inherted methods from above
#     #     self._set_headers(200)
#     #     response = {}
#     #     # Your new console.log() that outputs to the terminal
#     #     print(self.path)
        
#     #     # Parse the URL and capture the tuple that is returned
#     #     # Remember: resource is the list and id is the id of a specific dictionary within that list
#     #     (resource, id) = self.parse_url(self.path)

#     #     # It's an if..else statement
#     #     if resource == "animals":            
#     #         # In Python, this is a list of dictionaries
#     #         # In JavaScript, you would call it an array of objects
#     #         if id is not None:
#     #             response = f"{get_single_animal(id)}"

#     #         else:
#     #             response = f"{get_all_animals()}"
#     #     if resource == "locations":            
           
#     #         if id is not None:
#     #             response = f"{get_single_location(id)}"

#     #         else:
#     #             response = f"{get_all_locations()}"
#     #     if resource == "employees":            
            
#     #         if id is not None:
#     #             response = f"{get_single_employee(id)}"

#     #         else:
#     #             response = f"{get_all_employees()}"
#     #     if resource == "customers":            
            
#     #         if id is not None:
#     #             response = f"{get_single_customer(id)}"

#     #         else:
#     #             response = f"{get_all_customers()}"

#     #     # This weird code sends a response back to the client
#     #     self.wfile.write(response.encode())

#     # Here's a method on the class that overrides the parent's method.
#     # It handles any POST request.
#     def do_POST(self):
#         # Set response code to 'Created'
#         self._set_headers(201)
#         # Q: what is happening here?
#         # A:
#         content_len = int(self.headers.get('content-length', 0))
#         post_body = self.rfile.read(content_len)

#         # Convert JSON string to a Python dictionary
#         # string to dictionary
#         post_body = json.loads(post_body)

#         # Parse the URL
#         (resource, id) = self.parse_url(self.path)

#         # Initialize new animal
#         new_animal = None

#         # Add a new animal to the list. 
#         if resource == "animals":
#             new_animal = create_animal(post_body)

#         # Encode the new animal and send in response
#             self.wfile.write(f"{new_animal}".encode())
        

#     #     # Initialize new animal
#     #     new_customer = None

#     #     # Add a new customer to the list. Don't worry about
#     #     # the orange squiggle, you'll define the create_customer
#     #     # function next.
#     #     if resource == "customers":
#     #         new_customer = create_customer(post_body)

#     #     # Encode the new customer and send in response
#     #         self.wfile.write(f"{new_customer}".encode())
#     #     # Set response code to 'Created'
        

#         # Initialize new employee
#         new_employee = None

#         # Add a new employee to the list. Don't worry about
#         # the orange squiggle, you'll define the create_employee
#         # function next.
#         if resource == "employees":
#             new_employee = create_employee(post_body)

#         # Encode the new employee and send in response
#             self.wfile.write(f"{new_employee}".encode())
#         # Set response code to 'Created'
        
#     #     # Initialize new location
#     #     new_location = None

#     #     # Add a new location to the list. Don't worry about
#     #     # the orange squiggle, you'll define the create_location
#     #     # function next.
#     #     if resource == "locations":
#     #         new_location = create_location(post_body)

#     #     # Encode the new location and send in response
#     #         self.wfile.write(f"{new_location}".encode())
#     # # Here's a method on the class that overrides the parent's method.
#     # # It handles any PUT request.

#     # def do_PUT(self):
#     #     # 204 is "no content"; request was successful but do not need to send back updated resource
#     #     self._set_headers(204)
#     #     content_len = int(self.headers.get('content-length', 0))
#     #     post_body = self.rfile.read(content_len)
#     #     post_body = json.loads(post_body)

#     #     # Parse the URL
#     #     (resource, id) = self.parse_url(self.path)

#     #     # Delete a single animal from the list
#     #     if resource == "animals":
#     #         update_animal(id, post_body)
#     #     if resource == "customers":
#     #         update_customer(id, post_body)
#     #     if resource == "employees":
#     #         update_employee(id, post_body)
#     #     if resource == "locations":
#     #         update_location(id, post_body)

#     #     # Encode the new animal and send in response
#     #     self.wfile.write("".encode())
    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "entries":
            delete_entry(id)
        # if resource == "customers":
        #     delete_customer(id)
        # if resource == "employees":
        #     delete_employee(id)
        # if resource == "locations":
        #     delete_location(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

# # This function is not inside the class. It is the starting
# # point of this application.
# main = "startup"
def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

# "__main__" is the what python calls this file
# if this is the main file run startup, if not, we dont run this
# dunderscore hidden function
# script tag, main.js
# it knows that if this is the startup file, then __name__= "__main__"
if __name__ == "__main__":
    main()
