#BIOpython-Annika_Deep_investigations

from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from numpy.core.fromnumeric import size
from weblogo import color
import xlrd
import xlsxwriter
import matplotlib.pyplot as plt
import math
import seqlogo
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True
import pandas as pd
import PIL
import numpy as np
import argparse
from toolz import unique
import csv


parser = argparse.ArgumentParser()
parser.add_argument("input_file_name")
parser.add_argument("support_file_name")
parser.add_argument("output_file_name")

parser.add_argument("-XLer", "--crosslinker", type=str,
					help="change the name of the header for the Crosslinker. Please introduce quotation marks, espacially if the name contains whitespaces", default ="Crosslinker")
parser.add_argument("-sA", "--sequence_A", type=str,
					help="change the name of the header for the Sequence A. Please introduce quotation marks, especially if the name contains whitespaces!", default="Sequence A")
parser.add_argument("-sB", "--sequence_B", type=str,
					help="change the name of the header for the Sequence A. Please introduce quotation marks, especially if the name contains whitespaces!", default="Sequence B")
parser.add_argument("-naprotA","--name_of_protein_A", type=str,
					help="change the name of the header for the Protein-Name-A. Please introduce quotation marks, especially if the name contains whitespaces!", default="Accession A")
parser.add_argument("-naprotB","--name_of_protein_B", type=str,
					help="change the name of the header for the Protein-Name-A. Please introduce quotation marks, especially if the name contains whitespaces!", default="Accession B")
parser.add_argument("-bscr", "--CSM_score", type=str,
					help="change the name of the header for the CSM-score of the crosslink. Please introduce quotation marks, especially if the name contains whitespaces!", default="Combined Score")
parser.add_argument("-pospA", "--position_in_sequence_A",
					help="change the name of the header for the position of the binding aminoacid in the protein A. Please introduce quotation marks, especially if the name contains whitespaces!",default="Crosslinker Position A")
parser.add_argument("-pospB", "--position_in_sequence_B",
					help="change the name of the header for the position of the binding aminoacid in the protein B. Please introduce quotation marks, especially if the name contains whitespaces!",default="Crosslinker Position B")
parser.add_argument("-rt", "--retention_time", type=str,
					help="change the name of the header for the retention time. Please introduce quotation marks, especially if the name contains whitespaces!", default="RT [min]")             
args = parser.parse_args()


'''




average_value_of_XL = 0


'''
DSSO_mass = 158.00376
CDI_mass = 25.97926
DSBU_mass = 196.084792
DSBSO_mass_unhydrolysed = 419.1185
DSBSO_mass_hydrolysed = 308.03883
ADH_mass = 138.09055
DHSO_mass = 186.0575
DSS_mass = 138.06808
DMTMM_mass = -18.01056
PhoX_mass = 209.97181

dictionary_of_aminoacids = {'A':0.0, 'C':0.0, 'D':0.0,
							'E':0.0, 'F':0.0, 'G':0.0,
							'H':0.0, 'I':0.0, 'K':0.0,
							'L':0.0, 'M':0.0, 'N':0.0,
							'P':0.0, 'Q':0.0, 'R':0.0,
							'S':0.0, 'T':0.0, 'V':0.0,
							'W':0.0, 'Y':0.0}

dictionary_of_aminoacids_reduced_1 = {'A':0.0, 'C':0.0, 'D':0.0,
									'E':0.0, 'F':0.0, 'G':0.0,
									'H':0.0, 'I':0.0, 'K':0.0,
									'L':0.0, 'M':0.0, 'N':0.0,
									'P':0.0, 'Q':0.0, 'R':0.0,
									'S':0.0, 'T':0.0, 'V':0.0,
									'W':0.0, 'Y':0.0, 'X':0.0,
									'*':0.0, '-':0.0}
dictionary_of_aminoacids_reduced_2 = {'A':0.0, 'C':0.0, 'D':0.0,
									'E':0.0, 'F':0.0, 'G':0.0,
									'H':0.0, 'I':0.0, 'K':0.0,
									'L':0.0, 'M':0.0, 'N':0.0,
									'P':0.0, 'Q':0.0, 'R':0.0,
									'S':0.0, 'T':0.0, 'V':0.0,
									'W':0.0, 'Y':0.0, 'X':0.0,
									'*':0.0, '-':0.0}
dictionary_of_aminoacids_reduced_3 = {'A':0.0, 'C':0.0, 'D':0.0,
									'E':0.0, 'F':0.0, 'G':0.0,
									'H':0.0, 'I':0.0, 'K':0.0,
									'L':0.0, 'M':0.0, 'N':0.0,
									'P':0.0, 'Q':0.0, 'R':0.0,
									'S':0.0, 'T':0.0, 'V':0.0,
									'W':0.0, 'Y':0.0, 'X':0.0,
									'*':0.0, '-':0.0}
dictionary_of_aminoacids_reduced_4 = {'A':0.0, 'C':0.0, 'D':0.0,
									'E':0.0, 'F':0.0, 'G':0.0,
									'H':0.0, 'I':0.0, 'K':0.0,
									'L':0.0, 'M':0.0, 'N':0.0,
									'P':0.0, 'Q':0.0, 'R':0.0,
									'S':0.0, 'T':0.0, 'V':0.0,
									'W':0.0, 'Y':0.0, 'X':0.0,
									'*':0.0, '-':0.0}
dictionary_of_aminoacids_reduced_5 = {'A':0.0, 'C':0.0, 'D':0.0,
									'E':0.0, 'F':0.0, 'G':0.0,
									'H':0.0, 'I':0.0, 'K':0.0,
									'L':0.0, 'M':0.0, 'N':0.0,
									'P':0.0, 'Q':0.0, 'R':0.0,
									'S':0.0, 'T':0.0, 'V':0.0,
									'W':0.0, 'Y':0.0, 'X':0.0,
									'*':0.0, '-':0.0}
dictionary_of_aminoacids_reduced_6 = {'A':0.0, 'C':0.0, 'D':0.0,
									'E':0.0, 'F':0.0, 'G':0.0,
									'H':0.0, 'I':0.0, 'K':0.0,
									'L':0.0, 'M':0.0, 'N':0.0,
									'P':0.0, 'Q':0.0, 'R':0.0,
									'S':0.0, 'T':0.0, 'V':0.0,
									'W':0.0, 'Y':0.0, 'X':0.0,
									'*':0.0, '-':0.0}

