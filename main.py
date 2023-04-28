from flask import Flask
from flask import request
import git
import base64

app = Flask(__name__)

ids = []

def encode_base_64(message):
    message_in_bytes = message.encode('ascii')
    message_in_base_64 = base64.b64encode(message_in_bytes)
    return  message_in_base_64
def decode_base_64(message_in_base_64):
    message_in_bytes = message_in_base_64.encode('ascii')
    message = base64.b64decode(message_in_bytes)
    return message

@app.route('/package', methods=['POST'])
def create_package(token):
    url = ""
    ##############
    # query package in database before anything else
    package_query = ""
    query_response = ""
    rating = 0
    id = 0
    if query_response == None:
        # add the following to the database
        # metadata: name, version, id
        # data: content (and maybe JSProgram?)
        ######################################
        # rating = x
        if rating >= 0.5:
            for header in request.headers:
                if header == 'URL':
                    git.clone(request.args.get('URL'))
                    break
                if header == 'Content':
                    package_contents = decode_base_64(request.args.get('Content'))
                    url = package_contents['homepage']
                    git.clone(url)

            if len(ids) > 0:
                id = ids[len(ids) - 1] + 1
                # write id and name to database
        return id, "Success. Check the ID in the returned metadata for the official ID.", 201
    elif query_response != None:
        return "-1", "Package exists already.", 409

    # query directory for package id
    # if it exists return error else create package

    # else
    # rate package
    else:
        return "-1", "Package is not uploaded due to the disqualified rating.", 424

@app.route('/package/byName/{name}', methods=['GET', 'DELETE'])
def get_history_of_package(token):
    name = request.args.get('name')
    query = ""
    query_response = ""
    history = ""
    if query_response == "":
        return query_response, 200
    elif name == None or token == None:
        # also check if token is invalid
        return "There is missing field(s) in the PackageData/AuthenticationToken or it is formed improperly, or the AuthenticationToken is invalid.", 400
    elif query_response == "":
        return "No such package", 404
    else:
        return "unexpected error", 500
def delete_package(token):
    # use query commands to delete package
    # check return statement of query
    name = request.args.get('name')
    query = ""
    query_response = ""
    if query_response == "":
        return "Package is deleted", 200
    elif name == None or token == None:
        # also check if token is invalid
        return "There is missing field(s) in the PackageData/AuthenticationToken or it is formed improperly, or the AuthenticationToken is invalid.", 400
    if query_response == "":
        return "Package does not exist", 404
    return

@app.route('/package/{id}', methods=['GET', 'DELETE', 'PUT'])
def get_package_by_ID():
    ident = request.args.get('id')

    return

def delete_package_by_ID(token):
    ident = request.args.get('id')
    if ident not in ids:
        return "Package does not exist", 404
    query = ""
    query_response = ""
    if query_response == "":
        return "Package is deleted", 200
    elif ident is None or token is None:
        # also check if token is invalid
        return "There is missing field(s) in the PackageData/AuthenticationToken or it is formed improperly, or the AuthenticationToken is invalid.", 400
    if query_response == "":
        return "Package does not exist", 404
    return

def update_package():
    ident = request.args.get('id')
    query = ""
    query_respone = ""
    # git clone <url> -b <version>
    # clone, cd, checkout
    if query_respone == "":
        # delete package from database
        for header in request.headers:
            if header == 'URL':
                git.clone(request.args.get('URL'))
                break
            if header == 'Content':
                package_contents = decode_base_64(request.args.get('Content'))
                url = package_contents['homepage']
                git.clone(url)

            git.checkout('b', request.args.get('Version'))
        return "Version is updated", 200
    # return "There is missing field(s) in the PackageID/AuthenticationToken or it is formed improperly, or the AuthenticationToken is invalid.", 400
    # return "Package does not exist", 404
    # return

@app.route('/package/{id}/rate', methods=['GET'])
def rate_package():
    ident = request.args.get('id')
    score = -1
    # query backend
    # add package to database
    return score

@app.route('/packages', methods=['POST'])
def get_ID_packages():
    offset = request.args.get('offset')
    if offset == None:
        # print first page of entries
        return
    if offset != None:
        # print offset num entries
        return
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("begin test")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
