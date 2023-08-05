#!/usr/bin/env python3

import os
import re
import requests
import argparse
from pathlib import Path
from collections import namedtuple
from mako.template import Template
from pip._vendor.distlib.util import split_filename
try:
    from urllib.parse import urljoin, quote, unquote
except ImportError:
    from urllib import urljoin, quote, unquote

# language=HTML
index_template = Template("""
<html>
<head><title>${project} pip index</title></head>
<body>
<h1>${project}</h1>
    % for package_name, package_url in packages:
        <a href="./${package_url}">${package_name}</a><br/>
    % endfor
</body>
</html>
""")

# language=HTML
package_template = Template("""
<html>
<head><title>${project} pip index - ${package}</title></head>
<body>
<h1>${package}</h1>
    <ul>
    % for name, url in package_files:
        <li><a href="${url}">${name}</a><br/></li>
    % endfor
    </ul>
</body>
</html>
""")


def main():
    parser = argparse.ArgumentParser(description='Generate python repo index files for all tags in project')
    parser.add_argument('--server', default=None, help='url of gitlab server or $CI_PROJECT_URL')
    parser.add_argument('--project_id', default=None, help='Unique id of project, available in '
                                                           'Project Settings/General or $CI_PROJECT_ID')
    parser.add_argument('--private_token', help='login token if using a private repo')
    parser.add_argument('--pre', default=None, help='file glob for local artifacts to include as pre-release wheels')
    parser.add_argument('destination', help='folder to generate html files into')

    args = parser.parse_args()

    headers = None
    if args.private_token:
        headers = {'PRIVATE-TOKEN': args.private_token}

    server = args.server or os.environ['CI_PROJECT_URL']
    if not server:
        print("Must provide --server if not running from CI")
        exit(1)

    project_id = args.project_id or os.environ['CI_PROJECT_ID']
    if not project_id:
        print("Must provide --project_id if not running from CI")
        exit(1)
    project_id = quote(project_id, safe='')

    api_url = urljoin(server, "/api/v4/projects/%s/" % project_id)

    details = requests.get(api_url, headers=headers).json()
    project_url = details['web_url']

    print("Processing tags for %s" % project_url)

    if not server.endswith('/'):
        server += '/'

    if not os.path.exists(args.destination):
        os.makedirs(args.destination)

    rsp = requests.get(urljoin(api_url, 'repository/tags'), headers=headers)
    tags = rsp.json()
    released_file = namedtuple('released_file', ('name', 'url'))
    released_files = {}
    for tag in tags:
        print("Version: %s" % tag['name'])
        try:
            release = tag['release']
            description = re.findall(r'\[(.*?)\]\((.*)\)', release['description'])
            for name, relurl in description:
                pkg = split_filename(name)[0].replace('_', '-')
                if pkg not in released_files:
                    released_files[pkg] = []
                f = released_file(name=name, url=''.join((project_url, relurl)))
                print("  - %s" % f.name)
                released_files[pkg].append(f)
        except (KeyError, TypeError):
            print("  No released files")

    if args.pre:
        print("Pre-release:")
        for f in Path('.').glob(args.pre.strip("'").strip('"')):
            relurl = "../" + quote(str(f.name).replace("\\", "/"))
            pkg = split_filename(f.name)[0].replace('_', '-')
            if pkg not in released_files:
                released_files[pkg] = []
            f = released_file(name=f.name, url=relurl)
            print("  - %s" % f.name)
            released_files[pkg].append(f)

    with open(os.path.join(args.destination, 'index.html'), 'w') as indexfile:
        packages = [(p, p) for p in released_files.keys()]
        packages.extend([(p.replace('-', '_'), p) for p in released_files.keys() if '-' in p])
        packages.sort()
        index_page = index_template.render(project=project_url, packages=packages)
        indexfile.write(index_page)

    for package, package_files in released_files.items():
        packagedir = os.path.join(args.destination, package)
        if not os.path.exists(packagedir):
            os.makedirs(packagedir)
        with open(os.path.join(packagedir, 'index.html'), 'w') as packagefile:
            package_page = package_template.render(project=project_url, package=package, package_files=package_files)
            packagefile.write(package_page)
    print('\nCreated html files in %s' % args.destination)


if __name__ == '__main__':
    main()
