# modules/run.py
from modules.decompiler.apktool import decompileApkUsingApktool
from modules.decompiler.jadx import decompileApkUsingJadx
from modules.downloader.playstore import playstore_download
from modules.parser.deeplink import parseDeeplinks
from modules.parser.smali import parseSmali
from modules.filter.deeplink import filterDeeplinks
from modules.filter.param import filterParams
from modules.tester.test import testDeeplink
import os
import dotenv

dotenv.load_dotenv()
# REDIRECT_URL = "https://example.com"
REDIRECT_URL = os.getenv("REDIRECT_URL")


def run(package_name):
    csv_dir = "./data/csv/"

    try:
        print("Downloading APK...")
        playstore_download(package_name)

        print("Decompiling APK (jadx)...")
        decompileApkUsingJadx(package_name)

        print("Decompiling APK (apktool)...")
        decompileApkUsingApktool(package_name)

        print("Parsing deeplinks...")
        deeplinks = parseDeeplinks(
            package_name,
            csv_dir,
            f"./data/decompiled/{package_name}/resources/AndroidManifest.xml",
            f"./data/decompiled/{package_name}/resources/res/values/strings.xml",
        )
        deeplinks = filterDeeplinks(deeplinks)
        if deeplinks:
            print(deeplinks)
            print("Deeplinks parsed and saved successfully.")
        else:
            print("No deeplinks found or error in parsing.")

        params, addURIs, UriParses, addJsIfs, method = parseSmali(
            f"./data/decompiled/apktool_{package_name}", deeplinks
        )
        params = filterParams(params)
        print("[getQueryParameter] :", params)
        print("[addURI] :", addURIs)
        print("[parse] :", UriParses)
        print("[Javascript Interface] :", method)
        print("[addJavascriptInterface] :", addJsIfs)

        testDeeplink(deeplinks, params, REDIRECT_URL)
    except:
        with open("error.txt", "w") as f:
            f.write(package_name + "\n")
        pass


def multiRun(package_list):
    for package_name in package_list:
        run(package_name)