list_one_letter_code = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']






#
#
#
#
#
#
#
groups_support_file = args.support_file_name

workbook_groups = xlrd.open_workbook(groups_support_file, on_demand = True)
worksheet_groups = workbook_groups.sheet_by_index(0)

number_groups = 0
peptides_per_group = []
# identify the number of groups
for i in range(worksheet_groups.nrows):
	if worksheet_groups.cell(i, 0).value.find("Group")!=-1:
		number_groups = number_groups +1
		peptides_per_group.append(i)

# add the position where the first empty cell is found
peptides_per_group.append(worksheet_groups.nrows)

#subtract the positions of group headers in order to calculate the number of peptides per group
for i in range(number_groups):
	peptides_per_group[i] = peptides_per_group[i+1]-peptides_per_group[i]-1

peptides_per_group = peptides_per_group[:-1]



# in list_of_groups there will be all peptides groups with all their members stored 
list_of_groups = []
# will be added to the list_of_groups and contains temporary the members of one group at the time
list_of_peptides_per_group = []


# all peptide sequences present in the excel document are read one by oneand the added to the list of groups
# list of peptides per group will be permanently emptied to make space for the other groups 
# the number of list of peptides per group is static, not dynamic and should be kept constant
pivot_excel = 1

for i in range(1,number_groups+1):
	if i!=1:
		pivot_excel = pivot_excel+peptides_per_group[i-2]+1
	list_of_peptides_per_group = []
	for j in range(0,peptides_per_group[i-1]):
		list_of_peptides_per_group.append(worksheet_groups.cell(pivot_excel+j, 0).value)
	a = list_of_peptides_per_group
	list_of_groups.append(a)
#
#
#
#
#


name_file_annika_theorie= groups_support_file

counter=0

loc = name_file_annika_theorie        #Giving the location of the file 

wb = xlrd.open_workbook(loc)                    #opening & reading the excel file
s1 = wb.sheet_by_index(0)                     #extracting the worksheet
s1.cell_value(0,0)                            #initializing cell from the excel file mentioned through the cell position

print("No. of rows:", s1.nrows)               #Counting & Printing thenumber of rows & columns respectively
print("No. of columns:", s1.ncols)

ws = wb.sheet_by_index(0)

for i in range(1,s1.nrows):
	if(ws.cell(i,0).value.find('Group')!=0):
		print(ws.cell(i,0).value,ws.cell(i,1).value)


list_theoretical_XL = []

pivot_theoretical = 1
pivot_local = 1
while pivot_local!=s1.nrows:
	while (ws.cell(pivot_local,0).value.find('Group')!=0) and pivot_local!=s1.nrows-1:
		print(pivot_local,ws.cell(pivot_local,0).value.find('Group') )
		pivot_local = pivot_local +1
	start_position = pivot_theoretical
	if pivot_local==s1.nrows-1:
		pivot_local = s1.nrows
	for i in range(start_position, pivot_local,1):
		pivot_theoretical = i
		for j in range(pivot_theoretical, pivot_local,1):
			list_theoretical_XL.append([ws.cell(pivot_theoretical,0).value,ws.cell(j,0).value,1,"pn1","pn2",1,1,1,1,int(ws.cell(pivot_theoretical,1).value),int(ws.cell(j,1).value)])
			print(ws.cell(pivot_theoretical,0).value,ws.cell(j,0).value,int(ws.cell(pivot_theoretical,1).value),int(ws.cell(j,1).value))
	pivot_theoretical=pivot_local+1
	if pivot_local!=s1.nrows:
		pivot_local = pivot_local +1




list_theoretical_XL = list(map(list,unique(map(tuple,list_theoretical_XL))))
print("number of theoretical crosslinks:"+str(len(list_theoretical_XL)))
#
#
#
#
#









name_file_annika= args.input_file_name

import os
name_of_the_image = os.path.splitext(name_file_annika)[0]


# detect the current working directory and print it
path = os.path.abspath(args.output_file_name)

# define the name of the directory to be created
if os.path.isdir(path)==False:
	os.mkdir(path)

#
#
#
#
counter=0

loc = name_file_annika         #Giving the location of the file 
  
wb = xlrd.open_workbook(loc)                    #opening & reading the excel file
s1 = wb.sheet_by_index(0)                     #extracting the worksheet
s1.cell_value(0,0)                            #initializing cell from the excel file mentioned through the cell position
  
print("No. of rows:", s1.nrows)               #Counting & Printing thenumber of rows & columns respectively
print("No. of columns:", s1.ncols)

ws = wb.sheet_by_index(0)

character_to_delete = ["{","[","]","}","X","J"]
unique_crosslinks = []
list_of_scores_annika = []
list_of_areas_annika = []
list_of_number_of_CSMs = []
temporary_areas = []

#
#
#
#
#
#
#
#
#doooooooooooo


header_name_seq_A = args.sequence_A
header_name_seq_B = args.sequence_B
header_name_protein_A = args.name_of_protein_A
header_name_protein_B = args.name_of_protein_B
header_position_AminoAcid_A = args.position_in_sequence_A
header_position_AminoAcid_B = args.position_in_sequence_B
header_score = args.CSM_score
header_crosslinker = args.crosslinker
header_retention = args.retention_time

column_pos_Protein_A = -1
column_pos_Protein_B = -1
column_pos_score = -1


for i in range(ws.ncols):
	if ws.cell(0,i).value == header_name_seq_A:
		column_pos_Sequence_A = i
	elif ws.cell(0,i).value == header_name_seq_B:
		column_pos_Sequence_B = i
	elif ws.cell(0,i).value == header_name_protein_A:
		column_pos_Protein_A = i
	elif ws.cell(0,i).value == header_name_protein_B:
		column_pos_Protein_B = i
	elif ws.cell(0,i).value == header_position_AminoAcid_A:
		column_pos_Position_AA_A = i
	elif ws.cell(0,i).value == header_position_AminoAcid_B:
		column_pos_Position_AA_B = i
	elif ws.cell(0,i).value == header_score:
		column_pos_score = i
	elif ws.cell(0,i).value == header_crosslinker:
		column_crosslinker = i
	elif ws.cell(0,i).value == header_retention:
		column_retention = i



