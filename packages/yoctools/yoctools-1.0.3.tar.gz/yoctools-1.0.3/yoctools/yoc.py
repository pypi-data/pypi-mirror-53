#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys

try:
    from urlparse import urlparse
    import urllib
    import httplib as http
except:
    from urllib.parse import urlparse
    import urllib.request
    import http.client as http

import hashlib
import json
import time

import git
import zipfile

from yoctools.toolchain import load_package

class YoC:
    def __init__(self, path=''):
        self.path = path
        self.occ = OCC('occ.t-head.cn')
        # self.occ = OCC('cid.c-sky.com')
        self.occ.yocComponentList('614193542956318720')
        self.components = []
        try:
            files = os.listdir(os.path.join(self.path, 'components'))
            for component_name in files:
                comp_path = os.path.join(self.path, 'components', component_name)
                if os.path.isdir(comp_path):
                    self.add_component(component_name)
        except:
            pass


    def add_component(self, name):
        # print("add component " + name)
        for c in self.components:
            if c.name == name:
                return
        pack = self.occ.get(name)
        if pack:
            for dep in pack.depends:
                self.add_component(dep['name'])
            if pack.type != 'solution':
                self.components.append(pack)

    def update(self):
        for pack in self.components:
            pack.download()
        genScons(self.components, self.path)
        getSConstruct(self.path)

class Component:
    def __init__(self, js):
        self.name = ''
        self.depends = []
        self.description = ''
        self.versions = ''
        self.license = ''
        self.historyVersion = {}
        self.updated = ''
        self.repo_url = ''
        self.repo = None
        self.path = ''
        self.type = 'common'

        if js:
            self.parser(js)
            self.js = js


    def parser(self, js):
        self.name = js['name']
        self.depends = js['depends']
        self.description = js['description']
        self.versions = js['versions']
        self.license = js['license']
        self.repo_url = js['aboutURL']

        self.updated = js['updated']

        for ver in js['historyVersion']:
            self.historyVersion[ver['version']] = ver['url']

        if self.name not in ['mbedtls', 'bt', 'ezxml', 'faad', 'mad', 'srtp']:
            self.depends = [
                {"name": "mbedtls", "version": "master"},
                {"name": "bt",      "version": "master"},
                {"name": "ezxml",   "version": "master"},
                {"name": "faad",    "version": "master"},
                {"name": "mad",     "version": "master"},
                {"name": "srtp",    "version": "master"}
            ]

        self.path = 'components/' + self.name
        if self.name == "helloworld":
            self.type = "solution"
            self.path = ''


    def download(self, version=None):
        if version == None:
            version = self.versions
        if self.repo_url:
            if (not os.path.exists(self.path)) or (not os.path.isdir(os.path.join(self.path, '.git'))):
                print(self.repo_url)
                print('git clone %s (%s)...' % (self.name, version))
                repo = git.Repo.init(self.path)
                origin = repo.create_remote(name='origin', url=self.repo_url)
                origin.fetch()

                repo.create_head(version, origin.refs.master)  # create local branch "master" from remote "master"
                repo.heads.master.set_tracking_branch(origin.refs.master)  # set local "master" to track remote "master
                repo.heads.master.checkout()  # checkout local "master" to working tree
            # else:
            #     print('git pull %s (%s)...' % (self.name, version))
            #     repo = git.Repo(self.path)
            #     remote = repo.remote()
            #     remote.pull()
        else:
            zip_url = self.historyVersion[version]
            filename = http_get(zip_url, '.cache')
            zipf = zipfile.ZipFile(filename)
            if self.path != '.':
                zipf.extractall('components/')
            else:
                zipf.extractall('.')

    def zip(self):
        path = 'components/' + self.name
        zipName = '.cache/' + self.name + "-" + self.versions + ".zip"
        zip_path(path, zipName)

        return zipName

    def show(self):
        if os.path.isdir(self.path):
            status = '*'
        else:
            status = ' '

        s1 = self.name + ' (' + self.versions + ')'
        size = len(s1)

        print("%s %s %s - %s" % (status, s1, ' ' * (40 - size), self.description[:60]))
        size = len(self.description)
        begin = 60
        while True:
            if begin < size:
                print(' ' * 46 + self.description[begin:begin+60])
                begin += 60
            else:
                break


