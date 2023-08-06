import os
from openpyxl import load_workbook


"""
# Example Function Run
# Function(dataDictionary, FileName)

# DICTIONARY {"SHEET": {"CELL": VALUE, "CELL": VALUE}}
datadict = {'Sheet1': {'D1': 123.4, 'D2': 567.8},
            'Sheet2': {'D1': 123.4, 'D2': 567.8},
            'Sheet3': {'D1': 123.4, 'D2': 567.8},
            }

# FULL PATH TO FILE
loc = os.getcwd()
fnme = 'MMW_BMP_Spreadsheet_Tool(Skippack).xlsx'
file = os.path.join(loc, fnme)

BMPxlsxWriter.write(datadict, file)

"""


def write(datadict, file):
    loc = os.getcwd()
    wb = load_workbook(file)
    for key, value in datadict.iteritems():
        sheet = wb[key]
        for k, v in value.iteritems():
            sheet[k] = v
    wb.save(filename=os.path.join(loc, file))


def main():
    message = "The Excel Writing Function has one method, write, which takes two parameters: DataDictionary, FileName"
    print(message)


if __name__ == '__main__':
    main()

