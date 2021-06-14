from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
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
'''
my_seq = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
analysed_seq = ProteinAnalysis(my_seq)
mass = analysed_seq.molecular_weight()
gravy_value = analysed_seq.gravy()
aromaticity_value = analysed_seq.aromaticity()
instability_value = analysed_seq.instability_index()
flexibility_value = analysed_seq.flexibility()
isoelectric_point_value = analysed_seq.isoelectric_point()
secondary_structure_fraction_dictionary = analysed_seq.secondary_structure_fraction()
charge_at_pH_value = analysed_seq.charge_at_pH(1)
amino_acid_percent = analysed_seq.get_amino_acids_percent()


print("analysed_seq.count_amino_acids()")
print(analysed_seq.count_amino_acids())
print("mass")
print(mass)
print("gravy_value")
print(gravy_value)
print("aromaticity_value")
print(aromaticity_value)
print("instability_value")
print(instability_value)
print("flexibility_value")
print(flexibility_value)
print("isoelectric_point_value")
print(isoelectric_point_value)
print("analysed_seq.secondary_structure_fraction()")
print(secondary_structure_fraction_dictionary)
print("charge_at_pH_value")
print(charge_at_pH_value)
print("amino_acid_percent")
print(amino_acid_percent)


dictionary_of_aminoacids = {'A':0.0, 'C':0.0, 'D':0.0,
							'E':0.0, 'F':0.0, 'G':0.0,
							'H':0.0, 'I':0.0, 'K':0.0,
							'L':0.0, 'M':0.0, 'N':0.0,
							'P':0.0, 'Q':0.0, 'R':0.0,
							'S':0.0, 'T':0.0, 'V':0.0,
							'W':0.0, 'Y':0.0}



average_value_of_XL = 0



DSSO_mass = 0
CDI_mass = 0
DSBU_mass = 0
DSBSO_mass_unhydrolysed = 0
DSBSO_mass_hydrolysed = 0
ADH_mass = 0
DHSO_mass = 0

'''
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
									'W':0.0, 'Y':0.0}
dictionary_of_aminoacids_reduced_2 = {'A':0.0, 'C':0.0, 'D':0.0,
									'E':0.0, 'F':0.0, 'G':0.0,
									'H':0.0, 'I':0.0, 'K':0.0,
									'L':0.0, 'M':0.0, 'N':0.0,
									'P':0.0, 'Q':0.0, 'R':0.0,
									'S':0.0, 'T':0.0, 'V':0.0,
									'W':0.0, 'Y':0.0}
dictionary_of_aminoacids_reduced_3 = {'A':0.0, 'C':0.0, 'D':0.0,
									'E':0.0, 'F':0.0, 'G':0.0,
									'H':0.0, 'I':0.0, 'K':0.0,
									'L':0.0, 'M':0.0, 'N':0.0,
									'P':0.0, 'Q':0.0, 'R':0.0,
									'S':0.0, 'T':0.0, 'V':0.0,
									'W':0.0, 'Y':0.0}
dictionary_of_aminoacids_reduced_4 = {'A':0.0, 'C':0.0, 'D':0.0,
									'E':0.0, 'F':0.0, 'G':0.0,
									'H':0.0, 'I':0.0, 'K':0.0,
									'L':0.0, 'M':0.0, 'N':0.0,
									'P':0.0, 'Q':0.0, 'R':0.0,
									'S':0.0, 'T':0.0, 'V':0.0,
									'W':0.0, 'Y':0.0}
dictionary_of_aminoacids_reduced_5 = {'A':0.0, 'C':0.0, 'D':0.0,
									'E':0.0, 'F':0.0, 'G':0.0,
									'H':0.0, 'I':0.0, 'K':0.0,
									'L':0.0, 'M':0.0, 'N':0.0,
									'P':0.0, 'Q':0.0, 'R':0.0,
									'S':0.0, 'T':0.0, 'V':0.0,
									'W':0.0, 'Y':0.0}
