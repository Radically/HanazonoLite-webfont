import re
import os
import argparse
import subprocess
import requests
from requests.models import Response

from .constants import *

parser = argparse.ArgumentParser()
parser.add_argument("font_splitter", help="Path to font-splitter binary")
parser.add_argument("locale", help="g, t, h, j, k, or v")
parser.add_argument("cjk", help="1 for CJK, 0 for single language")

rls = None
program_args = None


def get_release() -> Response:
    global rls
    if rls:
        return rls
    rls = requests.get(
        url="https://api.github.com/repos/radically/hanazonolite/releases/latest"
    )
    return rls


def download_otf(locale: str, is_mincho: bool, cjk: bool):
    resp = get_release().json()
    tmp = filter(lambda x: x["content_type"] == "font/otf", resp["assets"])

    search_regex = (
        f"Hana{'Min' if is_mincho else 'Goth'}Lite{'CJK' if cjk else ''}Test{LOCALES[locale]['suffix']}.otf\Z"
        if "TEST_RUN" in os.environ
        else f"Hana{'Min' if is_mincho else 'Goth'}Lite{'CJK' if cjk else ''}([A-D0-9]{{1,2}}){LOCALES[locale]['suffix']}.otf\Z"
    )
    tmp = list(
        filter(
            lambda x: re.search(
                search_regex,
                x["name"],
            ),
            tmp,
        )
    )
    # print(tmp)
    # otfs = map(lambda x: {"name": x["name"], "url": x["browser_download_url"]}, tmp)
    otfs = map(lambda x: x["browser_download_url"], tmp)
    subprocess.run(["wget", "-nc"] + list(otfs))  # for debugging purposes
    return list(map(lambda x: x["name"], tmp))


def remove_downloaded_otf():
    subprocess.Popen("rm *.otf", shell=True)


def generate_woff2(is_mincho: bool):
    font_splitter = program_args.font_splitter
    locale = program_args.locale
    cjk = program_args.cjk == "1"

    # Generate Mincho and Gothic

    dirname = f"{'Mincho' if is_mincho else 'Gothic'}"
    family_name = (
        f"Hanazono {'Mincho' if is_mincho else 'Gothic'} Lite{' CJK' if cjk else ''}"
    )
    combined_css_name = f"Hana{'Min' if is_mincho else 'Goth'}Lite{'CJK' if cjk else ''}{LOCALES[locale]['suffix']}"
    subprocess.run(
        [
            "rm",
            "-rf",
            dirname,
        ]
    )
    subprocess.run(
        [
            "mkdir",
            "-p",
            dirname,
        ]
    )
    tasks = []
    otf_names = download_otf(locale, is_mincho, cjk)

    for name in otf_names:
        tasks.append(
            subprocess.Popen(
                [font_splitter, "-o", dirname, "-n", f"'{family_name}'", name]
            )
        )
    for task in tasks:
        task.wait()

    remove_downloaded_otf()
    task = subprocess.Popen(
        f"cat ./{dirname}/*.css > {dirname}/{combined_css_name}.css", shell=True
    )
    task.wait()
    subprocess.run(
        [
            "cleancss",
            "-o" f"{dirname}/{combined_css_name}.min.css",
            f"{dirname}/{combined_css_name}.css",
        ]
    )
    # generate package.json and tarballs (package.json should obviously be in the tgz)
    f = open(f"{dirname}/package.json", "w")
    description = (
        f"{family_name} {LOCALES[locale]['suffix']} webfont leveraging unicode-range"
    )
    f.write(
        PACKAGE_JSON_TEMPLATE(
            f"{family_name} {LOCALES[locale]['suffix']}".replace(" ", "-").lower(),
            description,
            combined_css_name,
        )
    )
    f.close()

    subprocess.run(["npm", "pack", f"./{dirname}"])


def cli(args=None):
    global program_args
    program_args = parser.parse_args()

    for is_mincho in [True, False]:
        generate_woff2(is_mincho)

    # break
    # finally at the end, commit back to repo (after this script has ended)
