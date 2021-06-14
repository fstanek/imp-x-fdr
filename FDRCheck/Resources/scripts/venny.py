#Import libraries
from matplotlib_venn import venn2, venn2_circles, venn2_unweighted
from matplotlib_venn import venn3, venn3_circles
from matplotlib import pyplot as plt

import xlrd
import xlsxwriter
from xlsxwriter import Workbook
from xlsxwriter import workbook
from xlsxwriter import worksheet
import os


output_filename = sys.argv[1]
path = os.path.dirname(output_filename)
name_file_excel = os.path.basename(output_filename)

input_filename_list = []
title_list = []
color_list = []

for i in range(2,len(sys.arg)-3,3):
	input_filename_list.append(sys.argv[i])
	title_list.append(sys.argv[i+1])
	color_list.append(sys.argv[i+2])

print(input_filename_list)
sys.exit()

def parsing_the_files(string_name):

	list_all_XL = []
	list_all_true_XL = []
	list_all_false_XL = []
	
	# open the sheetspreadfile and the respective sheet 
	workbook = xlrd.open_workbook(string_name, on_demand = True)
	worksheet = workbook.sheet_by_index(0)   
	worksheet.cell_value(0,0)                           #initializing cell from the excel file mentioned through the cell position
  
	print("No. of rows:", worksheet.nrows)               #Counting & Printing thenumber of rows & columns respectively
	print("No. of columns:", worksheet.ncols)
	
	
	
	i=0
	while worksheet.cell(11+i,1).value!=xlrd.empty_cell.value:
		crosslink_string = worksheet.cell(11+i,1).value
		if(crosslink_string.find(", 'score_")!=-1):
			crosslink_string = crosslink_string[0:crosslink_string.find(", 'score_")+1]+"]"

		list_all_true_XL.append(crosslink_string)
		i=i+1
	all_true_XL= i

	i=0
	while worksheet.cell(11+i,2).value!=xlrd.empty_cell.value:
		list_all_false_XL.append(worksheet.cell(11+i,2).value)
		i=i+1
	all_false_XL = i

	list_all_XL = list_all_true_XL + list_all_false_XL
	all_XL = all_true_XL + all_false_XL






	return set(list_all_XL),set(list_all_true_XL),set(list_all_false_XL)

def venn2_diagram(name1,name2):

	a1, a2, a3 = parsing_the_files(name1)
	b1, b2, b3 = parsing_the_files(name2)

	venn2(subsets = (len(a1)-len(a1 & b1), len(b1)-len(a1 & b1), len(a1 & b1)), set_labels = (title_list[0], title_list[1]), set_colors=(color_list[0], color_list[1]), alpha = 0.7)

	workbook1 = xlsxwriter.Workbook(output_filename)
	worksheet1 = workbook1.add_worksheet('all crosslinks')
	row = 0
	col = 0

	worksheet1.write(1,1,"exclusively in "+title_list[0])
	pivot_list = list(a1-(a1 & b1))
	worksheet1.write(2,1,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,1,pivot_list[i])
	
	worksheet1.write(1,2,"exclusively in "+title_list[1])
	pivot_list = list(b1-(b1 & a1))
	worksheet1.write(2,2,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,2,pivot_list[i])
	
	worksheet1.write(1,3,"overlap " + title_list[0] + ", " +  title_list[1])
	pivot_list = list(b1 & a1)
	worksheet1.write(2,3,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,3,pivot_list[i])
	
		
	plt.savefig(path + "\\" + "venn2_allcrosslinks.svg")
	plt.clf()
	venn2(subsets = (len(a2)-len(a2 & b2), len(b2)-len(a2 & b2), len(a2 & b2)), set_labels = (title_list[0], title_list[1]), set_colors=(color_list[0], color_list[1]), alpha = 0.7);

	worksheet2 = workbook1.add_worksheet("true crosslinks")
	row = 0
	col = 0

	worksheet2.write(1,1,"exclusively in "+title_list[0])
	pivot_list = list(a2-(a2 & b2))
	worksheet2.write(2,1,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,1,pivot_list[i])
	
	worksheet2.write(1,2,"exclusively in "+title_list[1])
	pivot_list = list(b2-(b2 & a2))
	worksheet2.write(2,2,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,2,pivot_list[i])
	
	worksheet2.write(1,3,"overlap " + title_list[0] + ", " +  title_list[1])
	pivot_list = list(b2 & a2)
	worksheet2.write(2,3,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,3,pivot_list[i])


	plt.savefig(path + "\\" + "venn2_truecrosslinks.svg")
	plt.clf()

	venn2(subsets = (len(a3)-len(a3 & b3), len(b3)-len(a3 & b3), len(a3 & b3)), set_labels = (title_list[0], title_list[1]), set_colors=(color_list[0], color_list[1]), alpha = 0.7);

	worksheet3 = workbook1.add_worksheet("false crosslinks")
	row = 0
	col = 0

	worksheet3.write(1,1,"exclusively in "+title_list[0])
	pivot_list = list(a3-(a3 & b3))
	worksheet3.write(2,1,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,1,pivot_list[i])
	
	worksheet3.write(1,2,"exclusively in "+title_list[1])
	pivot_list = list(b3-(b3 & a3))
	worksheet3.write(2,2,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,2,pivot_list[i])
	
	worksheet3.write(1,3,"overlap " + title_list[0] + ", " +  title_list[1])
	pivot_list = list(b3 & a3)
	worksheet3.write(2,3,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,3,pivot_list[i])

	plt.savefig(path + "\\" + "venn2_falsecrosslinks.svg")
	plt.clf()

	worksheet1.set_column(0,1,70)
	worksheet1.set_column(0,2,70)
	worksheet1.set_column(0,3,70)

	worksheet2.set_column(0,1,70)
	worksheet2.set_column(0,2,70)
	worksheet2.set_column(0,3,70)

	worksheet3.set_column(0,1,70)
	worksheet3.set_column(0,2,70)
	worksheet3.set_column(0,3,70)

	workbook1.close()

	print('RESULT: '+ name_file_excel + ', '+'venn2_allcrosslinks.svg'+', ' +'venn2_truecrosslinks.svg' + ', ' + 'venn2_falsecrosslinks.svg')


	

