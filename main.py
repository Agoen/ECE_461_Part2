#!/usr/bin/ python3

import sys
import os
import time


def license_name(file_name):
    # read the file
    urls = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            urls.append(line.strip())

    # get the license name
    import requests

    if  os.environ.get("GITHUB_TOKEN") == None:
        print("Could not find GITHUB_TOKEN")
        sys.exit(1)


    headers = {
        "Authorization": "Bearer " + os.environ.get("GITHUB_TOKEN")
    }
    license_name =  ""
    open('src/license.txt','w').close()
    for url in urls:
        if "github.com" in url:
            # get data from api.github.com/repo/ using request
            owner = url.split("/")[3]
            repo = url.split("/")[4]

            # get the license name
            # use environment variable to get the token from the user GITHUB_TOKEN and use that token to make the request
            request_url = "https://api.github.com/repos/" + owner + "/" + repo
            response = requests.get(request_url, headers=headers)
            data = response.json()
            if ("license" not in data.keys()):
                license_name = "None"
            else:
                if (data['license'] == None):
                    license_name = "None"
                else:
                    # print(data)
                    license_name = data["license"]["name"]
            os.sys
        elif "npmjs.com" in url:
            repo = url.split("/")[4]
            request_url = "https://replicate.npmjs.com/" + repo
            response = requests.get(request_url)
            # Extract Data from the URL
            data = response.json()
            npmjs_urls = data['repository']['url']
            npmjs_urls = npmjs_urls.split('//')
            # This to remove "@" symbol from the
            npmjs_urls = npmjs_urls[1].split('@')
            if len(npmjs_urls) > 1:
                owner = npmjs_urls[1].split('/')[0]
            else:
                owner = npmjs_urls[0].split('/')[1]
            if (len(npmjs_urls) > 1):
                npmjs_urls = npmjs_urls[1]
            if (type(npmjs_urls) == list):
                npmjs_urls = npmjs_urls[0]
            npmjs_urls = npmjs_urls.replace('.git', '')
            request_url = "https://api.github.com/repos/" + owner + "/" + repo
            response = requests.get(request_url, headers=headers)
            data = response.json()
            if ("license" not in data.keys()):
                license_name = "None"
            else:
                if (data['license'] == "None"):
                    license_name = "None"
                else:
                    license_name = data["license"]["name"]

            # with open('src/license.txt', 'a+') as f:
            #     f.write(license_name)
            #     f.write('\n')
        else:
            print(f"Invalid URL:")
            print(url)
            sys.exit(1)           

        with open('src/license.txt', 'a+') as f:
            f.write(license_name)
            f.write('\n')
        # print(license_name)


def ramp_Up():
    # Clone the repository
    import git
    if (os.path.exists("Useless")):
        os.system("rm -rf Useless")

    os.system("mkdir Useless")
    repo = git.Repo.clone_from(
        "https://github.com/aaradhyajajoo/ECE_461.git", "./Useless")
    repo.remote().pull()

    i = 0
    for commit in repo.iter_commits():  # iter_commits starts from the latest commit
        first_commit = commit
        i += 1

    current_commit = repo.commit()

    start_time = int(first_commit.committed_datetime.timestamp())
    end_time = int(current_commit.committed_datetime.timestamp())

    # Calculate the ramp-up time
    ramp_up_time = end_time - start_time
    total_time = time.time() - start_time
    normalized_ramp_up_time = ramp_up_time / total_time

    with open('src/ramp_up.txt', 'w') as f:
        f.write(str(round(normalized_ramp_up_time, 2)))

    # os.system("rm -rf Useless/.git/objects/pack/")
    # os.system("rm -rf Useless")

# install function


def install():
    os.system("npm --silent --no-progress install")
    os.system("npm --silent --no-progress install typescript")
    os.system("npm --silent --no-progress install ts-node")
    os.system("npm --silent --no-progress install ts-node-dev")
    os.system("npm --silent --no-progress install --save-dev jest")
    os.system("pip install -q -r requirements.txt > /dev/null 2>&1")
    # os.system("ts-node src/install.ts > /dev/null 2>&1")
    os.system("tsc src/install.ts")
    os.system("node src/install.js")
    sys.exit(0)


