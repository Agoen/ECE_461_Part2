from flask import Flask, render_template
from flask import request
import requests
import subprocess
import base64
import git
import json
import os
import zipfile
from google.cloud import storage

app = Flask(__name__)

ids = []
names = []
iD = -1;


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    # Note: The call returns a response only when the iterator is consumed.
    for blob in blobs:
        print(blob.name)

def rate_return_as_string(id):
    url_fileptr = open('url_file.txt', 'r')
    temp_fileptr = open('temp_file.txt', 'w')
    lines = url_fileptr.readlines()
    for line in lines:
        line.split(' ')
        if id == line[0]:
            temp_fileptr.write(line[1])
            break

    output = subprocess.getoutput("./run temp_file.txt")
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
    return f'data_url={url}, net_score={net_score}, ramp_up={ramp_up}, correctness={correctness}, bus_factor={bus_factor}, responsive_maintainer={responsiveness}, license={license_score}'

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
    return  net_score
    # return render_template('webpage.html', data_url=url, net_score=net_score, ramp_up=ramp_up, correctness=correctness
    #                       , bus_factor=bus_factor, responsive_maintainer=responsiveness, license=license_score)


def encode_base_64(message):
    message_in_bytes = message.encode('ascii')
    message_in_base_64 = base64.b64encode(message_in_bytes)
    return message_in_base_64


def decode_base_64(message_in_base_64):
    message_in_bytes = message_in_base_64.encode('ascii')
    message = base64.b64decode(message_in_bytes)
    return message.decode()


def getName(url):
    split_url = url.split('/')
    if split_url[len(split_url)-1] == "" or split_url[len(split_url)-1] == "\n":
        name = split_url[len(split_url)-2]
        owner =  split_url[len(split_url)-3]
    else:
        name = split_url[len(split_url)-1]
        owner =  split_url[len(split_url)-2]
    return name, owner

    
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
    content = None
    rating = 0.5
    flag = 0
    id = ""
    name = ""
    # add the foll
    #
    # owing to the database
    # metadata: name, version, id
    # data: content (and maybe JSProgram?)
    ######################################
    # rating = x

    # print(request.data) 
    parse_json = json.loads(request.data)
    for header in parse_json:
        # print(header)
        if header == 'URL' and parse_json['URL'] is not None and parse_json['URL'] is not "" and parse_json['Content'] is None:
            flag = 1
            # url = parse_json['URL']
            with open('url_cache.txt', 'w') as url_cache:
                url_cache.write(parse_json['URL'])
            # name = getName(url)
            # path = f'autonomous-time-309221.appspot.com/cloned_packages/{name}'
            #git.Git(path).clone(url)
            # git.Repo.clone_from(url=url,to_path= path)
            break
        if header == 'Content' and parse_json['Content'] is not None and parse_json['Content'] != "" and parse_json['URL'] is None:
            
            package_contents = (parse_json['Content'])
            flag = 1
            package_contents_decoded = base64.b64decode(package_contents)
            k = open('temp_zip_file.zip', 'wb')
            k.write(package_contents_decoded)
            zipfile_contents = zipfile.ZipFile("temp_zip_file.zip", 'r')
            zipfile_contents.extractall('temp_content_dir')
            zipfile_contents.close()
            os.system('rm temp_zip_file.zip')
           
            os.system('cd temp_content_dir')
            os.system('cd *')
            os.system('mv temp_content_dir/*/* temp_content_dir')
            json_file = open('temp_content_dir/package.json')
            json_file_lines = json.load(json_file)
            with open('url_cache.txt', 'w') as t:
                t.write(json_file_lines['homepage'])
            os.system('rm -rf temp_content_dir')
            content = package_contents
            # print(package_contents)
            # package_contents = decode_base_64(parse_json['Content'])
            # url = package_contents['homepage']
            # name = getName(url)
            # path = f'autonomous-time-309221.appspot.com/cloned_packages/{name}'
            # git.Repo.clone_from(url=url, to_path=path)
            break
    if flag == 0:
        return "Invalid input." + " 400"
    if url == "":
        with open('url_cache.txt', 'r') as f:
            j =  f.readlines()
        url = j[len(j)-1].split("\n")[0]
        name, owner = getName(url)

    if name == None or name == "":
        return "403"
    rating = rate()
    if rating == 'N/A':
        return "Package is not uploaded due to the disqualified rating." + "424"
    # call main.py here
    if float(rating) >= 0.5:
            # write id and name to database
            # http://34.121.45.140:8001/package/id/%7Bid%7D?0
        names.append(name)
        storage_client = storage.Client()
        bucket = storage_client.bucket('autonomous-time-309221.appspot.com')  # updated bucket name
        # blob name your_bucket_name/path_in_gcs
        # blob = bucket.blob('packages.txt')
        
        t = open('local_package_directory.txt', 'r')
        l = t.readlines()
        if len(l) > 0:
            last_line = l[-1]

        id = name.lower()
        for line in l:
            if id in line:
                return "Package exists already." + " 409"
        t.close()
        path = f'autonomous-time-309221.appspot.com/cloned_packages/{name}'
        git.Repo.clone_from(url=url, to_path=path)
        '''
        with blob.open('w') as file:
            file.write([id, name])
        return str(id) +  "Success. Check the ID in the returned metadata for the official ID." + "201"
        '''
        '''
        headers = {
            "Authorization" : 'token ghp_r5***',
            "Accept": 'application/vnd.github.v3+json'
        #    "Accept": '*.*',
        }
        p = f'https://api.github.com/repos/{owner}/{name}/zipball/'''
        '''
        p = requests.get(p, headers=headers)
        print(p)
        '''
        package_dir_fileptr = open('local_package_directory.txt' ,'a')
        d = {"metadata": {"name": name, "Version": "1.0.0", "ID": id}, "data": {"Content":content, "JSProgram":""}}
        index_string = f"{id} {name}\n"
        url_string = f"{id} {url}\n"
        url_fileptr = open("url_file.txt", "a")
        url_fileptr.write(url_string)
        # index =  id + " " + name + "\n"
        corresp_json_fileptr = open('local_package_directory_json.txt', 'a')
        corresp_json_fileptr.write(str(d))
        package_dir_fileptr.write(index_string)
        return json.dumps(d, indent=1) +  " Success. Check the ID in the returned metadata for the official ID." + " 201"
        #blob.upload_from_filename('local_package_directory.txt')
    # query directory for package id
    # if it exists return error else create package

    # else
    # rate package
    else:
        return "Package is not uploaded due to the disqualified rating." + "424"