def venn3_diagram(name1,name2,name3):

	a1, a2, a3 = parsing_the_files(name1)
	b1, b2, b3 = parsing_the_files(name2)
	c1, c2, c3 = parsing_the_files(name3)

	venn3(subsets = (len(a1)-len(a1 & b1)-len(c1 & a1)+len(a1 & b1 & c1),
					 len(b1)-len(a1 & b1)-len(c1 & b1)+len(a1 & b1 & c1),
					 len(a1 & b1)-len(a1 & b1 & c1),
					 len(c1)-len(c1 & a1)-len(c1 & b1)+len(a1 & b1 & c1),
					 len(c1 & a1)-len(a1 & b1 & c1),
					 len(c1 & b1)-len(a1 & b1 & c1),
					 len(a1 & b1 & c1)),
					 set_labels = (title_list[0], title_list[1], title_list[2]), set_colors=(color_list[0], color_list[1], color_list[2]), alpha = 0.5);
	
	workbook3 = xlsxwriter.Workbook(output_filename)
	worksheet1 = workbook3.add_worksheet('all crosslinks')

	worksheet1.write(1,1,"exclusively in "+title_list[0])
	worksheet1.write(2,1,len(pivot_list))
	pivot_list=list(a1-(a1 & b1)-(c1 & a1))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,1,pivot_list[i])
	
	worksheet1.write(1,2,"exclusively in "+title_list[1])
	pivot_list=list(b1-(a1 & b1)-(c1 & b1))
	worksheet1.write(2,2,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,2,pivot_list[i])
	
	worksheet1.write(1,3,"overlap " + title_list[0]+ ", " + title_list[1])
	pivot_list=list((a1 & b1)-(a1 & b1 & c1))
	worksheet1.write(2,3,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,3,pivot_list[i])
	
	worksheet1.write(1,4,"exclusively in "+title_list[2])
	pivot_list=list(c1-(c1 & a1)-(c1 & b1))
	worksheet1.write(2,4,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,4,pivot_list[i])
	
	worksheet1.write(1,5,"overlap " + title_list[0]+ ", " + title_list[2])
	pivot_list=list((c1 & a1)-(a1 & b1 & c1))
	worksheet1.write(2,5,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,5,pivot_list[i])
	
	worksheet1.write(1,6,"overlap " + title_list[1]+ ", " + title_list[2])
	pivot_list=list((c1 & b1)-(a1 & b1 & c1))
	worksheet1.write(2,6,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,6,pivot_list[i])
	
	worksheet1.write(1,7,"overlap " + title_list[0]+ ", " + title_list[1] + "and" + title_list[2])
	pivot_list=list(a1 & b1 & c1)
	worksheet1.write(2,7,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,7,pivot_list[i])


	plt.savefig(path + "\\" + "venn3_allcrosslinks.svg")
	plt.clf()

	venn3(subsets = (len(a2)-len(a2 & b2)-len(c2 & a2)+len(a2 & b2 & c2),
					 len(b2)-len(a2 & b2)-len(c2 & b2)+len(a2 & b2 & c2),
					 len(a2 & b2)-len(a2 & b2 & c2),
					 len(c2)-len(c2 & a2)-len(c2 & b2)+len(a2 & b2 & c2),
					 len(c2 & a2)-len(a2 & b2 & c2),
					 len(c2 & b2)-len(a2 & b2 & c2),
					 len(a2 & b2 & c2)),
					 set_labels = (title_list[0], title_list[1], title_list[2]), set_colors=(color_list[0], color_list[1], color_list[2]), alpha = 0.5);

	worksheet2 = workbook3.add_worksheet('true crosslinks')

	worksheet2.write(1,1,"exclusively in "+title_list[0])
	pivot_list=list(a2-(a2 & b2)-(c2 & a2))
	worksheet2.write(2,1,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,1,pivot_list[i])
	
	worksheet2.write(1,2,"exclusively in "+title_list[1])
	pivot_list=list(b2-(a2 & b2)-(c2 & b2))
	worksheet2.write(2,2,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,2,pivot_list[i])
	
	worksheet2.write(1,3,"overlap " + title_list[0]+ ", " + title_list[1])
	pivot_list=list((a2 & b2)-(a2 & b2 & c2))
	worksheet2.write(2,3,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,3,pivot_list[i])
	
	worksheet2.write(1,4,"exclusively in "+title_list[2])
	pivot_list=list(c2-(c2 & a2)-(c2 & b2))
	worksheet2.write(2,4,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,4,pivot_list[i])
	
	worksheet2.write(1,5,"overlap " + title_list[0]+ ", " + title_list[2])
	pivot_list=list((c2 & a2)-(a2 & b2 & c2))
	worksheet2.write(2,5,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,5,pivot_list[i])
	
	worksheet2.write(1,6,"overlap " + title_list[1]+ ", " + title_list[2])
	pivot_list=list((c2 & b2)-(a2 & b2 & c2))
	worksheet2.write(2,6,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,6,pivot_list[i])
	
	worksheet2.write(1,7,"overlap " + title_list[0]+ ", " + title_list[1] + "and" + title_list[2])
	pivot_list=list(a2 & b2 & c2)
	worksheet2.write(2,7,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,7,pivot_list[i])

	plt.savefig(path + "\\" + "venn3_truecrosslinks.svg")
	plt.clf()
	venn3(subsets = (len(a3)-len(a3 & b3)-len(c3 & a3)+len(a3 & b3 & c3),
					 len(b3)-len(a3 & b3)-len(c3 & b3)+len(a3 & b3 & c3),
					 len(a3 & b3)-len(a3 & b3 & c3),
					 len(c3)-len(c3 & a3)-len(c3 & b3)+len(a3 & b3 & c3),
					 len(c3 & a3)-len(a3 & b3 & c3),
					 len(c3 & b3)-len(a3 & b3 & c3),
					 len(a3 & b3 & c3)),
					 set_labels = (title_list[0], title_list[1], title_list[2]), set_colors=(color_list[0], color_list[1], color_list[2]), alpha = 0.5);

	worksheet3 = workbook3.add_worksheet('false crosslinks')

	worksheet3.write(1,1,"exclusively in "+title_list[0])
	pivot_list=list(a3-(a3 & b3)-(c3 & a3))
	worksheet3.write(2,1,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,1,pivot_list[i])
	
	worksheet3.write(1,2,"exclusively in "+title_list[1])
	pivot_list=list(b3-(a3 & b3)-(c3 & b3))
	worksheet3.write(2,2,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,2,pivot_list[i])
	
	worksheet3.write(1,3,"overlap " + title_list[0]+ ", " + title_list[1])
	pivot_list=list((a3 & b3)-(a3 & b3 & c3))
	worksheet3.write(2,3,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,3,pivot_list[i])
	
	worksheet3.write(1,4,"exclusively in "+title_list[2])
	pivot_list=list(c3-(c3 & a3)-(c3 & b3))
	worksheet3.write(2,4,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,4,pivot_list[i])
	
	worksheet3.write(1,5,"overlap " + title_list[0]+ ", " + title_list[2])
	pivot_list=list((c3 & a3)-(a3 & b3 & c3))
	worksheet3.write(2,5,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,5,pivot_list[i])
	
	worksheet3.write(1,6,"overlap " + title_list[1]+ ", " + title_list[2])
	pivot_list=list((c3 & b3)-(a3 & b3 & c3))
	worksheet3.write(2,6,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,6,pivot_list[i])
	
	worksheet3.write(1,7,"overlap " + title_list[0]+ ", " + title_list[1] + "and" + title_list[2])
	pivot_list=list(a3 & b3 & c3)
	worksheet3.write(2,7,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,7,pivot_list[i])

	plt.savefig(path + "\\" + "venn3_falsecrosslinks.svg")
	plt.clf()

	worksheet1.set_column(0,1,70)
	worksheet1.set_column(0,2,70)
	worksheet1.set_column(0,3,70)
	worksheet1.set_column(0,4,70)
	worksheet1.set_column(0,5,70)
	worksheet1.set_column(0,6,70)
	worksheet1.set_column(0,7,70)

	worksheet2.set_column(0,1,70)
	worksheet2.set_column(0,2,70)
	worksheet2.set_column(0,3,70)
	worksheet2.set_column(0,4,70)
	worksheet2.set_column(0,5,70)
	worksheet2.set_column(0,6,70)
	worksheet2.set_column(0,7,70)

	worksheet3.set_column(0,1,70)
	worksheet3.set_column(0,2,70)
	worksheet3.set_column(0,3,70)
	worksheet3.set_column(0,4,70)
	worksheet3.set_column(0,5,70)
	worksheet3.set_column(0,6,70)
	worksheet3.set_column(0,7,70)

	workbook3.close()

	print('RESULT: '+ name_file_excel + ', '+'venn3_allcrosslinks.svg'+', ' +'venn3_truecrosslinks.svg' + ', ' + 'venn3_falsecrosslinks.svg')

