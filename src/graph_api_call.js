"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
exports.write_to_log_file = void 0;
var fs = require("fs");
var axios_1 = require("axios");
var exec = require('child_process').exec;
var readline = require('readline');
// Global variables
var license_compatibility;
var bus_factor;
var ramp_upTime;
var responsiveness;
var correctness;
var net_score;
var licenseName;
var issuesCount;
var forksCount;
var watchersCount;
var stargazerCount;
var repo_URL;
var verbosity;
var filename;
var filename = String(process.env.LOG_FILE);
var verbosity = Number(process.env.LOG_LEVEL);
var to_sort = {};
var global_url_count = 0;
var i;
var licenseArray = [];
var count;
//  get the github token from the environment variable
var github_token = process.env.GITHUB_TOKEN;
// function that writes to the log file for verbosity
function write_to_log_file() {
    if (verbosity == 0) {
        return;
    }
    if (verbosity == 1) { //1 means informational messages
        var Console = new console.Console(fs.createWriteStream(filename, { flags: 'a' })); //displays the scores to console
        Console.log("URL: " + repo_URL);
        Console.log("NET_SCORE: " + net_score);
        Console.log("RAMP_UP_SCORE: " + ramp_upTime);
        Console.log("CORRECTNESS_SCORE: " + correctness);
        Console.log("BUS_FACTOR_SCORE: " + bus_factor);
        Console.log("RESPONSIVENESS_SCORE: " + responsiveness);
        Console.log("LICENSE_COMPATIBILITY_SCORE: " + license_compatibility);
        Console.log("\n");
    }
    if (verbosity == 2) { //2 means debug message
        var Console = new console.Console(fs.createWriteStream(filename, { flags: 'a' })); //displa
        Console.log("URL: " + repo_URL);
        Console.log("NET_SCORE: " + net_score);
        Console.log("RAMP_UP_SCORE: " + ramp_upTime);
        Console.log("CORRECTNESS_SCORE: " + correctness);
        Console.log("BUS_FACTOR_SCORE: " + bus_factor);
        Console.log("RESPONSIVENESS_SCORE: " + responsiveness);
        Console.log("LICENSE_COMPATIBILITY_SCORE: " + license_compatibility);
        Console.log("The following are how the individual scores are calculated: " + repo_URL);
        Console.log("Bus Factor = ((issuesCount / (issuesCount + forksCount + watchersCount + stargazerCount)) * license_compatibility)");
        Console.log("Responsiveness = (Math.abs(1 - (1 / issuesCount)))");
        Console.log("Correctness = (Math.abs(1 - (1 / forksCount)))");
        Console.log("Ramp Up Time = (Math.abs(1 - (1 / watchersCount)))");
        Console.log("\n");
        Console.log("\n");
    }
    return 0;
}
exports.write_to_log_file = write_to_log_file;
function ramp_upTime_calc() {
    // read from a file called rampedUp.txt
    var rampedUp = fs.readFileSync('src\/ramp_up.txt', 'utf-8');
    var rampedUp_arr = rampedUp.split(/\r?\n/);
    return rampedUp_arr[0];
}
// Function to request APIs from github GraphQL API
function getData_github(requestUrl, owner, repo, flag) {
    return __awaiter(this, void 0, void 0, function () {
        var query, prev_owner, prev_repo, error_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    query = "\n    query {\n      repository(owner: \"owner123\", name: \"repo1\") {\n        name\n        url\n        description\n        watchers {\n        totalCount\n        }\n        forks{\n          totalCount\n        }\n        issues {\n            totalCount\n        }\n        stargazerCount\n        }\n        }\n      ";
                    prev_owner = "owner123";
                    prev_repo = "repo1";
                    query = query.replace(prev_owner, owner);
                    query = query.replace(prev_repo, repo);
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, (0, axios_1["default"])({
                            url: requestUrl,
                            method: 'post',
                            headers: {
                                Authorization: "Token ".concat(github_token),
                                Accept: 'application/vnd.github+json; application/vnd.github.hellcat-preview+json; application/vnd.github.squirrel-girl-preview+json'
                            },
                            data: {
                                query: query
                            }
                        }).then(function (response) {
                            // get the data from the response
                            if (flag == 0) {
                                repo_URL = response.data.data.repository.url;
                            }
                            else {
                                repo_URL = "https://npmsjs.com/package/" + response.data.data.repository.name;
                            }
                            issuesCount = response.data.data.repository.issues.totalCount; //store the number of issues
                            forksCount = response.data.data.repository.forks.totalCount; //store the number of forks
                            watchersCount = response.data.data.repository.watchers.totalCount; //store the number of watchers
                            stargazerCount = response.data.data.repository.stargazerCount; //store the number of stargazers
                            // call the function to calculate the scores
                            calculate_scores(issuesCount, forksCount, watchersCount, stargazerCount, net_score);
                        })];
                case 2:
                    _a.sent();
                    return [3 /*break*/, 4];
                case 3:
                    error_1 = _a.sent();
                    console.error("There was a problem with the fetch operation with ", requestUrl); //throws an error if a bad URL was inputted 
                    console.error(error_1);
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
// Function to request APIs
function getData_npmjs(requestUrl) {
    return __awaiter(this, void 0, void 0, function () {
        var response, npmjs_urls, owner, repo, request_url;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, axios_1["default"].get(requestUrl)];
                case 1:
                    response = _a.sent();
                    npmjs_urls = response.data['repository']['url'];
                    npmjs_urls = npmjs_urls.split('//');
                    npmjs_urls = npmjs_urls[1].split('@'); //This to remove "@" symbol from the 
                    if (npmjs_urls.length > 1) {
                        npmjs_urls = npmjs_urls[1];
                    }
                    if (typeof npmjs_urls == 'object') {
                        npmjs_urls = npmjs_urls[0];
                    }
                    npmjs_urls = npmjs_urls.replace('.git', '');
                    owner = npmjs_urls.split("/")[1];
                    repo = npmjs_urls.split("/")[2];
                    request_url = "https://api.github.com/graphql";
                    getData_github(request_url, owner, repo, 1); //Get and store the respone from github API
                    return [2 /*return*/];
            }
        });
    });
}
function calculate_scores(issuesCount, forksCount, watchersCount, stargazerCount, net_score) {
    // check what license the repo has
    // console.log("License Name: " + licenseName);
    // calculate license compatibility:
    licenseName = licenseArray[i];
    if (licenseName.includes('MIT')) {
        license_compatibility = 1;
    }
    else if (licenseName.includes('Other')) {
        license_compatibility = 1;
    }
    else {
        license_compatibility = 0;
    }
    // calculate the bus_factor time
    if (license_compatibility == 0) {
        bus_factor = 0;
    }
    else {
        var bus_factor_str = (((issuesCount) / (issuesCount + forksCount + watchersCount + stargazerCount)) * license_compatibility).toFixed(2); // Bus factor Formula
        bus_factor = Number(bus_factor_str);
    }
    // calculate the responsiveness time
    if (watchersCount < issuesCount) {
        responsiveness = (Math.abs(1 - (watchersCount / issuesCount))).toFixed(2); //Responsiveness formula
    }
    else {
        responsiveness = (Math.abs(1 - (issuesCount / watchersCount))).toFixed(2);
    }
    // calculate the ramp_upTime
    ramp_upTime = Number(ramp_upTime_calc()); //Ramp-up formula
    correctness = Number(((Number(responsiveness) + license_compatibility) / 2).toFixed(2));
    // calculate the net_score time
    var net_score = Number(((0.4 * Number(responsiveness) + 0.1 * bus_factor + 0.2 * license_compatibility + 0.1 * ramp_upTime + 0.2 * correctness)).toFixed(2)); //NET score formula
    write(license_compatibility, bus_factor, ramp_upTime, Number(responsiveness), correctness, net_score);
}
function write(license_compatibility, bus_factor, ramp_upTime, responsiveness, correctness, net_score) {
    // write to the console
    write_to_log_file(); // Environment Variable
    i += 1; // Updating counter for urls
    to_sort[net_score] = [repo_URL, ramp_upTime, correctness, bus_factor, responsiveness, license_compatibility];
    // var line_to_print = "{\"URL\":\"" + repo_URL + "\", \"NET_SCORE\":" + net_score + ", \"RAMP_UP_SCORE\":" + ramp_upTime + 
    // ", \"CORRECTNESS_SCORE\":" + correctness + ", \"BUS_FACTOR_SCORE\":" + bus_factor + ", \"RESPONSIVE_MAINTAINER_SCORE\":" 
    // + responsiveness + ", \"LICENSE_SCORE\":" + license_compatibility + "}"
    if (i == global_url_count) {
        // console.log(to_sort)
        var Console = new console.Console(fs.createWriteStream("results.txt", { flags: 'w' }));
        Console.log(to_sort);
    }
    // console.log(line_to_print);
}
// Main function
function main() {
    // get the arguments from the command line
    var args = process.argv;
    // get the filename from the command line
    var filename = args[2];
    filename = filename.replace(/\r/g, '');
    // read the file
    var string_urls = fs.readFileSync(filename, 'utf-8');
    var arr_urls = string_urls.split(/\r?\n/);
    // read license txt file
    var rl = readline.createInterface({
        input: fs.createReadStream('src/license.txt')
    });
    rl.on('line', function (line) {
        licenseArray.push(line);
    });
    // Stack Overflow Citation 
    // https://stackoverflow.com/questions/30016773/javascript-filter-true-booleans
    arr_urls = arr_urls.filter(Boolean);
    i = 0;
    count = 0;
    global_url_count = arr_urls.length;
    arr_urls.forEach(function (url) {
        // get the owner and repo name from the url
        var owner = url.split('/')[3];
        var repo = url.split('/')[4];
        // GitHub URLs 
        if (url.includes('github')) {
            var request_url = "https://api.github.com/graphql";
            getData_github(request_url, owner, repo, 0);
        }
        // NPM URLs
        else if (url.includes('npm')) {
            var request_url = "https://replicate.npmjs.com/" + repo;
            getData_npmjs(request_url);
        }
        // Invalid URL
        else {
            console.log("Invalid URL: ");
            console.log(url);
        }
    });
}
if (process.env.LOG_FILE == null) {
    console.log("Invalid Log File");
    process.exit(1);
}
if (process.env.LOG_LEVEL == null) {
    console.log("Invalid Log Level");
    process.exit(1);
}
main(); // Main 