dictionary_of_aminoacids_reduced_6 = {'A':0.0, 'C':0.0, 'D':0.0,
									'E':0.0, 'F':0.0, 'G':0.0,
									'H':0.0, 'I':0.0, 'K':0.0,
									'L':0.0, 'M':0.0, 'N':0.0,
									'P':0.0, 'Q':0.0, 'R':0.0,
									'S':0.0, 'T':0.0, 'V':0.0,
									'W':0.0, 'Y':0.0}
name_file_annika= input("please copy-paste the whole name of the document with the xlsx extension as well:")

import os
name_of_the_image = os.path.splitext(name_file_annika)[0]


# detect the current working directory and print it
path = os.getcwd()
print ("The current working directory is %s" % path)

# define the name of the directory to be created
path = path + '\Results' + name_of_the_image
if os.path.isdir(path)==False:
	os.mkdir(path)


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



for i in range(1,s1.nrows):
	try:
		CSM_number = int(ws.cell(i,3).value)
		position_in_peptide_1 = ws.cell(i,5).value.find('[')
		position_in_peptide_2 = ws.cell(i,8).value.find('[')
		string1 = ws.cell(i,5).value.replace("[","").replace("]","")
		string2 = ws.cell(i,8).value.replace("[","").replace("]","")
		protein_name_1 = ws.cell(i,6).value
		protein_name_2 = ws.cell(i,9).value
		final_position_1 = int(ws.cell(i,14).value)
		final_position_2 = int(ws.cell(i,15).value)
		score = float(ws.cell(i,13).value)
	except:
		string1 = ws.cell(i,5).value.replace("[","").replace("]","")
		string2 = ws.cell(i,8).value.replace("[","").replace("]","")

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

		protein_name_1 = read_until_find_undecided(ws.cell(i,6).value)
		protein_name_2 = read_until_find_undecided(ws.cell(i,9).value)
		protein_name_1 = read_until_find_undecided(ws.cell(i,6).value)
		protein_name_2 = read_until_find_undecided(ws.cell(i,9).value)
		final_position_1 = int(read_until_find_undecided(str(ws.cell(i,14).value).replace(".0","")))
		final_position_2 = int(read_until_find_undecided(str(ws.cell(i,15).value).replace(".0","")))
		score = float(ws.cell(i,13).value)
		CSM_number = int(ws.cell(i,3).value)

	unique_crosslinks.append([string1,string2,score,protein_name_1,protein_name_2,final_position_1,final_position_2,CSM_number,CSM_number,position_in_peptide_1,position_in_peptide_2])
	list_of_scores_annika.append(score)
	list_of_areas_annika.append(CSM_number)



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
for i in range(len(unique_crosslinks)):
	print(unique_crosslinks[i])

