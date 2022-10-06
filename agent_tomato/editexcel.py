from openpyxl import Workbook

book = Workbook()
sheet = book.active

sheet['A1'] = 1
sheet.cell(row=2, column=2).value = 2

book.save('C://users/ratatosk/desktop/DRONMARKET/agent_tomato/text.xlsx')