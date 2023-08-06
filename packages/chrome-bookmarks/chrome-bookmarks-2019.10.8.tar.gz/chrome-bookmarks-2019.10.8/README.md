<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/chrome-bookmarks.svg?longCache=True)](https://pypi.org/project/chrome-bookmarks/)

#### Installation
```bash
$ [sudo] pip install chrome-bookmarks
```

#### Features
OS|path
-|-
`Linux`|`~/.config/google-chrome/Default/Bookmarks`
`macOS`|`~/Library/Application Support/Google/Chrome/Default/Bookmarks`
`Windows`|`~\AppData\Local\Google\Chrome\User Data\Default\Bookmarks`

#### Classes
class|`__doc__`
-|-
`chrome_bookmarks.Bookmarks` |Bookmarks class. attrs: `path`. properties: `folders`, `urls`
`chrome_bookmarks.Item` |Item class, dict based. properties: `id`, `name`, `type`, `url`, `folders`, `urls`

#### Examples
```python
import chrome_bookmarks

for folder in chrome_bookmarks.folders:
    print(folder.name)
    print(folder.folders)
```

```python
for url in chrome_bookmarks.urls:
    print(url.url, url.name)
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>