def gravy_index(list_gravy_index):
	for i in range(len(list_gravy_index)):
		analysed_seq = ProteinAnalysis(list_gravy_index[i][0])
		gravy_value_1 = analysed_seq.gravy()
		analysed_seq = ProteinAnalysis(list_gravy_index[i][1])
		gravy_value_2 = analysed_seq.gravy()
		gravy_value_average_XL = (gravy_value_1 + gravy_value_2)/2
		if gravy_value_average_XL<=0:
			plt.scatter(gravy_value_average_XL,(math.log(list_gravy_index[i][8],10)), s=10, c='b', marker="s")
		else:
			plt.scatter(gravy_value_average_XL,(math.log(list_gravy_index[i][8],10)), s=10, c='r', marker="s")

	plt.savefig(path + '\\' + name_of_the_image + 'annika_GRAVY_INDEX.png')
	plt.clf()

	list_for_histogram = []
	for i in range(len(list_gravy_index)):
		analysed_seq = ProteinAnalysis(list_gravy_index[i][0])
		gravy_value_1 = analysed_seq.gravy()
		analysed_seq = ProteinAnalysis(list_gravy_index[i][1])
		gravy_value_2 = analysed_seq.gravy()
		gravy_value_average_XL = (gravy_value_1 + gravy_value_2)/2
		#for i in range(list_gravy_index[i][8]):
		list_for_histogram.append(gravy_value_average_XL)

	bins = np.linspace(-3.5, 3.5, 100)

	#kwargs = dict(alpha=0.5, density=True)
	plt.hist(list_for_histogram, bins, label='reality')
	plt.legend(loc='upper right')

	name_file_annika_theorie= input("please copy-paste the whole name of the document with the xlsx extension as well:")

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
				list_theoretical_XL.append([ws.cell(pivot_theoretical,0).value,ws.cell(j,0).value,int(ws.cell(pivot_theoretical,1).value),int(ws.cell(j,1).value)])
				print(ws.cell(pivot_theoretical,0).value,ws.cell(j,0).value,int(ws.cell(pivot_theoretical,1).value),int(ws.cell(j,1).value))
		pivot_theoretical=pivot_local+1
		if pivot_local!=s1.nrows:
			pivot_local = pivot_local +1



	from toolz import unique
	list_theoretical_XL = list(map(list,unique(map(tuple,list_theoretical_XL))))
	list_theoretical_XL_for_hist = []
	for i in range(len(list_theoretical_XL)):
		print(list_theoretical_XL[i])
		analysed_seq = ProteinAnalysis(list_theoretical_XL[i][0])
		gravy_value_1 = analysed_seq.gravy()
		analysed_seq = ProteinAnalysis(list_theoretical_XL[i][1])
		gravy_value_2 = analysed_seq.gravy()
		gravy_value_average_XL = (gravy_value_1 + gravy_value_2)/2
		list_theoretical_XL_for_hist.append(gravy_value_average_XL)
	plt.hist(list_theoretical_XL_for_hist, bins,alpha =0.2, label='theorie')
	plt.legend(loc='upper right')
	

	plt.show()


	

gravy_index(unique_crosslinks)

def isoelectric_point_index(list_isoelectric_point):
	for i in range(len(list_isoelectric_point)):
		analysed_seq= ProteinAnalysis(list_isoelectric_point[i][0])
		isoelectric_value_1 = analysed_seq.isoelectric_point()
		analysed_seq= ProteinAnalysis(list_isoelectric_point[i][1])
		isoelectric_value_2 = analysed_seq.isoelectric_point()
		isoelectric_value_average = (isoelectric_value_1+isoelectric_value_2)/2
		
		plt.scatter(isoelectric_value_average,(math.log(list_isoelectric_point[i][8],10)), s=10, c='b', marker="s")

	plt.savefig(path + '\\' + name_of_the_image + 'annika_ISOELECTRIC_POINT.png')
	plt.clf()

isoelectric_point_index(unique_crosslinks)
def charge_at_ph_index(list_charge_at_pH,value_of_pH):
	dict_charge = {}
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
		charge_1 = round(analysed_seq.charge_at_pH(value_of_pH))

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
		charge_2 = round(analysed_seq.charge_at_pH(value_of_pH))

		if str(charge_1+charge_2) in dict_charge.keys():
			dict_charge[str(charge_1+charge_2)] = dict_charge[str(charge_1+charge_2)] + list_charge_at_pH[i][8]
		else:
			dict_charge[str(charge_1+charge_2)] = list_charge_at_pH[i][8]
			
	dictionary_items = dict_charge.items()
	sorted_items = sorted(dictionary_items)
	x_values = []
	y_values = []
	for i in range(len(sorted_items)):
		x_values.append(sorted_items[i][0])
		y_values.append(sorted_items[i][1])
	
	plt.bar(x_values,y_values, color='g')
	plt.savefig(path + '\\' + name_of_the_image + 'annika_charge_at_pH_CSM_dependencies.png')
	plt.clf()

value_of_the_pH = float(input("The value of the pH: "))

charge_at_ph_index(unique_crosslinks, value_of_the_pH)

