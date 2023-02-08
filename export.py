import openpyxl
import pandas as pd
from openpyxl.styles import Font
import math
import json 
import os
from openpyxl.styles import PatternFill

config_file = json.load(open('assets/config.json'))
colors = config_file["colors"]

def save(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename+".xlsx", index=False, header=False)

def colorCode(filename):
    assert os.path.isfile(filename+".xlsx")
    doc = openpyxl.load_workbook(filename+".xlsx")
    spreadsheet = doc.active
    for column in range(1, spreadsheet.max_column+1):
        column_data = []
        for row in range(2, spreadsheet.max_row+1):
            column_data.append(spreadsheet.cell(row=row, column=column).value)
        column_data = sorted(column_data, reverse=True)
        for row in range(2, spreadsheet.max_row+1):
            cell = spreadsheet.cell(row=row, column=column)
            index = math.floor((len(colors)-1)*column_data.index(cell.value)/(len(column_data)-1))
            if column == spreadsheet.max_row:
                index = 91
            color = colors[index]
            cell.fill = PatternFill(fgColor=color, bgColor=color, fill_type='solid')
    doc.save(filename+".xlsx")
