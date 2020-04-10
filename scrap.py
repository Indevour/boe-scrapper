from bs4 import BeautifulSoup
from getData import getData, getIds
from dataset import Dataset
import re

# Output:
# If found CPVs, returns array of CPVs
# Otherwise, returns None
def extractCPVsFromSoup(soup):
    cpv_label = soup.find(text=re.compile('CPV')) # 5. Códigos CPV:
    if (cpv_label is not None):
        cpv_label_dt_tag = cpv_label.parent # <dt>5. Códigos CPV:</dt>
        cpv_dd_tag = cpv_label_dt_tag.findNext('dd') # <dd>72000000 (Servicios TI: consultoría, desarrollo de software, Internet y apoyo).</dd>
        cpv_text = cpv_dd_tag.contents[0] # 72000000 (Servicios TI: consultoría, desarrollo de software, Internet y apoyo).
        cpvs = [int(s) for s in cpv_text.split() if s.isdigit()]
        print('Found cpvs:', cpvs)
    else:
        print('Failed to find cpvs')
        cpvs = None
    return cpvs

def containsITCPV(cpvs):
    contains_it_cpv = False
    for cpv in cpvs:
        if (cpv >= 72000000 and cpv < 73000000):
            contains_it_cpv = True
            break

    # if(contains_it_cpv):
    #     print('This document contains an IT CPV')
    # else:
    #     print('This document does not contain an IT CPV')

    return contains_it_cpv

def main():
    # ids = [
    #     'BOE-A-2019-1',
    #     'BOE-B-2019-1',
    #     'BOE-B-2019-34786'
    # ]
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
            soup = BeautifulSoup(data, 'html.parser')
            cpvs = extractCPVsFromSoup(soup)

            if (cpvs is not None):
                if(len(cpvs) == 0):
                    counts['cpvs_not_found'] += 1

                is_it = containsITCPV(cpvs)

                if(is_it):
                    print('Adding document to dataset...')
                    dataset.addEntry({
                        'id': id,
                        'cpv': cpvs[0], # TODO: Revisit
                        'date': date
                    })
                    counts['it'] += 1
                else:
                    counts['not_it'] += 1
            else:
                raise Exception('CPVs NOT FOUND ' + id)

    print('Results:')
    print('IT Licitations Found: ' + str(counts['it']))
    print('Not-IT Licitations Found: ' + str(counts['not_it']))
    print('Licitations with unknown CPVs: ' + str(counts['cpvs_not_found']))

    print('Exporting dataset...')
    dataset.exportAsCSV('./data.csv')

if __name__ == '__main__':
    main()