def aromaticity_index(list_aromaticity):
	for i in range (len(list_aromaticity)):
		analysed_seq= ProteinAnalysis(list_aromaticity[i][0])
		aromaticity_value_1 = analysed_seq.aromaticity()
		analysed_seq= ProteinAnalysis(list_aromaticity[i][1])
		aromaticity_value_2 = analysed_seq.aromaticity()
		aromaticity_value_average = (aromaticity_value_1+aromaticity_value_2)/2
		
		plt.scatter(aromaticity_value_average,list_aromaticity[i][8], s=10, c='b', marker="s")

	plt.savefig(path + '\\' + name_of_the_image + 'annika_AROMATICITY_CSM_dependencies.png')
	plt.clf()

aromaticity_index(unique_crosslinks)


def get_amino_acids_percent(list_amino_acid_percent):
	amino_acid_percent_all = np.zeros(20)
	for i in range(len(list_amino_acid_percent)):
		analysed_seq = ProteinAnalysis(list_amino_acid_percent[i][0])
		amino_acid_percent_1 = np.array(list(analysed_seq.get_amino_acids_percent().values()))

		analysed_seq = ProteinAnalysis(list_amino_acid_percent[i][1])
		amino_acid_percent_2 = np.array(list(analysed_seq.get_amino_acids_percent().values()))

		amino_acid_percent_average  = ((amino_acid_percent_1 + amino_acid_percent_2)/2)*list_amino_acid_percent[i][8]
		amino_acid_percent_all = amino_acid_percent_all + amino_acid_percent_average
	
	normalization = np.sum(amino_acid_percent_all)
	amino_acid_percent_all = amino_acid_percent_all/normalization

	plt.bar(list(dictionary_of_aminoacids.keys()), amino_acid_percent_all, color='g')
	plt.savefig(path + '\\' + name_of_the_image + 'annika_AA_PERCENT_CSM_dependencies.png')
	plt.clf()



get_amino_acids_percent(unique_crosslinks)




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
	plt.savefig(path + '\\' + name_of_the_image + 'annika_SECONDARY_STRUCTURE_CSM_dependencies.png')
	plt.clf()

secondary_structure_percent(unique_crosslinks)