if column_pos_Protein_A==-1 or column_pos_Protein_B==-1 or column_pos_score==-1:
	header_name_protein_A = "Protein Accession A"
	header_name_protein_B = "Protein Accession B"
	header_score = "XlinkX Score"

	for i in range(ws.ncols):
		if ws.cell(0,i).value == header_name_protein_A:
			column_pos_Protein_A = i
		elif ws.cell(0,i).value == header_name_protein_B:
			column_pos_Protein_B = i 
		elif ws.cell(0,i).value == header_score:
			column_pos_score = i


for i in range(1,s1.nrows):
	try:
		position_in_peptide_1 = int(ws.cell(i,column_pos_Position_AA_A).value)-1
		position_in_peptide_2 = int(ws.cell(i,column_pos_Position_AA_B).value)-1
		string1 = ws.cell(i,column_pos_Sequence_A).value
		string2 = ws.cell(i,column_pos_Sequence_B).value
		protein_name_1 = ws.cell(i,column_pos_Protein_A).value
		protein_name_2 = ws.cell(i,column_pos_Protein_B).value
		score = float(ws.cell(i,column_pos_score).value)
		retention_time = float(ws.cell(i,column_retention).value)
	except:
		string1 = ws.cell(i,column_pos_Sequence_A).value
		string2 = ws.cell(i,column_pos_Sequence_B).value
		retention_time = float(ws.cell(i,column_retention).value)

		def read_until_find_undecided(example_string):
			a = example_string.find(";")
			b_list = list(example_string)
			if a!=-1:
				construct_pivot=0
				word = ""
				while construct_pivot<a:
					word = word + b_list[construct_pivot]
					construct_pivot = construct_pivot+1
				return word
			else:
				return example_string

		protein_name_1 = read_until_find_undecided(ws.cell(i,column_pos_Protein_A).value)
		protein_name_2 = read_until_find_undecided(ws.cell(i,column_pos_Protein_B).value)
		protein_name_1 = read_until_find_undecided(ws.cell(i,column_pos_Protein_A).value)
		protein_name_2 = read_until_find_undecided(ws.cell(i,column_pos_Protein_B).value)

		position_in_peptide_1 = int(read_until_find_undecided(ws.cell(i,column_pos_Position_AA_A).value))-1
		position_in_peptide_2 = int(read_until_find_undecided(ws.cell(i,column_pos_Position_AA_B).value))-1

		score = float(ws.cell(i,column_pos_score).value)

	unique_crosslinks.append([string1,string2,retention_time,protein_name_1,protein_name_2,1,1,1,1,position_in_peptide_1,position_in_peptide_2])
	list_of_scores_annika.append(score)



def order_alphabetically(example_list):

	example_list2= []

	for i in range(len(example_list)):
		example_list2 = example_list[i][0:2]

		
		if (example_list[i][0:2] != sorted(example_list2[0:2])):
			
			exchange = example_list[i][0]
			example_list[i][0] = example_list[i][1]
			example_list[i][1] = exchange

			exchange = example_list[i][3]
			example_list[i][3] = example_list[i][4]
			example_list[i][4] = exchange

			exchange = example_list[i][5]
			example_list[i][5] = example_list[i][6]
			example_list[i][6] = exchange

			exchange = example_list[i][9]
			example_list[i][9] = example_list[i][10]
			example_list[i][10] = exchange




			

	return  example_list;

unique_crosslinks = order_alphabetically(unique_crosslinks)
list_theoretical_XL = order_alphabetically(list_theoretical_XL)
for i in range(len(unique_crosslinks)):
	print(unique_crosslinks[i])

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
all_crosslinks = 0
correct_crosslinks = 0
homeotypic = 0

unique_crosslinks_true = []
unique_crosslinks_false = []
retention_list = []

for j in range(len(unique_crosslinks)):
	found = False
	k = 0
	while(k<number_groups and found == False):
		l = 0
		while(l<peptides_per_group[k] and found == False):
			if unique_crosslinks[j][0] == list_of_groups[k][l] or unique_crosslinks[j][0] in list_of_groups[k][l] :
				m = 0
				#this will make a difference in case the support file contains the undigested version of the peptides
				

				while(m<peptides_per_group[k] and found== False):
					if (unique_crosslinks[j][1]== list_of_groups[k][m] or unique_crosslinks[j][1] in list_of_groups[k][m]):
						found = True
						

						temporary_position_finder = unique_crosslinks[j][0] 
						unique_crosslinks[j][0] = list_of_groups[k][l]
						unique_crosslinks[j][9] = unique_crosslinks[j][9] + unique_crosslinks[j][0].find(temporary_position_finder)
						#this will make a difference in case the support file contains the undigested version of the peptides
						temporary_position_finder = unique_crosslinks[j][1]
						unique_crosslinks[j][1] = list_of_groups[k][m]
						unique_crosslinks[j][10] = unique_crosslinks[j][10] + unique_crosslinks[j][1].find(temporary_position_finder)

						correct_crosslinks = correct_crosslinks +1
						unique_crosslinks_true.append(unique_crosslinks[j])
						if unique_crosslinks[j][0] == unique_crosslinks[j][1]:
							homeotypic = homeotypic+1
					else:
						m = m+1
			l = l+1
		k = k+1
	if found == False:
		unique_crosslinks_false.append(unique_crosslinks[j])

unique_crosslinks_true=order_alphabetically(unique_crosslinks_true)

print("Number of unique crosslinks:" + str(len(unique_crosslinks)))
print("Number of unique true crosslinks:" + str(len(unique_crosslinks_true)))
print(unique_crosslinks_true)
print("Number of unique false crosslinks:" + str(len(unique_crosslinks_false)))
print(number_groups)
print(peptides_per_group)
for i in range(len(list_of_groups)):
	print(list_of_groups[i])
for i in range(len(unique_crosslinks_false)):
	print(unique_crosslinks_false[i])
