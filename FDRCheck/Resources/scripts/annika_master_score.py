#MS Annika
import csv
from numpy.lib.function_base import append
import xlrd                              #Import xlrd package
import argparse
import sys
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True



parser = argparse.ArgumentParser()
parser.add_argument("input_file_name")
parser.add_argument("support_file_name")
parser.add_argument("output_file_name")


parser.add_argument("-sA", "--sequence_A", type=str,
                    help="change the the name of the header for the Sequence A. Please introduce quotation marks, especially if the name contains whitespaces!", default="Sequence A")
parser.add_argument("-sB", "--sequence_B", type=str,
                    help="change the the name of the header for the Sequence A. Please introduce quotation marks, especially if the name contains whitespaces!", default="Sequence B")
parser.add_argument("-naprotA","--name_of_protein_A", type=str,
                    help="change the the name of the header for the Protein-Name-A. Please introduce quotation marks, especially if the name contains whitespaces!", default="Accession A")
parser.add_argument("-naprotB","--name_of_protein_B", type=str,
                    help="change the the name of the header for the Protein-Name-A. Please introduce quotation marks, especially if the name contains whitespaces!", default="Accession B")
parser.add_argument("-bscr", "--best_score", type=str,
                    help="change the the name of the header for the Best CSM-score of the crosslink. Please introduce quotation marks, especially if the name contains whitespaces!", default="Best CSM Score")
parser.add_argument("-pospA", "--position_in_protein_A",
                    help="change the the name of the header for the position of the binding aminoacid in the protein A. Please introduce quotation marks, especially if the name contains whitespaces!",default="In protein A")
parser.add_argument("-pospB", "--position_in_protein_B",
                    help="change the the name of the header for the position of the binding aminoacid in the protein B. Please introduce quotation marks, especially if the name contains whitespaces!",default="In protein B")             
args = parser.parse_args()

#list_crosslinks_connect_acid = ["D","E"]
#list_crosslinks_connect_lys = ["K","Y","T","S"]


# open the sheetspreadfile and the respective sheet
#groups_support_file = input("please introduce the name of the support file: ")
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
for i in range(1,number_groups+1):
    for j in range(1,peptides_per_group[i-1]+1):
        list_of_peptides_per_group.append(worksheet_groups.cell(((i-1)*(peptides_per_group[i-1]+1))+j, 0).value)
    a = list_of_peptides_per_group
    list_of_groups.append(a)
    list_of_peptides_per_group = []


#name_file_annika= input("please copy-paste the whole name of the document with the xlsx extension as well:")
name_file_annika = args.input_file_name

import os

name_of_the_image = os.path.splitext(name_file_annika)[0]

counter=0

loc = name_file_annika         #Giving the location of the file 

wb = xlrd.open_workbook(loc)                    #opening & reading the excel file
s1 = wb.sheet_by_index(0)                     #extracting the worksheet
s1.cell_value(0,0)                            #initializing cell from the excel file mentioned through the cell position
  

ws = wb.sheet_by_index(0)




header_name_seq_A = args.sequence_A
header_name_seq_B = args.sequence_B
header_name_protein_A = args.name_of_protein_A
header_name_protein_B = args.name_of_protein_B
header_position_AminoAcid_A = args.position_in_protein_A
header_position_AminoAcid_B = args.position_in_protein_B
header_score = args.best_score


ws = wb.sheet_by_index(0)

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

character_to_delete = ["{","[","]","}","X","J"]
unique_crosslinks = []
list_of_scores_xlinkx = []


