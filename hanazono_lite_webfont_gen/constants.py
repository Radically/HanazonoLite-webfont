LOCALES = {
    "g": {"tla": "ZHS", "suffix": "SC"},
    "t": {"tla": "ZHT", "suffix": "TC"},
    "h": {"tla": "ZHH", "suffix": "HK"},
    "j": {"tla": "JAN", "suffix": "JP"},
    "k": {"tla": "KOR", "suffix": "KR"},
    "v": {"tla": "VIT", "suffix": "VN"},
    "test": {"tla": "TEST", "suffix": "Test"},
}

_PACKAGE_JSON_TEMPLATE = """{{
  "name": "{Name}",
  "version": "0.0.1",
  "description": "{Description}",
  "keywords": [
    "font",
    "serif",
    "type",
    "face",
    "mincho",
    "songti",
    "hanazono",
    "hanamin",
    "明朝体",
    "宋体",
    "明朝體",
    "宋體",
    "web",
    "split",
    "subset",
    "woff2",
    "cjk",
    "chinese",
    "japanese",
    "korean",
    "hanzi",
    "kanji",
    "hanja",
    "unicode"
  ],
  "main": "{MinifiedName}.min.css",
  "repository": {{
    "type": "git",
    "url": "git+https://github.com/HanazonoLite-webfont.git"
  }},
  "author": {{
    "name": "Bryan Kok",
    "email": "bryan.wyern1@gmail.com"
  }},
  "license": "OFL-1.1",
  "bugs": {{
    "url": "https://github.com/HanazonoLite-webfont/issues"
  }},
  "homepage": "https://github.com/HanazonoLite-webfont#readme"
}}
"""


def PACKAGE_JSON_TEMPLATE(Name, Description, MinifiedName):
    return _PACKAGE_JSON_TEMPLATE.format(
        Name=Name, Description=Description, MinifiedName=MinifiedName
    )