#

#

#
DSSO_mass = 158.00376
CDI_mass = 25.97926
DSBU_mass = 196.084792
DSBSO_mass_unhydrolysed = 419.1185
DSBSO_mass_hydrolysed = 308.03883
ADH_mass = 138.09055
DHSO_mass = 186.0575
DSS_mass = 138.06808
DMTMM_mass = -18.01056
PhoX_mass = 209.97181

mass_crosslinker=158

if ws.cell(1,column_crosslinker).value == "DSSO":
	mass_crosslinker = DSSO_mass
elif ws.cell(1,column_crosslinker).value == "CDI":
	mass_crosslinker= CDI_mass
elif ws.cell(1,column_crosslinker).value == "DSBU":
	mass_crosslinker = DSBU_mass
elif ws.cell(1,column_crosslinker).value == "DSBSO":
	mass_crosslinker = DSBSO_mass_hydrolysed
elif ws.cell(1,column_crosslinker).value == "ADH":
	mass_crosslinker = ADH_mass
elif ws.cell(1,column_crosslinker).value == "DHSO":
	mass_crosslinker = DHSO_mass
elif ws.cell(1,column_crosslinker).value == "DMTMM" or ws.cell(1,column_crosslinker).value == "EDC":
	mass_crosslinker = DMTMM_mass
elif ws.cell(1,column_crosslinker).value == "PhoX":
	mass_crosslinker = PhoX_mass

def gravy_index(list_gravy_index,weighted):
	list_return = []
	for i in range(len(list_gravy_index)):
		analysed_seq = ProteinAnalysis(list_gravy_index[i][0])
		gravy_value_1 = analysed_seq.gravy()
		analysed_seq = ProteinAnalysis(list_gravy_index[i][1])
		gravy_value_2 = analysed_seq.gravy()
		gravy_value_average_XL = ((gravy_value_1*len(list_gravy_index[i][0])) + (gravy_value_2*len(list_gravy_index[i][1])))/(len(list_gravy_index[i][0])+len(list_gravy_index[i][1]))
		if weighted==True:	
			for j in range(list_gravy_index[i][8]):
				list_return.append(gravy_value_average_XL)
		else:
			list_return.append(gravy_value_average_XL)
	return list_return

	
def mass_index(list_mass,weighted):
	list_return = []
	for i in range(len(list_mass)):
		analysed_seq= ProteinAnalysis(list_mass[i][0])
		mass_value_1 = analysed_seq.molecular_weight()
		analysed_seq= ProteinAnalysis(list_mass[i][1])
		mass_value_2 = analysed_seq.molecular_weight()
		mass_value_average = mass_value_1+mass_value_2 + mass_crosslinker 
		if weighted ==True:
			for j in range(list_mass[i][8]):
				list_return.append(mass_value_average)
		else:
				list_return.append(mass_value_average)
	return list_return


def isoelectric_point_index(list_isoelectric_point,weighted):
	list_return = []
	for i in range(len(list_isoelectric_point)):
		analysed_seq= ProteinAnalysis(list_isoelectric_point[i][0])
		isoelectric_value_1 = analysed_seq.isoelectric_point()
		analysed_seq= ProteinAnalysis(list_isoelectric_point[i][1])
		isoelectric_value_2 = analysed_seq.isoelectric_point()
		weighter_1 = list_isoelectric_point[i][0].count("K")+list_isoelectric_point[i][0].count("R")+list_isoelectric_point[i][0].count("H")+list_isoelectric_point[i][0].count("D")+list_isoelectric_point[i][0].count("E")
		weighter_2 = list_isoelectric_point[i][1].count("K")+list_isoelectric_point[i][1].count("R")+list_isoelectric_point[i][1].count("H")+list_isoelectric_point[i][1].count("D")+list_isoelectric_point[i][1].count("E")
					 
		isoelectric_value_average = ((isoelectric_value_1*weighter_1)+(isoelectric_value_2*weighter_2))/(weighter_1+weighter_2)
		if weighted==True:
			for j in range(list_isoelectric_point[i][8]):
				list_return.append(isoelectric_value_average)
		else:
			list_return.append(isoelectric_value_average)
			
	return list_return
		




def charge_at_ph_index(list_charge_at_pH,value_of_pH,weighted):

	list_return = []

	for i in range(len(list_charge_at_pH)):
		peptide_without_bounded_position = ""
		if list_charge_at_pH[i][9] == 0:
			string_pivot = list_charge_at_pH[i][0]
			peptide_without_bounded_position = string_pivot[1:]
		elif list_charge_at_pH[i][9] == len(list_charge_at_pH[i][0])-1:
			string_pivot = list_charge_at_pH[i][0]
			peptide_without_bounded_position = string_pivot[:-1]
		else:
			string_pivot = list_charge_at_pH[i][0]
			peptide_without_bounded_position = string_pivot[:list_charge_at_pH[i][9]] + string_pivot[(list_charge_at_pH[i][9]+1):]
		
		analysed_seq = ProteinAnalysis(peptide_without_bounded_position)
		charge_1 = analysed_seq.charge_at_pH(value_of_pH)

		peptide_without_bounded_position = ""
		if list_charge_at_pH[i][10] == 0:
			string_pivot = list_charge_at_pH[i][1]
			peptide_without_bounded_position = string_pivot[1:]
		elif list_charge_at_pH[i][10] == len(list_charge_at_pH[i][1])-1:
			string_pivot = list_charge_at_pH[i][1]
			peptide_without_bounded_position = string_pivot[:-1]
		else:
			string_pivot = list_charge_at_pH[i][1]
			peptide_without_bounded_position = string_pivot[:list_charge_at_pH[i][10]] + string_pivot[(list_charge_at_pH[i][10]+1):]
		
		analysed_seq = ProteinAnalysis(peptide_without_bounded_position)
		charge_2 = analysed_seq.charge_at_pH(value_of_pH)
		if weighted==True:
			for j in range(list_charge_at_pH[i][8]):
				list_return.append(charge_1+charge_2)
		else:
			list_return.append(charge_1+charge_2)

	return list_return





#value_of_the_pH = float(input("The value of the pH: "))
value_of_the_pH = 3.55


