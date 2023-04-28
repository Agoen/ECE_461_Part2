#!/usr/bin/env tsc
import fetch from 'node-fetch';

interface Package
{
    name: string;
    version: string;
    readme: string;
}

async function fetch_pkgdir(): Promise<Package[]>
{
    const url = 'https://registry.npmjs.com/-/v1/search?text=';
    const pageSize = 250;
    let page = 0;
    let packages: Package[] = [];
    while(true)
    {
        const response = await fetch(`${url}&size=${pageSize}&from=${page * pageSize}`);
        const json = await response.json();
        if (json.objects.length === 0) 
        {
            break;
        }
    }
    return packages;
}

async function regex_search(regex: RegExp): Promise<Package[]>
{
    const url = 'https://registry.npmjs.com/-/v1/search?text=';
    const pageSize = 250;
    let page = 0;
    let packages: Package[] = [];
    while (true) {
        const response = await fetch(`${url}&size=${pageSize}&from=${page * pageSize}`);
        const json = await response.json();
        if (json.objects.length === 0) {
            break;
        }
        const pagePackages: Package[] = await Promise.all(json.objects.map(async (obj: any) => {
            const name = obj.package.name;
            const version = obj.package.version;
            const readmeResponse = await fetch(`https://registry.npmjs.com/${name}/${version}`);
            const readmeJson = await readmeResponse.json();
            const readme = readmeJson.readme;
            return { name, version, readme };
        }));
        packages = [...packages, ...pagePackages.filter(pkg => pkg.name.match(regex) || (pkg.readme && pkg.readme.match(regex)))];
        page++;
    }

    return packages;
}
    