#!/usr/bin/python
#-*- encoding: utf-8 -*-

import openpyxl as xl
import Tkinter as t

wb = xl.load_workbook("../QO10 - Copie.xlsx", guess_types=True)


#root = t.Tk()
#text = t.Text(root)
#scrollbar = t.Scrollbar(root)
#scrollbar.pack( side = t.RIGHT, fill=t.Y )
#scroll2 = t.Scrollbar(root,orient=t.HORIZONTAL)
#scroll2.pack( side = t.BOTTOM, fill=t.X )


#text = t.Listbox(root, yscrollcommand = scrollbar.set, xscrollcommand=scroll2.set )

corpus=dict()

for row in wb['A1']:
	#text.insert(t.END, u" | ".join([ unicode(cell.value)  for cell in row])+"\n")
	corpus[row[1].value]=row[2].value
	
	
	
	
#text.pack( side = t.LEFT, fill = t.BOTH, expand=1 )
#scroll2.config( command = text.xview )
#scrollbar.config( command = text.yview )
#text.pack()
#root.mainloop()
