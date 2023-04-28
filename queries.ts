#!/usr/bin/env tsc

async function regex_search(regex: RegExp)
{
    const url = `https://api.github.com/search/repositories?`;
    const response = await fetch(`${url}q={${regex}}+in:readme`);
    const json = await response.json();
    //const pkgs = Array.of(json);
    return json;
}

async function main() {
    const regexPattern = new RegExp('secular', 'i');
    const pkgs = await regex_search(regexPattern);
}

main();
    