class OCC:
    def __init__(self, host=None):
        if host:
            self.host = host
        else:
            self.host = 'occ.t-head.cn'
        self.components = {}

    def get(self, name):
        if name in self.components:
            return self.components[name]

    def download(self, name, version=None):
        if name in self.components:
            pack = self.components[name]
            if pack:
                pack.download(version)

    def showList(self):
        for _, pack in self.components.items():
            pack.show()


    def yocComponentListUpload(self):
        cmd = '/api/resource/cdk/yocComponent/common/upload'
        body = {
             "model": {
                 "name":"CH2201",
                 "version":"version"
                }
        }
        text = json.dumps(body)

        js = self.request(get_url(cmd, text), text)


    def yocGetInfo(self, name):
        cmd = '/api/resource/component/getInfo'
        body = {}
        js = self.request(get_url(cmd, body), body)

    def yocComponentList(self, chipId):
        cmd = '/api/resource/cdk/yocComponentList'
        body = {"name": "jsmn"}
        text = json.dumps(body)

        js = self.request(get_url(cmd, text), text)

        for p in js:
            pack = Component(p)
            self.components[pack.name] = pack

    def request(self, url, body):
        connection = http.HTTPSConnection(self.host)

        connection.request('POST', url, body)
        response = connection.getresponse()
        text = response.read()
        js = json.loads(text)
        # print(js)

        if js['code'] == 0:
            return js['result']['packages']
        else:
            return {}


def MD5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()

def get_url(cmd, body):
    timestamp = time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))
    md5 = MD5(cmd + timestamp + body)

    return '%s?timestamp=%s&sign=%s&chipId=614193542956318720' % (cmd, timestamp, md5)

def http_get(url, path):
    conn = urlparse(url)

    if conn.scheme == "https":
        connection = http.HTTPSConnection(conn.netloc)
    else:
        connection = http.HTTPConnection(conn.netloc)

    connection.request('GET', conn.path)
    response = connection.getresponse()

    filename = os.path.join(path, os.path.basename(conn.path))

    with open(filename, 'wb') as f:
        f.write(response.read())
    return filename


def dfs_get_zip_file(input_path,result):
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path+'/'+file):
            dfs_get_zip_file(input_path+'/'+file,result)
        else:
            result.append(input_path+'/'+file)

def zip_path(input_path, zipName):
    if os.path.isdir(input_path):
        f = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)
        filelists = []
        dfs_get_zip_file(input_path, filelists)
        for file in filelists:
            f.write(file)
        f.close()

def genScons(components, path):
    script = """]

for d in components:
    file_name = os.path.join(d, 'SConscript')
    if os.path.isfile(file_name):
        SConscript(file_name, duplicate=0)
"""

    script_file = os.path.join(path, 'components/SConscript')
    try:
        with open(script_file, "w") as f:
            f.write('#! /bin/env python\n\n')
            f.write('import os\n\n')

            f.write('components = [\n')

            for comp in components:
                f.write('    "' + comp.name + '",\n')
            f.write(script)
    except:
        pass

def getSConstruct(path):
    script_file = os.path.join(path, 'SConstruct')
    with open(script_file, "w") as f:
        f.write(
"""#! /bin/env python

import yoctools.toolchain as toolchain

defconfig = toolchain.DefaultConfig()

Export('defconfig')

paths = [
    'components',
]

defconfig.build_package(paths)
""")

# cmd:
#   install
#   uninstall
#   list
#   help
#   search

def usage():
    print("Usage:")
    print("  yoc <command> [options]\n")
    print("Commands:")
    print("  install                     Install component.")
    print("  uninstall                   Uninstall component.")
    print("  list                        List all packages")
    print("")

    print("General Options:")
    print("  -h, --help                  Show help.")

def main():
    argc = len(sys.argv)
    if argc < 2:
        usage()
        exit(0)


    yoc = YoC()

    if sys.argv[1] == 'list':
        yoc.occ.showList()
    elif sys.argv[1] in ['install', 'download']:
        if argc >= 3:
            yoc.add_component(sys.argv[2])
            yoc.update()
            print("%s download Success!" % sys.argv[2])


if __name__ == "__main__":
    main()