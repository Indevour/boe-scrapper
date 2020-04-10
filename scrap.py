from bs4 import BeautifulSoup
from getData import getData, getIds
from dataset import Dataset
import re

# Output:
# If found CPVs, returns array of CPVs
# Otherwise, returns None
# TEST: Finds 60 IT CPVs in Jan 2020
def extractCPVsFromSoup(soup):
    cpv_labels = soup.find_all(text=re.compile('CPV')) # 5. Códigos CPV:

    cpvs = []
    for cpv_label in cpv_labels:
        if (cpv_label is not None):
            cpv_label_dt_tag = cpv_label.parent # <dt>5. Códigos CPV:</dt>
            cpv_dd_tag = cpv_label_dt_tag.findNext('dd') # <dd>72000000 (Servicios TI: consultoría, desarrollo de software, Internet y apoyo).</dd>
            cpv_text = cpv_dd_tag.contents[0] # 72000000 (Servicios TI: consultoría, desarrollo de software, Internet y apoyo).
            cpvs += [int(s) for s in cpv_text.split() if s.isdigit()]

    if (len(cpvs) == 0):
        return None
    cpvs = list(dict.fromkeys(cpvs))
    return cpvs

# TEST: Finds 62 IT CPVs in Jan 2020
def extractCPVsFromData(data):
    cpvs = [int(s) for s in re.findall(r'\d+', data) if len(s) == 8]
    return cpvs

def extractInvestmentsFromData(data):
    # costs = [(s.replace('.', '')).replace(',', '.') for s in re.findall(r'\d+,\d\d euros', data)]
    costs = [(s.replace('.', '')).replace(',', '.') for s in re.findall(r'(?:\.*\d+)*,\d\d euros', data)]
    print(costs)
    return costs

def containsITCPV(cpvs):
    contains_it_cpv = False
    for cpv in cpvs:
        if (cpv >= 72000000 and cpv < 73000000):
            contains_it_cpv = True
            break
    return contains_it_cpv

def main():
    dataset = Dataset()
    counts = {
        'cpvs_not_found': 0,
        'it': 0,
        'not_it': 0
    }


    idsDictionary = getIds('jan2020.csv')
    for date in idsDictionary:
        ids = idsDictionary[date]

        for id in ids:
            data = getData(id)
            # soup = BeautifulSoup(data, 'html.parser')
            # cpvs = extractCPVsFromSoup(soup)
            cpvs = extractCPVsFromData(data)
            # print('Found CPVs:', cpvs)

            if (cpvs is not None):
                if(containsITCPV(cpvs)):
                    investments = extractInvestmentsFromData(data)
                    print('Adding document to dataset...')
                    dataset.addEntry({
                        'id': id,
                        'cpv': cpvs,
                        'date': date,
                        'investments': investments
                    })
                    counts['it'] += 1
                else:
                    counts['not_it'] += 1
            else:
                raise Exception('CPVs NOT FOUND ' + id)
                counts['cpvs_not_found'] += 1

    print('Results:')
    print('IT Licitations Found: ' + str(counts['it']))
    print('Not-IT Licitations Found: ' + str(counts['not_it']))
    print('Licitations with unknown CPVs: ' + str(counts['cpvs_not_found']))

    print('Exporting dataset...')
    dataset.exportAsCSV('./data.csv')

if __name__ == '__main__':
    main()