for i in range(1,s1.nrows):
	try:
		string1 = ws.cell(i,column_pos_Sequence_A).value.replace("[","").replace("]","")
		string2 = ws.cell(i,column_pos_Sequence_B).value.replace("[","").replace("]","")
		protein_name_1 = ws.cell(i,column_pos_Protein_A).value
		protein_name_2 = ws.cell(i,column_pos_Protein_B).value
		final_position_1 = int(ws.cell(i,column_pos_Position_AA_A).value)
		final_position_2 = int(ws.cell(i,column_pos_Position_AA_B).value)
		score = float(ws.cell(i,column_pos_score).value)
	except:
		string1 = ws.cell(i,column_pos_Sequence_A).value.replace("[","").replace("]","")
		string2 = ws.cell(i,column_pos_Sequence_B).value.replace("[","").replace("]","")

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
		final_position_1 = int(read_until_find_undecided(str(ws.cell(i,column_pos_Position_AA_A).value).replace(".0","")))
		final_position_2 = int(read_until_find_undecided(str(ws.cell(i,column_pos_Position_AA_B).value).replace(".0","")))
		score = float(ws.cell(i,column_pos_score).value)

	unique_crosslinks.append([string1,string2,score,protein_name_1,protein_name_2,final_position_1,final_position_2])
	list_of_scores_xlinkx.append(score)



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


            

    return  example_list;

unique_crosslinks = order_alphabetically(unique_crosslinks)

from toolz import unique
unique_crosslinks = list(map(list,unique(map(tuple,unique_crosslinks))))


list_of_scores_xlinkx = list(set(list_of_scores_xlinkx))
list_of_scores_xlinkx.sort()

#erase afterwards
#fdr_cutoff_value = input("please type in the fdr cutoff value (ex:0.05): ")
fdr_cutoff_value = "X"
temp1 = []
temp2 = []

