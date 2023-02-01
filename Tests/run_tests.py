from urllib.request import Request,urlopen
from subprocess import Popen
from pathlib import Path
from time import sleep
from test_login import login_tests

PROJECT_DIR = str(Path(__file__).parent.parent.resolve())

def main():
    website_url = "https://localhost:5001"
    download_chromedriver()
    Popen(f"Deployment/init_website.sh -d -u {website_url}",
                    cwd=PROJECT_DIR,
                    shell=True).communicate()
    try:
        host_webserver = Popen(f"Deployment/host_website.sh -d",
                        cwd=PROJECT_DIR,
                        shell=True)
        sleep(5)
        login_tests(website_url)
        host_webserver.kill()
    except Exception as e:
        host_webserver.kill()
        raise e

def download_chromedriver():
    response = _make_http_request("https://sites.google.com/chromium.org/driver/downloads")
    drivers = {}
    if response["successful"]:
        html = response["data"].replace(">",">\n")
        for line in html.split("\n"):
            if "chromedriver.storage.googleapis.com/index.html?path=" in line:
                url = line.split("href=\"")[1].split("\"")[0]
                version = url.split("=")[-1].split("/")[0]
                drivers[version] = url
    if not drivers:
        raise Exception
    latest_driver = latest_version(list(drivers.keys()))
    Popen(f"curl {drivers[latest_driver]} >> chromedriver",
          cwd=PROJECT_DIR+"/Tests",
          shell=True).communicate()

def latest_version(versions):
    if not versions:
        raise Exception
    while len(versions) > 1:
        version_a = [int(x) for x in versions[0].split(".")]
        version_b = [int(x) for x in versions[1].split(".")]
        popped = False
        for i in range(min(len(version_a),len(version_b))):
            if version_a[i] > version_b[i]:
                versions.pop(1)
                popped = True
                break
            elif version_a[i] < version_b[i]:
                versions.pop(0)
                popped = True
                break
            else:
                continue
        if not popped:
            versions.pop(0)
    return versions[0]

def _make_http_request(url):
    try:
        request = Request(
            url,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        response_obj = urlopen(request,timeout=10)
        response = response_obj.read().decode("utf-8")
        successful = True
    except Exception as e:
        response = e
        successful = False
    return {"successful":successful,"data":response}

main()
