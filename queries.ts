#!/usr/bin/env tsc

async function regex_search(regex: RegExp)
{
    const url = `https://api.github.com/search/repositories?`;
    const response = await fetch(`${url}q={${regex}}+in:readme`);
    const json = await response.json();
    return json;
}
    