def aromaticity_index(list_aromaticity,weighted):
	list_return = []
	for i in range (len(list_aromaticity)):
		analysed_seq= ProteinAnalysis(list_aromaticity[i][0])
		aromaticity_value_1 = analysed_seq.aromaticity()
		analysed_seq= ProteinAnalysis(list_aromaticity[i][1])
		aromaticity_value_2 = analysed_seq.aromaticity()
		aromaticity_value_average = ((aromaticity_value_1*len(list_aromaticity[i][0]))+(aromaticity_value_2*len(list_aromaticity[i][1])))/(len(list_aromaticity[i][0])+len(list_aromaticity[i][1]))
		if weighted==True:
			for j in range(list_aromaticity[i][8]):
				list_return.append(aromaticity_value_average)
		else:
			list_return.append(aromaticity_value_average)
		
	return list_return




def get_amino_acids_percent(list_amino_acid_percent):
	amino_acid_percent_all = np.zeros(20)
	for i in range(len(list_amino_acid_percent)):
		analysed_seq = ProteinAnalysis(list_amino_acid_percent[i][0])
		amino_acid_percent_1 = np.array(list(analysed_seq.get_amino_acids_percent().values()))

		analysed_seq = ProteinAnalysis(list_amino_acid_percent[i][1])
		amino_acid_percent_2 = np.array(list(analysed_seq.get_amino_acids_percent().values()))

		amino_acid_percent_average  = (((amino_acid_percent_1*len(list_amino_acid_percent[i][0])) + (amino_acid_percent_2*len(list_amino_acid_percent[i][1])))/(len(list_amino_acid_percent[i][0])+len(list_amino_acid_percent[i][1])))*list_amino_acid_percent[i][8]
		amino_acid_percent_all = amino_acid_percent_all + amino_acid_percent_average
	
	normalization = np.sum(amino_acid_percent_all)
	amino_acid_percent_all = amino_acid_percent_all/normalization

	return amino_acid_percent_all







dictionary_secondary_structure = {'Helix': 0.0, 'Turn':0.0, 'Sheet':0.0}


def secondary_structure_percent(list_secondary_strucutre):
	secondary_structure_all = np.zeros(3)
	for i in range(len(list_secondary_strucutre)):
		analysed_seq = ProteinAnalysis(list_secondary_strucutre[i][0])
		secondary_structure_1 = np.array(list(analysed_seq.secondary_structure_fraction()))

		analysed_seq = ProteinAnalysis(list_secondary_strucutre[i][1])
		secondary_structure_2 = np.array(list(analysed_seq.secondary_structure_fraction()))

		secondary_structure_average = ((secondary_structure_1+secondary_structure_2)/2)*list_secondary_strucutre[i][8]
		secondary_structure_all = secondary_structure_all + secondary_structure_average


	normalization = np.sum(secondary_structure_all)
	secondary_structure_all = secondary_structure_all/normalization

	plt.bar(list(dictionary_secondary_structure.keys()), secondary_structure_all, color='g')
	plt.savefig(path + '\\annika_SECONDARY_STRUCTURE_CSM_dependencies.svg')
	plt.clf()