def venn4_diagram(name1,name2,name3,name4):

	a1, a2, a3 = parsing_the_files(name1)
	b1, b2, b3 = parsing_the_files(name2)
	c1, c2, c3 = parsing_the_files(name3)
	d1, d2, d3 = parsing_the_files(name4)

	workbook4 = xlsxwriter.Workbook(output_filename)

	import venn

	labels = venn.get_labels([a1,b1,c1,d1], fill=['number'])
	fig, ax = venn.venn4(labels, names=[title_list[0],title_list[1],title_list[2],title_list[3]])
	fig.savefig(path + "\\" + "venn4_allcrosslinks.svg")
	fig.clf()

	labels = venn.get_labels([a2,b2,c2,d2], fill=['number'])
	fig, ax = venn.venn4(labels, names=[title_list[0],title_list[1],title_list[2],title_list[3]])
	fig.savefig(path + "\\" + "venn4truecrosslinks.svg")
	fig.clf()

	labels = venn.get_labels([a3,b3,c3,d3], fill=['number'])
	fig, ax = venn.venn4(labels, names=[title_list[0],title_list[1],title_list[2],title_list[3]])
	fig.savefig(path + "\\" + "venn4falsecrosslinks.svg")
	fig.clf()

	worksheet1 = workbook4.add_worksheet('all crosslinks')

	worksheet1.write(1,1,"present in at least one group")
	pivot_list=list(a1 | b1 | c1 | d1)
	worksheet1.write(2,1,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,1,pivot_list[i])
	
	worksheet1.write(1,2,"present in at least two groups")
	pivot_list=list((a1 & b1) | (a1 & c1) | (a1 & d1) | (b1 & c1) | (b1 & d1) | (c1 & d1))
	worksheet1.write(2,2,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,2,pivot_list[i])
	
	worksheet1.write(1,3,"present in at least three groups")
	pivot_list = list((a1 & b1 & c1) | (a1 & b1 & d1) | (a1 & c1 & d1) | (b1 & c1 & d1))
	worksheet1.write(2,3,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,3,pivot_list[i])

	worksheet1.write(1,4,"present in all four groups")
	pivot_list = list(a1 & b1 & c1 & d1)
	worksheet1.write(2,4,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet1.write(3+i,4,pivot_list[i])
	
	
	
	
	worksheet2 = workbook4.add_worksheet('true crosslinks')

	worksheet2.write(1,1,"present in at least one group")
	pivot_list=list(a2 | b2 | c2 | d2)
	worksheet2.write(2,1,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,1,pivot_list[i])
	
	worksheet2.write(1,2,"present in at least two groups")
	pivot_list=list((a2 & b2) | (a2 & c2) | (a2 & d2) | (b2 & c2) | (b2 & d2) | (c2 & d2))
	worksheet2.write(2,2,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,2,pivot_list[i])
	
	worksheet2.write(1,3,"present in at least three groups")
	pivot_list = list((a2 & b2 & c2) | (a2 & b2 & d2) | (a2 & c2 & d2) | (b2 & c2 & d2))
	worksheet2.write(2,3,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,3,pivot_list[i])

	worksheet2.write(1,4,"present in all four groups")
	pivot_list = list(a2 & b2 & c2 & d2)
	worksheet2.write(2,4,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet2.write(3+i,4,pivot_list[i])
	
	
	worksheet3 = workbook4.add_worksheet('false crosslinks')

	worksheet3.write(1,1,"present in at least one group")
	pivot_list=list(a3 | b3 | c3 | d3)
	worksheet3.write(2,1,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,1,pivot_list[i])
	
	worksheet3.write(1,2,"present in at least two groups")
	pivot_list=list((a3 & b3) | (a3 & c3) | (a3 & d3) | (b3 & c3) | (b3 & d3) | (c3 & d3))
	worksheet3.write(2,2,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,2,pivot_list[i])
	
	worksheet3.write(1,3,"present in at least three groups")
	pivot_list = list((a3 & b3 & c3) | (a3 & b3 & d3) | (a3 & c3 & d3) | (b3 & c3 & d3))
	worksheet3.write(2,3,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,3,pivot_list[i])

	worksheet3.write(1,4,"present in all four groups")
	pivot_list = list(a3 & b3 & c3 & d3)
	worksheet3.write(2,4,len(pivot_list))
	for i in range(len(pivot_list)):
		worksheet3.write(3+i,4,pivot_list[i])

	
	
	worksheet1.set_column(0,1,70)
	worksheet1.set_column(0,2,70)
	worksheet1.set_column(0,3,70)
	worksheet1.set_column(0,4,70)


	worksheet2.set_column(0,1,70)
	worksheet2.set_column(0,2,70)
	worksheet2.set_column(0,3,70)
	worksheet2.set_column(0,4,70)


	worksheet3.set_column(0,1,70)
	worksheet3.set_column(0,2,70)
	worksheet3.set_column(0,3,70)
	worksheet3.set_column(0,4,70)

	workbook4.close()

	print('RESULT: '+ name_file_excel + ', '+'venn4_allcrosslinks.svg'+', ' +'venn4_truecrosslinks.svg' + ', ' + 'venn4_falsecrosslinks.svg')

import sys

try:

	a = (len(sys.argv)-2)/3


	if a == 2:

		address_of_the_first_file = sys.argv[1]
		address_of_the_second_file = sys.argv[4]

		venn2_diagram(address_of_the_first_file,address_of_the_second_file)

	elif a== 3:
		address_of_the_first_file = sys.argv[1]
		address_of_the_second_file = sys.argv[4]
		address_of_the_third_file = sys.argv[7]

		venn3_diagram(address_of_the_first_file,address_of_the_second_file,address_of_the_third_file)

	elif a == 4:
		
		address_of_the_first_file = sys.argv[1]
		address_of_the_second_file = sys.argv[4]
		address_of_the_third_file = sys.argv[7]
		address_of_the_fourth_file = sys.argv[10]

		venn4_diagram(address_of_the_first_file,address_of_the_second_file,address_of_the_third_file,address_of_the_fourth_file)
except Exception as e:
	print(e, file=sys.stderr)








