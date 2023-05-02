from flask import Flask, render_template
from flask import request
import subprocess
import base64
import git
import json
from google.cloud import storage

app = Flask(__name__)

ids = []

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    # Note: The call returns a response only when the iterator is consumed.
    for blob in blobs:
        print(blob.name)

def rate():
    output = subprocess.getoutput("./run url_cache.txt")
    try:
        # Get the json output of backend and set variables
        output = json.loads(output)
        url = output["URL"]
        net_score = output["NET_SCORE"]
        ramp_up = output["RAMP_UP_SCORE"]
        correctness = output["CORRECTNESS_SCORE"]
        bus_factor = output["BUS_FACTOR_SCORE"]
        responsiveness = output["RESPONSIVE_MAINTAINER_SCORE"]
        license_score = output["LICENSE_SCORE"]
    except:
        # If error, throw invalid error
        url = "Invalid URL"
        net_score = "N/A"
        ramp_up = "N/A"
        correctness = "N/A"
        bus_factor = "N/A"
        responsiveness = "N/A"
        license_score = "N/A"

    # Return metrics to html, while reloading page
    return render_template('webpage.html', data_url=url, net_score=net_score, ramp_up=ramp_up, correctness=correctness
                           , bus_factor=bus_factor, responsive_maintainer=responsiveness, license=license_score)



def encode_base_64(message):
    message_in_bytes = message.encode('ascii')
    message_in_base_64 = base64.b64encode(message_in_bytes)
    return message_in_base_64


def decode_base_64(message_in_base_64):
    message_in_bytes = message_in_base_64.encode('ascii')
    message = base64.b64decode(message_in_bytes)
    return message


def getName(url):
    slash_count = 0
    index = 0
    for letter in url:
        index += 1
        if letter == "/":
            slash_count += 1
        if slash_count == 2:
            break
    return url[index:]

@app.route('/')
def index():
    return render_template(template_name_or_list='webpage.html')

@app.route('/package', methods=['POST'])
def create_package():
    url = ""
    ##############
    # query package in database before anything else
    package_query = ""
    query_response = ""
    rating = 0
    id = 0
    name = ""
    # add the foll
    #
    # owing to the database
    # metadata: name, version, id
    # data: content (and maybe JSProgram?)
    ######################################
    # rating = x

    for header in request.headers():
        if header == 'URL':
            url = request.args.get('URL')
            git.Repo.clone_from(url)
            name = getName(url)
            break
        if header == 'Content':
            package_contents = decode_base_64(request.args.get('Content'))
            url = package_contents['homepage']
            git.Repo.clone_from(url)
            name = getName(url)
            break

    # call main.py here
    if rating >= 0.5:
        if len(ids) > 0:
            id = ids[len(ids) - 1] + 1
            # write id and name to database
        storage_client = storage.Client()
        bucket = storage_client.bucket('autonomous-time-309221.appspot.com')  # updated bucket name
        # blob name your_bucket_name/path_in_gcs
        blob = bucket.blob('packages')
        with blob.open('r') as file:
            if name in file.readlines():
                return "Package exists already." + "409"
        with blob.open('w') as file:
            file.write([id, name])
        return str(id) +  "Success. Check the ID in the returned metadata for the official ID." + "201"

    # query directory for package id
    # if it exists return error else create package

    # else
    # rate package
    else:
        return "-1", "Package is not uploaded due to the disqualified rating." + "424"


@app.route('/package/byName/{name}', methods=['DELETE'])
def delete_package():
    # use query commands to delete package
    # check return statement of query
    name = request.args.get('name')
    query = ""

    query_response = 0
    storage_client = storage.Client()
    bucket = storage_client.bucket('autonomous-time-309221.appspot.com')
    # blob name your_bucket_name/path_in_gcs
    blob = bucket.blob('packages')
    with blob.open('r') as file:
        lines = file.readlines()
    with blob.open('w') as file:
        file.truncate()
        for line in lines:
            if line[1] == request.args.get('name'):
                query_response = 1
            else:
                file.write(line)

    if query_response == 0:
        return "Package is deleted", 200
    if query_response == "":
        return "Package does not exist", 404
    return


@app.route('/package/{id}', methods=['GET', 'DELETE', 'PUT'])
def get_package_by_ID():
    ident = request.args.get('id')
    storage_client = storage.Client()
    bucket = storage_client.bucket('autonomous-time-309221.appspot.com')
    # blob name your_bucket_name/path_in_gcs
    blob = bucket.blob('packages')
    with blob.open('r') as file:
        lines = file.readlines()
        for line in lines:
            if lines[0] == ident:
                return line
    return 404, "Package does not exist"


def delete_package_by_ID():
    query_response = 0
    ident = request.args.get('id')
    storage_client = storage.Client()
    bucket = storage_client.bucket('autonomous-time-309221.appspot.com')
    # blob name your_bucket_name/path_in_gcs
    blob = bucket.blob('packages')
    with blob.open('r') as file:
        lines = file.readlines()
    with blob.open('w') as file:
        file.truncate()
        for line in lines:
            if line[0] == ident:
                query_response = 1
            else:
                file.write(line)
    if ident not in ids:
        return "Package does not exist", 404
    if query_response == 0:
        return "Package is deleted", 200
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
                repo = git.Repo.clone_from(request.args.get('URL'))
                repo.git.checkout('b', request.args.get('Version'))
                # write back to database
                # gitpy.clone(request.args.get('URL'))
                break
            if header == 'Content':
                package_contents = decode_base_64(request.args.get('Content'))
                url = package_contents['homepage']
                repo = git.Repo.clone_from(url)
                repo.git.checkout('b', request.args.get('Version'))
                # write back to database
                break

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
    return rate()


@app.route('/reset', methods=['DELETE'])
def reset():
    storage_client = storage.Client()
    bucket = storage_client.bucket('autonomous-time-309221.appspot.com')
    # blob name your_bucket_name/path_in_gcs
    blob = bucket.blob('packages')
    with blob.open('w') as file:
        file.truncate()
    return "Registry is reset", 200


@app.route('/packages', methods=['POST'])
def get_ID_packages():
    offset = request.args.get('offset')
    packages = []
    if offset is None:
        # print first page of entries
        storage_client = storage.Client()
        bucket = storage_client.bucket('autonomous-time-309221.appspot.com')
        # blob name your_bucket_name/path_in_gcs
        blob = bucket.blob('packages')
        with blob.open('r') as file:
            lines = file.readlines
        return lines[0:min(len(lines), 20)], 200
    elif offset is not None:
        # print offset num entries
        storage_client = storage.Client()
        bucket = storage_client.bucket('autonomous-time-309221.appspot.com')
        # blob name your_bucket_name/path_in_gcs
        blob = bucket.blob('packages')
        with blob.open('r') as file:
            lines = file.readlines
        if offset > len(lines):
            return "Too many packages returned.", 413
        return lines[0:offset], 200

    return "unexpected error", 413


# add url to rate to url_cache.txt
@app.route("/submit")
def submit():
    with open('url_cache.txt', 'a') as f:
        open("url_cache.txt", "w").close()
        url = request.args.get('url')
        f.write(url)
    return ('', 204)


# flask api call for running rating functionality





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("begin test")
    app.run(debug=True, host='10.128.0.2', use_reloader=False, port=8001)
    # host='10.128.0.2',
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