@app.route('/package/byName/{name}', methods=['GET','DELETE'])
def byNameMethods():
    if request.method == 'GET':
    # http://34.121.45.140:8001/package/id/%7Bid%7D?id=1
        name = request.args.get('name')
        #bucket = storage_client.bucket('autonomous-time-309221.appspot.com')
        # blob name your_bucket_name/path_in_gcs
        # blob = bucket.blob('api_calls')
        # listBlobs()
        with open('local_package_directory.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                print(line)
                print(line[2:])
                if name in line:
                    return line
        return str(404) +  " Package does not exist"

    if request.method == 'DELETE':
        name = request.args.get('name')
        lines_to_write = []
        query_response = 0
        f = open('local_package_directory.txt', 'r')
        lines = f.readlines()
        for line in lines:
            if name in line:
                query_response = 1
            else:
                lines_to_write.append(line)
        f.close()
        
        os.system(f'rm autonomous-time-309221/cloned_packages/{name}')

        t = open('local_package_directory.txt', 'w')
        for line in lines_to_write:
            t.write(line)
        t.close()

    if query_response == 1:
        return "Package is deleted" +' 200'
    if query_response == 0:
        return "Package does not exist"+ '404'
    return


@app.route('/package/{id}', methods=['GET', 'DELETE', 'PUT'])
def functions_by_ID():
    if request.method == 'GET':
        counter = -1
    # http://34.121.45.140:8001/package/id/%7Bid%7D?id=1
        ident = request.args.get('id')
        #bucket = storage_client.bucket('autonomous-time-309221.appspot.com')
        # blob name your_bucket_name/path_in_gcs
        # blob = bucket.blob('api_calls')
        # listBlobs()
        print(str(ident))
        with open('local_package_directory.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                line_array = line.split(' ')
                counter += 1
                if str(ident) == line_array[0]:
                    with open('local_package_directory_json.txt', 'r') as json_file:
                        lines_json = json_file.readlines()
                        requested_line = lines_json[counter]
                        requested_line = requested_line.replace("\'", "\"")
                        print(requested_line)
                        #requested_line_dict = dict(requested_line)
                        json_object = json.loads(requested_line)
                        return json.dumps(json_object, indent=1) + '200'
        return str(404) +  " Package does not exist"

    if request.method == 'DELETE':
        ident = request.args.get('id')
        query_response = 0
        lines_to_write = []
        lines_to_write_json = []
        name = ""
        counter = 0
        index = 0
        # blob name your_bucket_name/path_in_gcs
        f = open('local_package_directory.txt', 'r')
        f_json_readptr = open('local_package_directory.txt', 'r')
        f_json_writeptr = open('local_package_directory.txt', 'w')
        lines = f.readlines()
        for line in lines:
            if line[0] == ident:
                query_response = 1
                name = line[2:]
                index = counter
            else:
                lines_to_write.append(line)
            counter += 1
        f.close()
        if query_response == 0 or name == "":
            return "Package does not exist" + " 404"
        os.system(f"rm -rf autonomous-time-309221.appspot.com/cloned_packages/{name}")
        with open('local_package_directory.txt', 'w') as file:
            for line in lines_to_write:
                file.write(line)
        counter = 0
        lines_json = f_json_readptr.readlines()
        for i in range(0, len(lines_json)):
            if i != index:
                f_json_writeptr.write(lines_json[i])

        return "Package is deleted" +" 200"


    if request.method == "PUT":
        ident = request.args.get('id')
        print(f'ID:  {ident}\n\n') 
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

            return "Version is updated" + " 200"

@app.route('/package/{id}/rate', methods=['GET'])
def rate_package():
    ident = request.args.get('id')
    score = -1
    # query backend
    # add package to database
    return rate()


@app.route('/reset', methods=['DELETE', 'GET'])
def reset():
    storage_client = storage.Client()
    bucket = storage_client.bucket('autonomous-time-309221.appspot.com')
    # blob name your_bucket_name/path_in_gcs
    pack_dir = open('local_package_directory.txt', 'w')
    pack_dir.truncate()
    pack_dir.close()
    pack_dir_json = open('local_package_directory.txt', 'w')
    pack_dir_json.truncate()
    pack_dir_json.close()
    os.system(f'rm -rf autonomous-time-309221.appspot.com/cloned_packages')
    # /package/byName/%7Bname%7D?name=cloudinary_npm
    return "Registry is reset"+ "200"


@app.route('/packages', methods=['POST', 'GET'])
def get_ID_packages():
    offset = request.args.get('offset')
    packages = []
    pack_string = ""
    if offset is None:
        # print first page of entries
        f = open('local_package_directory.txt')
        # blob name your_bucket_name/path_in_gcs
        lines = f.readlines()
        for line in range(0, min((len(lines)),20)):
            pack_string += lines[line] + "\n"
        return pack_string + '200'
    elif offset is not None:
        # print offset num entries
        if offset > len(lines):
            return "Too many packages returned.", 413
        return pack_string + '200'

    return "unexpected error" + '413'

@app.route('/getPackage')
def queryPackageDir():
    iD = request.args.get('id')
    return ('', 204)

# add url to rate to url_cache.txt
@app.route("/submit")
def submit():
    with open('url_cache.txt', 'a') as f:
        open("url_cache.txt", "w").close()
        url = request.args.get('url')
        if url is not None:
            print("URL:    " + url)
        else:
            url = request.args.get('Content')
        f.write(url)
    return ('', 204)


# flask api call for running rating functionality


def listBlobs():
    client = storage.Client()
    for blob in client.list_blobs('autonomous-time-309221.appspot.com', prefix='autonomous-time-309221.appspot.com/api_calls'):
        print("\n\n"+str(blob)+"\n\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("begin test")
    # os.environ["GITHUB_TOKEN"] = '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'
    # app.config['GITHUB_TOKEN'] =  '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'
    app.run(debug=True, host='10.128.0.2', use_reloader=False, port=8001)
    # host='10.128.0.2',
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