def position_weight_matrix(list_position_weight,name_title):

	
	
	def get_the_neighbours(stringi, little_position):
		string_to_be_returned = ""
		
		if little_position-1<0:
			string_to_be_returned = "GGR"
		elif little_position-1==0:
			string_to_be_returned = "GR" + stringi[0]
		elif little_position-2==0:
			string_to_be_returned = "R" + stringi[0] + stringi[1]
		else:
			string_to_be_returned = stringi[little_position-3] + stringi[little_position-2] + stringi[little_position-1]


		if little_position==len(stringi)-1:
			string_to_be_returned = string_to_be_returned + "---"
		elif little_position==len(stringi)-2:
			#can differentiate betweem peplib1, peplib2 and peplib3 
			if stringi[little_position]=='D' or stringi[little_position]=='E':
				string_to_be_returned =string_to_be_returned + stringi[little_position+1] + "GG"
			else:
				string_to_be_returned = string_to_be_returned + stringi[little_position+1] + "--"
		elif little_position==len(stringi)-3:
			#specially created for a peptide inn peplib1 but can also be used for peplib3
			if string_to_be_returned == "PHA" or stringi[little_position]=='E' or stringi[little_position]=='D':
				string_to_be_returned = string_to_be_returned + stringi[little_position+1] + stringi[little_position+2] + "G"
			else:
				string_to_be_returned = string_to_be_returned + stringi[little_position+1] + stringi[little_position+2] + "-"
		else:
			string_to_be_returned = string_to_be_returned + stringi[little_position+1] + stringi[little_position+2] + stringi[little_position+3]
		
		return string_to_be_returned

	for i in range(len(list_position_weight)):
		
		
		
		
		neighbour_amino_acids_1 = get_the_neighbours(list_position_weight[i][0],list_position_weight[i][9])
		try:
			if neighbour_amino_acids_1[0] in dictionary_of_aminoacids_reduced_1:
				dictionary_of_aminoacids_reduced_1[neighbour_amino_acids_1[0]] = dictionary_of_aminoacids_reduced_1[neighbour_amino_acids_1[0]] + list_position_weight[i][8]
			if neighbour_amino_acids_1[1] in dictionary_of_aminoacids_reduced_2:
				dictionary_of_aminoacids_reduced_2[neighbour_amino_acids_1[1]] = dictionary_of_aminoacids_reduced_2[neighbour_amino_acids_1[1]] + list_position_weight[i][8]
			if neighbour_amino_acids_1[2] in dictionary_of_aminoacids_reduced_3:
				dictionary_of_aminoacids_reduced_3[neighbour_amino_acids_1[2]] = dictionary_of_aminoacids_reduced_3[neighbour_amino_acids_1[2]] + list_position_weight[i][8]
			if neighbour_amino_acids_1[3] in dictionary_of_aminoacids_reduced_4:
				dictionary_of_aminoacids_reduced_4[neighbour_amino_acids_1[3]] = dictionary_of_aminoacids_reduced_4[neighbour_amino_acids_1[3]] + list_position_weight[i][8]
			if neighbour_amino_acids_1[4] in dictionary_of_aminoacids_reduced_5:
				dictionary_of_aminoacids_reduced_5[neighbour_amino_acids_1[4]] = dictionary_of_aminoacids_reduced_5[neighbour_amino_acids_1[4]] + list_position_weight[i][8]
			if neighbour_amino_acids_1[5] in dictionary_of_aminoacids_reduced_6:
				dictionary_of_aminoacids_reduced_6[neighbour_amino_acids_1[5]] = dictionary_of_aminoacids_reduced_6[neighbour_amino_acids_1[5]] + list_position_weight[i][8]
		except:
			print(dictionary_of_aminoacids_reduced_1[neighbour_amino_acids_1[0]] , list_position_weight[8])
		#analysed_seq = ProteinAnalysis(neighbour_amino_acids_1)
		#amino_acid_percent_1 = np.array(list(analysed_seq.get_amino_acids_percent().values()))
		#gap_percent_1 = 1-np.sum(amino_acid_percent_1)

		neighbour_amino_acids_2 = get_the_neighbours(list_position_weight[i][1],list_position_weight[i][10])
		try:
			if neighbour_amino_acids_2[0] in dictionary_of_aminoacids_reduced_1:
				dictionary_of_aminoacids_reduced_1[neighbour_amino_acids_2[0]] = dictionary_of_aminoacids_reduced_1[neighbour_amino_acids_2[0]] + list_position_weight[i][8]
			if neighbour_amino_acids_2[1] in dictionary_of_aminoacids_reduced_2:
				dictionary_of_aminoacids_reduced_2[neighbour_amino_acids_2[1]] = dictionary_of_aminoacids_reduced_2[neighbour_amino_acids_2[1]] + list_position_weight[i][8]
			if neighbour_amino_acids_2[2] in dictionary_of_aminoacids_reduced_3:
				dictionary_of_aminoacids_reduced_3[neighbour_amino_acids_2[2]] = dictionary_of_aminoacids_reduced_3[neighbour_amino_acids_2[2]] + list_position_weight[i][8]
			if neighbour_amino_acids_2[3] in dictionary_of_aminoacids_reduced_4:
				dictionary_of_aminoacids_reduced_4[neighbour_amino_acids_2[3]] = dictionary_of_aminoacids_reduced_4[neighbour_amino_acids_2[3]] + list_position_weight[i][8]
			if neighbour_amino_acids_2[4] in dictionary_of_aminoacids_reduced_5:
				dictionary_of_aminoacids_reduced_5[neighbour_amino_acids_2[4]] = dictionary_of_aminoacids_reduced_5[neighbour_amino_acids_2[4]] + list_position_weight[i][8]
			if neighbour_amino_acids_2[5] in dictionary_of_aminoacids_reduced_6:
				dictionary_of_aminoacids_reduced_6[neighbour_amino_acids_2[5]] = dictionary_of_aminoacids_reduced_6[neighbour_amino_acids_2[5]] + list_position_weight[i][8]
		except:
			print(dictionary_of_aminoacids_reduced_1[neighbour_amino_acids_2[0]] , list_position_weight[8])


	array_1 = np.array(list(dictionary_of_aminoacids_reduced_1.values()))
	normalizer = np.sum(array_1)
	array_1 = array_1 / normalizer
	if(np.sum(array_1)!=1.0):
		max_index_col = np.argmax(array_1, axis=0)
		array_1[max_index_col]=array_1[max_index_col]+(1.0-np.sum(array_1))

	array_2 = np.array(list(dictionary_of_aminoacids_reduced_2.values()))
	normalizer = np.sum(array_2)
	array_2 = array_2 / normalizer
	if(np.sum(array_2)!=1.0):
		max_index_col = np.argmax(array_2, axis=0)
		array_2[max_index_col]=array_2[max_index_col]+(1.0-np.sum(array_2))

	array_3 = np.array(list(dictionary_of_aminoacids_reduced_3.values()))
	normalizer = np.sum(array_3)
	array_3 = array_3 / normalizer
	if(np.sum(array_3)!=1.0):
		max_index_col = np.argmax(array_3, axis=0)
		array_3[max_index_col]=array_3[max_index_col]+(1.0-np.sum(array_3))

	array_4 = np.array(list(dictionary_of_aminoacids_reduced_4.values()))
	normalizer = np.sum(array_4)
	array_4 = array_4 / normalizer
	if(np.sum(array_4)!=1.0):
		max_index_col = np.argmax(array_4, axis=0)
		array_4[max_index_col]=array_4[max_index_col]+(1.0-np.sum(array_4))

	array_5 = np.array(list(dictionary_of_aminoacids_reduced_5.values()))
	normalizer = np.sum(array_5)
	array_5 = np.round(array_5 / normalizer,decimals=16)
	if(np.sum(array_5)!=1.0 ):
		max_index_col = np.argmax(array_5, axis=0)
		array_5[max_index_col]=array_5[max_index_col]+round(1.0-np.sum(array_5),16)
		print(np.sum(array_5),round(1.0-np.sum(array_5),16))

	array_6 = np.array(list(dictionary_of_aminoacids_reduced_6.values()))
	normalizer = np.sum(array_6)
	array_6 = array_6 / normalizer
	if(np.sum(array_6)!=1.0):
		max_index_col = np.argmax(array_6, axis=0)
		array_6[max_index_col]=array_6[max_index_col]+(1.0-np.sum(array_6))

	print(np.sum(array_1),
		  np.sum(array_2),
		  np.sum(array_3),
		  np.sum(array_4),
		  np.sum(array_5),
		  np.sum(array_6))

	newArray = np.append([array_1], [array_2], axis = 0)
	newArray = np.append(newArray, [array_3], axis = 0)
	newArray = np.append(newArray, [array_4], axis = 0)
	newArray = np.append(newArray, [array_5], axis = 0)
	newArray = np.append(newArray, [array_6], axis = 0)
	
	print(newArray)

	pfm = pd.DataFrame(newArray)
	pwm = seqlogo.pfm2pwm(pfm, alphabet_type = "reduced AA",background=23, alphabet= "ACDEFGHIKLMNPQRSTVWYX*-")
	print(pwm)
	cpm = seqlogo.CompletePm(pfm, alphabet_type = "reduced AA",background=23, alphabet= "ACDEFGHIKLMNPQRSTVWYX*-")
	print(cpm)
	print(type(cpm))
	print(cpm.consensus)
	print(type(cpm.consensus))

	from Bio import SeqIO

	from Bio.SeqRecord import SeqRecord




	file_out= path +'\\neighbours_of_the_XL_binding_amino_acid_CSM_level_'+name_title+'.txt'

	with open(file_out, 'w') as f_out:
		f_out.write("The most frequent amino acid residues neighboring the binding amino acid are: ")
		f_out.write("\n")
		consensus = str(cpm.consensus)
		f_out.write("\n")
		f_out.write(consensus[0:3]+" ~binding amino acid~ "+consensus[3:6])
		f_out.write("\n")
		f_out.write("\n")
		f_out.write("Position frequency matrix of the closest neighbours to the binding amino acid from left (N-Terminus-direction) to right (C-Terminus-direction)")
		f_out.write("\n")
		f_out.write("Each row of the matrix represents a distinct position reported to the binding amino acid.")
		f_out.write("\n")
		f_out.write("\n")
		f_out.write(pfm.to_string(index=False,justify="left"))
		f_out.write("\n")
	
	return newArray
		



