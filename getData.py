import io
import os.path
import requests

DATA_FOLDER = './data/BOE/'
IDS_FOLDER = './data/ids/'

# Returns a dictionary where keys are dates and values are arrays of ids
def getIds(filename):
    with io.open(IDS_FOLDER + filename , 'r') as file:
        lines = file.readlines()

    idsDictionary = {}
    for line in lines:
        line = line.rstrip()
        date, *ids = line.split(',')
        idsDictionary[date] = ids

    return idsDictionary

def getData(id):
    page_url = 'https://boe.es/diario_boe/txt.php?id=' + id

    if (os.path.isfile(DATA_FOLDER + id)):
        # print('Reading data from storage...')
        with io.open(DATA_FOLDER + id, 'r', encoding='utf8') as file:
            return file.read()

    page = requests.get(page_url)
    # print('Getting data from web...', page.status_code)
    if(page.status_code == 200):
        with io.open(DATA_FOLDER + id, 'w+', encoding='utf8') as file:
            file.write(page.text)
    else:
        raise FileNotFoundError
    return page.text

def main():
    getIds('jan2020.csv')
    # id = 'BOE-A-2019-1'
    # getData(id)

if __name__ == '__main__':
    main()
