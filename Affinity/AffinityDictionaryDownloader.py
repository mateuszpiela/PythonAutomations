import http.client
import os

DICTIONARIES_URL = "https://raw.githubusercontent.com/LibreOffice/dictionaries/master"
AFFINITY_DIC_LOC = {
    "WIN": "C:\\ProgramData\\Affinity\\Common\\2.0\\Dictionaries",
    "MAC": "~/Library/Spelling/"
}


def __get_running_os() -> str:
    from sys import platform

    if platform == "win32":
        return "WIN"
    elif platform == "darwin":
        return "MAC"
    else:
        raise Exception("Unsupported OS")


def __save_dictionary(httpResp: http.client.HTTPResponse, lang: str, fileName: str):
    global AFFINITY_DIC_LOC
    dictionary_loc = AFFINITY_DIC_LOC[__get_running_os()]

    if not os.path.exists(dictionary_loc + os.sep + lang):
        os.makedirs(dictionary_loc + os.sep + lang)

    with open(dictionary_loc + os.sep + lang + os.sep + fileName, 'wb') as file:
        file.write(httpResp.read())


def download_dictionary(lang: str):
    import urllib.request
    global DICTIONARIES_URL

    DICTIONARIES_URL = DICTIONARIES_URL + "/" + lang + "/"
    file_format = ("{lang}.aff", "{lang}.dic", "hyph_{lang}.dic")

    for filenametpl in file_format:
        filename = filenametpl.format(lang=lang)
        print("Downloading file: {filename}".format(filename=filename))
        http_response = urllib.request.urlopen(DICTIONARIES_URL + filename)

        if http_response.status == 200:
            print("Saving file: {filename}".format(filename=filename))
            __save_dictionary(http_response, lang, filename)
        else:
            raise Exception("Cannot download file for this lang :" + lang)


if __name__ == "__main__":
    user_langs = input("What dictionary languages do you want to download (please separate it with commas) ?")

    if "," in user_langs:
        user_langs = user_langs.split(",")

    if user_langs is list:
        for lang in user_langs:
            print("Downloading dictionary for lang {lang}".format(lang=lang))
            try:
                download_dictionary(lang)
            except Exception as e:
                print("Error", e)
    else:
        try:
            download_dictionary(user_langs)
        except Exception as e:
            print("Error", e)