def histogram_maker(title, list_name_variables, matrix_of_values, left_barrier, right_barrier, steps, name_x_variable):
	bins = np.linspace(left_barrier,right_barrier,steps)

	#kwargs = dict(alpha=0.5, density=True)
	for i in range(len(list_name_variables)):
		plt.hist(matrix_of_values[i], bins,alpha= 0.6, label=list_name_variables[i],density=True)


	plt.legend(bbox_to_anchor = (1.25, 0.6))
	plt.xlabel(name_x_variable)
	plt.ylabel("Normalised numbers of CSMs")
	plt.savefig(path + '\\' + title + '.svg',bbox_inches="tight")
	plt.clf()

def histogram_maker_unweighted(title, list_name_variables, matrix_of_values, left_barrier, right_barrier, steps, name_x_variable):
	bins = np.linspace(left_barrier,right_barrier,steps)

	#kwargs = dict(alpha=0.5, density=True)
	for i in range(len(list_name_variables)):
		plt.hist(matrix_of_values[i], bins,alpha= 0.6, label=list_name_variables[i])


	plt.legend(bbox_to_anchor = (1.25, 0.6))
	plt.xlabel(name_x_variable)
	plt.ylabel("Number of crosslinks")
	plt.savefig(path + '\\' + title + '.svg',bbox_inches="tight")
	plt.clf()

def bar_plot(list_real,list_theory):

	r = np.arange(0,40,2)
	width = 0.6
	
	bar1=plt.bar(r, list_real)
	bar2=plt.bar(r+width, list_theory,alpha=0.6)

	plt.xlabel("Aminoacid")
	plt.ylabel('Frequency')
	plt.title("Frequency of the aminoacids in crosslinks - CSM level")
  
	plt.xticks(r+width,list(dictionary_of_aminoacids.keys()))
	plt.legend( (bar1, bar2), ('reality', 'theory'),bbox_to_anchor = (1.25, 0.6))
	plt.savefig(path + '\\_AA_distribution_CSM_level.svg',bbox_inches="tight")
	plt.clf()

	file_frequency = open(path + "\\frequency_amino_acids.csv", "w", newline='')
	writer = csv.writer(file_frequency)

	writer.writerow(["Amino acid","Reality","Theory"])

	for i in range(len(list_theory)):
		writer.writerow([list_one_letter_code[i],list_real[i],list_theory[i]])

	file_frequency.close()
		

	



gravy_values_real  = gravy_index(unique_crosslinks_true,False)
gravy_values_theoretical = gravy_index(list_theoretical_XL,False)

aromaticity_values_real  = aromaticity_index(unique_crosslinks_true,False)
aromaticity_values_theoretical = aromaticity_index(list_theoretical_XL,False)

isoelectric_point_values_real = isoelectric_point_index(unique_crosslinks_true,False)
isoelectric_point_values_theoretical = isoelectric_point_index(list_theoretical_XL,False)

mass_index_real = mass_index(unique_crosslinks_true,False)
mass_index_theoretical = mass_index(list_theoretical_XL,False)

#charge_at_ph_value_real = charge_at_ph_index(unique_crosslinks_true, value_of_the_pH,False)
#charge_at_ph_value_theoretical = charge_at_ph_index(list_theoretical_XL,value_of_the_pH,False)


histogram_maker("Gravy-index",["theory","reality"],[gravy_values_theoretical,gravy_values_real],min(gravy_values_theoretical),max(gravy_values_theoretical),150,"gravy-index")
histogram_maker("Aromaticity",["theory","reality"],[aromaticity_values_theoretical,aromaticity_values_real],min(aromaticity_values_theoretical),max(aromaticity_values_theoretical),50,"relative frequency of Phe+Trp+Tyr")
histogram_maker("isoelectric point",["theory","reality"],[isoelectric_point_values_theoretical,isoelectric_point_values_real],min(isoelectric_point_values_theoretical),max(isoelectric_point_values_theoretical),90,"value pI")
histogram_maker("molecular-weight",["theory","reality"],[mass_index_theoretical,mass_index_real],min(mass_index_theoretical),max(mass_index_theoretical),200,"molecular-weight")
#histogram_maker("charge-at-pH",["theory","reality"],[charge_at_ph_value_theoretical,charge_at_ph_value_real],min(charge_at_ph_value_theoretical),max(charge_at_ph_value_theoretical),max(charge_at_ph_value_theoretical)-min(charge_at_ph_value_theoretical)+1,"charge-at-pH")




file_real = open(path + "\\values_real.csv", "w",newline='')
writer = csv.writer(file_real)


def writing_values(list_1,list_2,list_3,list_4,list_5):
	
	writer.writerow(["Sequence 1", "Sequence 2", "Gravy value", "Aromaticity fraction", "Isoelectric-point","Molecular-Weight(g/mol)","RT [min]"])

	little_range = len(list_1)
	a = 0
	for i in range(little_range):
		for j in range(list_1[i][8]):
			writer.writerow([list_1[i][0],list_1[i][1],list_2[a],list_3[a],list_4[a],list_5[a],list_1[i][2]])
			a = a+1