def position_weight_matrix(list_position_weight):

	
	
	def get_the_neighbours(stringi, little_position):
		string_to_be_returned = ""
		
		if little_position-1<0:
			string_to_be_returned = "---"
		elif little_position-1==0:
			string_to_be_returned = "--" + stringi[0]
		elif little_position-2==0:
			string_to_be_returned = "-" + stringi[0] + stringi[1]
		else:
			string_to_be_returned = stringi[little_position-3] + stringi[little_position-2] + stringi[little_position-1]


		if little_position==len(stringi)-1:
			string_to_be_returned = string_to_be_returned + "---"
		elif little_position==len(stringi)-2:
			string_to_be_returned = string_to_be_returned + stringi[little_position+1] + "--"
		elif little_position==len(stringi)-3:
			string_to_be_returned = string_to_be_returned + stringi[little_position+1] + stringi[little_position+2] + "-"
		else:
			string_to_be_returned = string_to_be_returned + stringi[little_position+1] + stringi[little_position+2] + stringi[little_position+3]
		
		'''kmer_3_1 = kmer_3_1 + string_to_be_returned[0] + string_to_be_returned[3]
		kmer_3_2 = kmer_3_2 + string_to_be_returned[1] + string_to_be_returned[4]
		kmer_3_3 = kmer_3_3 + string_to_be_returned[2] + string_to_be_returned[5]

		kmer_6_1 = kmer_6_1 + string_to_be_returned[0]
		kmer_6_2 = kmer_6_2 + string_to_be_returned[1]
		kmer_6_3 = kmer_6_3 + string_to_be_returned[2]
		kmer_6_4 = kmer_6_4 + string_to_be_returned[3]
		kmer_6_5 = kmer_6_5 + string_to_be_returned[4]
		kmer_6_6 = kmer_6_6 + string_to_be_returned[5]'''
		
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
		#analysed_seq = ProteinAnalysis(neighbour_amino_acids_2)
		#amino_acid_percent_2 = np.array(list(analysed_seq.get_amino_acids_percent().values()))
		#gap_percent_2 = np.sum(amino_acid_percent_2)

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
	pwm = seqlogo.pfm2pwm(pfm, alphabet_type = "AA", background= 20, alphabet= "ACDEFGHIKLMNPQRSTVWY")
	print(pwm)
	cpm = seqlogo.CompletePm(pfm, alphabet_type = "AA", background= 20, alphabet= "ACDEFGHIKLMNPQRSTVWY")
	print(cpm)
	print(cpm.consensus)
	original= seqlogo.seqlogo(cpm, ic_scale = False, format = 'png', size = 'medium')



	'''analysed_seq = ProteinAnalysis(kmer_3_1)
	amino_acid_percent_3_1 = np.array(list(analysed_seq.get_amino_acids_percent().values()))
	gap_percent_3_1 = 1-np.sum(amino_acid_percent_3_1)
	amino_acid_percent_3_1 = np.append(amino_acid_percent_3_1,[0,0,gap_percent_3_1])

	analysed_seq = ProteinAnalysis(kmer_3_2)
	amino_acid_percent_3_2 = np.array(list(analysed_seq.get_amino_acids_percent().values()))
	gap_percent_3_2 = 1-np.sum(amino_acid_percent_3_2)
	amino_acid_percent_3_2 = np.append(amino_acid_percent_3_2,[0,0,gap_percent_3_2])

	analysed_seq = ProteinAnalysis(kmer_3_3)
	amino_acid_percent_3_3 = np.array(list(analysed_seq.get_amino_acids_percent().values()))
	gap_percent_3_3 = 1-np.sum(amino_acid_percent_3_3)
	amino_acid_percent_3_3 = np.append(amino_acid_percent_3_3,[0,0,gap_percent_3_3])


	analysed_seq = ProteinAnalysis(kmer_6_1)
	amino_acid_percent_6_1 = np.array(list(analysed_seq.get_amino_acids_percent().values()))
	gap_percent_6_1 = 1-np.sum(amino_acid_percent_6_1)
	amino_acid_percent_6_1 = np.append(amino_acid_percent_6_1,[0,0,gap_percent_6_1])

	analysed_seq = ProteinAnalysis(kmer_6_2)
	amino_acid_percent_6_2 = np.array(list(analysed_seq.get_amino_acids_percent().values()))
	gap_percent_6_2 = 1-np.sum(amino_acid_percent_6_2)
	amino_acid_percent_6_2 = np.append(amino_acid_percent_6_2,[0,0,gap_percent_6_2])

	analysed_seq = ProteinAnalysis(kmer_6_3)
	amino_acid_percent_6_3 = np.array(list(analysed_seq.get_amino_acids_percent().values()))
	gap_percent_6_3 = 1-np.sum(amino_acid_percent_6_3)
	amino_acid_percent_6_3 = np.append(amino_acid_percent_6_3,[0,0,gap_percent_6_3])

	analysed_seq = ProteinAnalysis(kmer_6_4)
	amino_acid_percent_6_4 = np.array(list(analysed_seq.get_amino_acids_percent().values()))
	gap_percent_6_4 = 1-np.sum(amino_acid_percent_6_4)
	amino_acid_percent_6_4 = np.append(amino_acid_percent_6_4,[0,0,gap_percent_6_4])

	analysed_seq = ProteinAnalysis(kmer_6_5)
	amino_acid_percent_6_5 = np.array(list(analysed_seq.get_amino_acids_percent().values()))
	gap_percent_6_5 = 1-np.sum(amino_acid_percent_6_5)
	amino_acid_percent_6_5 = np.append(amino_acid_percent_6_5,[0,0,gap_percent_6_5])

	analysed_seq = ProteinAnalysis(kmer_6_6)
	amino_acid_percent_6_6 = np.array(list(analysed_seq.get_amino_acids_percent().values()))
	gap_percent_6_6 = 1-np.sum(amino_acid_percent_6_6)
	amino_acid_percent_6_6 = np.append(amino_acid_percent_6_6,[0,0,gap_percent_6_6])'''

	

		



		
	
position_weight_matrix(unique_crosslinks)

		