def fdr_diagamm(list_crosslinks):
    temp1 = []
    temp2 = []

    import xlsxwriter
    workbook = xlsxwriter.Workbook(os.path.splitext(args.output_file_name)[0]+"_venn_input.xlsx")

    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    worksheet.write(0,0, "Results")
    worksheet.write(2,0, "total number of CSMs:")
    worksheet.write(3,0, "total number of unique XLs:")
    worksheet.write(4,0, "all True crosslinks: ")
    worksheet.write(5,0, "homeotypic crosslinks:")
    worksheet.write(6,0, "non-homeotypic crosslinks:")
    worksheet.write(7,0, "false crosslinks")

    worksheet.write(9,0, "all crosslinks")
    worksheet.write(9,1, "true crosslinks")
    worksheet.write(9,2, "false crosslinks")

    worksheet.write(2,3,"number of XLs post-score cut-off 5%:")
    worksheet.write(3,3,"number of XLs post-score cut-off 1%:")


    worksheet.set_column(0,0,30)

    

    



    to_be_ploted_x = []
    to_be_ploted_y = []
    correct_no_homo_XL = []
    homo_XL = []
    false_XL = []


    # open the file in the write mode
    f = open((args.output_file_name), 'w', newline='')

    #define the header
    header_csv = ["Sequence A", "Sequence B","Accession A","Accession B","Position in protein A","Position in protein B","Score crosslink","Within same group"]

    # create the csv writer
    writer = csv.writer(f)
    writer.writerow(header_csv)

    list_true_XL_csv = []
    list_false_XL_csv = []


    import matplotlib.pyplot as plt


    for i in range(len(list_of_scores_xlinkx)):
        all_crosslinks = 0
        correct_crosslinks = 0
        homeotypic = 0
        for j in range(len(unique_crosslinks)):
            if unique_crosslinks[j][2]>=list_of_scores_xlinkx[i]:
                all_crosslinks = all_crosslinks +1
                temp1.append(list([unique_crosslinks[j][0],unique_crosslinks[j][1],
                                   unique_crosslinks[j][3],unique_crosslinks[j][4],
                                   str(unique_crosslinks[j][5]),str(unique_crosslinks[j][6]),str("score_" + str(unique_crosslinks[j][2]))]))
                found = False
                k = 0
                while(k<number_groups and found == False):
                    l = 0
                    while(l<peptides_per_group[k] and found == False):
                        if unique_crosslinks[j][0] == list_of_groups[k][l] or unique_crosslinks[j][0] in list_of_groups[k][l] :
                            m = 0
                            while(m<peptides_per_group[k] and found== False):
                                if (unique_crosslinks[j][1]== list_of_groups[k][m] or unique_crosslinks[j][1] in list_of_groups[k][m]):
                                    found = True
                                    correct_crosslinks = correct_crosslinks +1
                                    temp2.append(list([unique_crosslinks[j][0],unique_crosslinks[j][1],
                                                       unique_crosslinks[j][3],unique_crosslinks[j][4],
                                                       str(unique_crosslinks[j][5]),str(unique_crosslinks[j][6]),str("score_" + str(unique_crosslinks[j][2]))]))
                                    if i==0:
                                        list_true_XL_csv.append([unique_crosslinks[j][0],unique_crosslinks[j][1],
                                                          unique_crosslinks[j][3],unique_crosslinks[j][4],
                                                          str(unique_crosslinks[j][5]),str(unique_crosslinks[j][6]),unique_crosslinks[j][2],"TRUE"])
                                    if unique_crosslinks[j][0] == unique_crosslinks[j][1]:
                                        homeotypic = homeotypic+1
                                else:
                                    m = m+1
                            
                        l = l+1
                    k = k+1
                if i==0 and found == False:
                    list_false_XL_csv.append([unique_crosslinks[j][0],unique_crosslinks[j][1],
                                                          unique_crosslinks[j][3],unique_crosslinks[j][4],
                                                          str(unique_crosslinks[j][5]),str(unique_crosslinks[j][6]),unique_crosslinks[j][2],"FALSE"])

                
        if i == 0:
            temp11 = []
            temp22 = []

            for m in range(len(temp1)):
                temp1[m].sort()
                temp1[m]=str(temp1[m])
                temp11.append(str(temp1[m]))
                worksheet.write(11+m,0,str(temp1[m]))


            for m in range(len(temp2)):
                temp2[m].sort()
                temp2[m]=str(temp2[m])
                temp22.append(str(temp2[m]))
                worksheet.write(11+m,1,str(temp2[m]))

            temp3=list(set(temp11)-set(temp22)) 
            for m in range(len(temp3)):
                worksheet.write(11+m,2,str(temp3[m]))
            
            list_of_the_correct_crosslinks = set(temp2)
            list_of_the_false_crosslinks = set(set(temp11)-set(temp22))
            list_of_all_crosslinks = set(temp1)



        #print(all_crosslinks-correct_crosslinks, all_crosslinks)
        to_be_ploted_x.append(list_of_scores_xlinkx[i])
        to_be_ploted_y.append((all_crosslinks-correct_crosslinks)/all_crosslinks)
        correct_no_homo_XL.append(correct_crosslinks-homeotypic)
        homo_XL.append(homeotypic)
        false_XL.append(all_crosslinks-correct_crosslinks)
        
    
    plt.plot(to_be_ploted_x,to_be_ploted_y)

    plt.title('Real FDR dependent of the score')
    plt.xlabel('Score')
    plt.ylabel('FDR')
    alarm_005 = False
    alarm_001 = False

    
    try:
        worksheet.write(2,1,"not calculated")
        worksheet.write(3,1,correct_no_homo_XL[0]+homo_XL[0]+false_XL[0])
        worksheet.write(4,1,correct_no_homo_XL[0]+homo_XL[0])
        worksheet.write(5,1,homo_XL[0])
        worksheet.write(6,1,correct_no_homo_XL[0])
        worksheet.write(7,1,false_XL[0])
    except:
        print("ATTENZIONE")
        print("ATTENZIONE")

    bar_graph = ["real FDR"+" " +str(float("{0:.1f}".format((false_XL[0]/(correct_no_homo_XL[0]+homo_XL[0]+false_XL[0]))*100)))+"%"]
    
    gold = [correct_no_homo_XL[0]]
    silver = [homo_XL[0]]
    bronze = [false_XL[0]]


    plt.scatter(to_be_ploted_x[0],to_be_ploted_y[0])
    plt.annotate((to_be_ploted_x[0],float("{0:.3f}".format(to_be_ploted_y[0]))),(to_be_ploted_x[0],to_be_ploted_y[0]))
    if to_be_ploted_y[0]>0.05:
        for i in range(len(to_be_ploted_x)):
            if to_be_ploted_y[i]<=0.05 and alarm_005 == False:
                plt.scatter(to_be_ploted_x[i],to_be_ploted_y[i])
                plt.annotate((to_be_ploted_x[i],float("{0:.3f}".format(to_be_ploted_y[i]))),(to_be_ploted_x[i],to_be_ploted_y[i]))
                alarm_005 = True
                worksheet.write(2,4,correct_no_homo_XL[i]+homo_XL[i]+false_XL[i])
                bar_graph.append("FDR 5%")
                gold.append(correct_no_homo_XL[i])
                silver.append(homo_XL[i])
                bronze.append(false_XL[i])
                if to_be_ploted_y[i]<=0.01:
                    alarm_001 = True
                    worksheet.write(3,4,correct_no_homo_XL[i]+homo_XL[i]+false_XL[i])
                    bar_graph[1] = "FDR 1%"
                    #gold.append(correct_no_homo_XL[i])
                    #silver.append(homo_XL[i])
                    #bronze.append(false_XL[i])
            if to_be_ploted_y[i]<=0.01 and alarm_001 == False:
                plt.scatter(to_be_ploted_x[i],to_be_ploted_y[i])
                plt.annotate((to_be_ploted_x[i],float("{0:.3f}".format(to_be_ploted_y[i]))),(to_be_ploted_x[i],to_be_ploted_y[i]))
                alarm_001 = True
                worksheet.write(3,4,correct_no_homo_XL[i]+homo_XL[i]+false_XL[i])
                bar_graph.append("FDR 1%")
                gold.append(correct_no_homo_XL[i])
                silver.append(homo_XL[i])
                bronze.append(false_XL[i])
    elif to_be_ploted_y[0]<=0.05 and to_be_ploted_y[0]>0.01:
        for i in range(len(to_be_ploted_x)):
            if to_be_ploted_y[i]<=0.01 and alarm_001 == False:
                plt.scatter(to_be_ploted_x[i],to_be_ploted_y[i])
                plt.annotate((to_be_ploted_x[i],float("{0:.3f}".format(to_be_ploted_y[i]))),(to_be_ploted_x[i],to_be_ploted_y[i]))
                alarm_001 = True
                worksheet.write(3,4,correct_no_homo_XL[i]+homo_XL[i]+false_XL[i])
                bar_graph.append("FDR 1%")
                gold.append(correct_no_homo_XL[i])
                silver.append(homo_XL[i])
                bronze.append(false_XL[i])

    workbook.close()  
 #
 # #
 # #
 # #
 # #
 # #
 # #
 #    
    plt.savefig(os.path.splitext(args.output_file_name)[0]+"_Annika_ScorevsFDR.svg")
    plt.clf()

    import numpy as np
    
    b_bronze = list (np.add(gold, silver))

    plt.bar(bar_graph,gold,0.3,label="correct XL",color="green")
    plt.bar(bar_graph,silver,0.3,bottom=gold, label="homeotypic",color="cyan")
    plt.bar(bar_graph,bronze,0.3,bottom=b_bronze, label="false",color="red")
    
    plt.xlabel("FDR")
    plt.ylabel("Number of crosslinks")
    plt.title("Type of crosslinks with the FDRCUTOFF="+ fdr_cutoff_value)
    plt.legend()
    plt.savefig(os.path.splitext(args.output_file_name)[0]+"_Annika_numberXLs.svg")

    plt.clf()
    plt.xlabel("Score")
    plt.ylabel("Number of crosslinks")
    plt.stackplot(list_of_scores_xlinkx,correct_no_homo_XL,homo_XL,false_XL,labels=["correct","correct homeotypic","false"], colors=["green","cyan","red"])
    plt.legend()
    plt.savefig(os.path.splitext(args.output_file_name)[0]+"_Annika_ScorevsNumberXLs.svg")
#
#
#
#
#
##

    writer.writerows(list_true_XL_csv)
    writer.writerows(list_false_XL_csv)
    f.close()

fdr_diagamm(unique_crosslinks)