writing_values(unique_crosslinks_true,gravy_values_real,aromaticity_values_real,isoelectric_point_values_real,mass_index_real)

file_real.close()
file_theoretical = open(path + "\\values_theory.csv", "w", newline='')
writer = csv.writer(file_theoretical)


writing_values(list_theoretical_XL,gravy_values_theoretical,aromaticity_values_theoretical,isoelectric_point_values_theoretical,mass_index_theoretical)

file_theoretical.close()





#gravy_index(unique_crosslinks,True)
#isoelectric_point_index(unique_crosslinks,True)
#aromaticity_index(unique_crosslinks,True)
#charge_at_ph_index(unique_crosslinks, value_of_the_pH,True)


bar_plot(get_amino_acids_percent(unique_crosslinks_true),get_amino_acids_percent(list_theoretical_XL))
#secondary_structure_percent(unique_crosslinks)	

A= position_weight_matrix(unique_crosslinks_true,"unique_crosslinks")
B= position_weight_matrix(list_theoretical_XL,"theoretical_crosslinks")

#just to be used in case Ghostscript is installed and on the path
'''
ppm = seqlogo.Ppm(A, alphabet_type = "reduced AA",background=23, alphabet= "ACDEFGHIKLMNPQRSTVWYX*-")
seqlogo.seqlogo(ppm, ic_scale = False, format = 'pdf', size = 'large', color_scheme='monochrome',filename=path+'//logo_reality.pdf')

ppm = seqlogo.Ppm(B, alphabet_type = "reduced AA",background=23, alphabet= "ACDEFGHIKLMNPQRSTVWYX*-")
seqlogo.seqlogo(ppm, ic_scale = False, format = 'pdf', size = 'large', color_scheme='monochrome',filename=path+'//logo_theory.pdf')

'''


retention_time_temporary = []

for i in range(len(unique_crosslinks_true)):
	retention_time_temporary.append(int(unique_crosslinks_true[i][2]))




plt.scatter(retention_time_temporary, gravy_values_real, s=10)
plt.xlabel("RT [min]")
plt.ylabel('Gravy value')
plt.savefig(path + '\\CSM_rt_vs_gravy.svg',bbox_inches="tight")
plt.clf()

plt.scatter(retention_time_temporary, mass_index_real, s=10)
plt.xlabel("RT [min]")
plt.ylabel('Mass [g/mol]')
plt.savefig(path + '\\CSM_rt_vs_mass.svg',bbox_inches="tight")
plt.clf()

plt.scatter(retention_time_temporary, isoelectric_point_values_real, s=10)
plt.xlabel("RT [min]")
plt.ylabel('pI value')
plt.savefig(path + '\\CSM_rt_vs_pI.svg',bbox_inches="tight")
plt.clf()

plt.scatter(retention_time_temporary, aromaticity_values_real, s=10)
plt.xlabel("RT [min]")
plt.ylabel('Aromaticity value')
plt.savefig(path + '\\CSM_rt_vs_AROMATIC.svg',bbox_inches="tight")
plt.clf()


charge_values = charge_at_ph_index(unique_crosslinks_true,3,False)
plt.scatter(retention_time_temporary, charge_values, s=10)
plt.xlabel("RT [min]")
plt.ylabel('charge value')
plt.savefig(path + '\\CSM_rt_vs_charge.svg',bbox_inches="tight")
plt.clf()


#here the duplicates will be eliminated
for i in range(len(unique_crosslinks_true)):
	unique_crosslinks_true[i][2]=1
unique_crosslinks_true = list(map(list,unique(map(tuple,unique_crosslinks_true))))

gravy_values_real  = gravy_index(unique_crosslinks_true,False)
gravy_values_theoretical = gravy_index(list_theoretical_XL,False)

aromaticity_values_real  = aromaticity_index(unique_crosslinks_true,False)
aromaticity_values_theoretical = aromaticity_index(list_theoretical_XL,False)

isoelectric_point_values_real = isoelectric_point_index(unique_crosslinks_true,False)
isoelectric_point_values_theoretical = isoelectric_point_index(list_theoretical_XL,False)

mass_index_real = mass_index(unique_crosslinks_true,False)
mass_index_theoretical = mass_index(list_theoretical_XL,False)

#charge_at_ph_value_real = charge_at_ph_index(unique_crosslinks_true, value_of_the_pH,False)
#charge_at_ph_value_theoretical = charge_at_ph_index(list_theoretical_XL,value_of_the_pH,False)




histogram_maker_unweighted("Hydrophobicity_XL_level_areas_not_normalised",["theory","reality"],[gravy_values_theoretical,gravy_values_real],min(gravy_values_theoretical),max(gravy_values_theoretical),150,"gravy-index")
histogram_maker_unweighted("Aromaticity_XL_level_areas_not_normalised",["theory","reality"],[aromaticity_values_theoretical,aromaticity_values_real],min(aromaticity_values_theoretical),max(aromaticity_values_theoretical),50,"relative frequency of Phe+Trp+Tyr")
histogram_maker_unweighted("Isoelectric_point_XL_level_areas_not_normalised_weighted_to_frequency_of_KRHDE",["theory","reality"],[isoelectric_point_values_theoretical,isoelectric_point_values_real],min(isoelectric_point_values_theoretical),max(isoelectric_point_values_theoretical),90,"value pI")
histogram_maker_unweighted("Molecular_weight_XL_level_areas_not_normalised",["theory","reality"],[mass_index_theoretical,mass_index_real],min(mass_index_theoretical),max(mass_index_theoretical),200,"molecular-weight")
#histogram_maker_unweighted("Unweighted_charge-at-pH",["theory","reality"],[charge_at_ph_value_theoretical,charge_at_ph_value_real],min(charge_at_ph_value_theoretical),max(charge_at_ph_value_theoretical),max(charge_at_ph_value_theoretical)-min(charge_at_ph_value_theoretical)+1,"charge-at-pH")