def main(args, *kwargs):

    # no arguments provided
    if (len(args) == 0):
        print("No arguments provided")
        sys.exit("1")

    # check if the first argument is install or test
    if (args[0].strip() == "install"):
        install()
    elif(args[0].strip() == "build"):
        sys.exit(0)

    elif (args[0].strip() == "test"):

        # for non existant file test
        os.system('./run file_DNE > DNE_OUTPUT')

        # for bad url test
        os.system('echo "youtube.com" > invalid_file')
        os.system('./run invalid_file > OUTPUT')
        os.system('./run sample_url_file.txt > OUTPUT2')
        # for duplicate test
        os.system('cat sample_url_file.txt > CONC')
        os.system('cat sample_url_file.txt >> CONC')
        os.system('./run sample_url_file.txt > OUTPUT3')

        time.sleep(10)

        # runs unit test
        os.system("python3 -m pytest run_test.py --tb=no --cov > PYTEST_RESULTS")
        with open('PYTEST_RESULTS', 'r') as file:
            test_string = file.read().replace('\n', '')

        import regex as re

        # interprets results of unit tests
        results = re.search(r"(\d+) failed", test_string)
        num_fail = 0 if results == None else int(results.group(1))
        results = re.search(r"(\d+) passed", test_string)
        num_pass = 0 if results == None else int(results.group(1))
        print(f"Total: {num_fail + num_pass}")
        print(f"Passed: {num_pass}")
        results = re.findall(r"\d+%", test_string)
        print(f"Coverage: {results[-1]}")
        print(
            f'{num_pass}/{num_fail + num_pass} test cases passed. {results[-1]} line coverage achieved.')
        
        os.system('rm OUTPUT')
        os.system('rm OUTPUT2')
        os.system('rm OUTPUT3')
        os.system('rm CONC')
        os.system('rm DNE_OUTPUT')
        sys.exit(0)

    # default test: check if the files exist
    else:
        check_files_exists(args, *kwargs)
        ramp_Up()
        license_name(args[0].strip())
        # os.system(f"ts-node src/graph_api_call.ts {args[0]}")
        os.system(f"tsc src/graph_api_call.ts")
        os.system(f"node src/graph_api_call.js {args[0]}")

        if (not os.path.exists('results.txt')):
            sys.exit(1)

        # Printing Ordered List of URLs
        with open('results.txt', 'r') as file:
            results = eval(file.read())
            sorted_results = dict(
                sorted(results.items(), key=lambda item: float(item[0]), reverse=True))
            for key, value in sorted_results.items():
                repo_URL = value[0]
                net_score = key
                ramp_upTime = value[1]
                correctness = value[2]
                bus_factor = value[3]
                responsiveness = value[4]
                license_compatibility = value[5]
                print("{\"URL\":\"" + repo_URL + "\", \"NET_SCORE\":" + str(net_score) + ", \"RAMP_UP_SCORE\":" + str(ramp_upTime) + ", \"CORRECTNESS_SCORE\":" + str(correctness) +
                      ", \"BUS_FACTOR_SCORE\":" + str(bus_factor) + ", \"RESPONSIVE_MAINTAINER_SCORE\":" + str(responsiveness) + ", \"LICENSE_SCORE\":" + str(license_compatibility) + "}")

        os.system('rm results.txt')
        sys.exit(0)

# check if the files with the input path exist


def check_files_exists(args):

    # no files provided
    if (len(args) == 0):
        sys.exit("No files provided")

    # check if the files exist
    for arg in args:
        arg = arg.strip()
        if not os.path.exists(arg):
            print(f"File {arg} does not exist")
            sys.exit(1)
        else:
            continue


if __name__ == "__main__":
    main(sys.argv[1:])