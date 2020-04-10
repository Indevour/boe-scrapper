import pandas as pd

DEFAULT_COLUMNS = ['id', 'date', 'cpv']

class Dataset:
    def __init__(self, columns=DEFAULT_COLUMNS):
        self.data = []
        self.columns=columns

    def addEntry(self, newEntry):
        self.data.append(newEntry)

    def exportAsCSV(self, filepath):
        df = pd.DataFrame(self.data, columns=self.columns)
        df.to_csv(filepath, index=False)

def main():
    dataset = Dataset()
    dataset.addEntry({
    'id': '1234',
    'cpv': '72000000'
    })
    dataset.exportAsCSV('./data.csv')

if __name__ == '__main__':
    main()
