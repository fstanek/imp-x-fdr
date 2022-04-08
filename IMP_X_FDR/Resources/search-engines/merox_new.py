#MeroX
from operator import index
import xlsxwriter
import csv
import xlrd
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys


xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

support_file_name = sys.argv[1]
output_file_name = sys.argv[2]
is_grouped = len(sys.argv) > 3 and sys.argv[3] == 'true'

workbook_groups = xlrd.open_workbook(support_file_name, on_demand = True)
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

print(peptides_per_group)
print(len(peptides_per_group))


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


def read_crosslinks():
    input = sys.stdin

    if sys.argv[3] == 'DEBUG':
        input = open('C:/Users/stanek/source/repos/imp-x-fdr/IMP_X_FDR/Resources/search-engines/merox_input.csv', 'r')

    for line in input:
        values = line.strip().split('\t')
        values[2] = float(values[2])    # score
        values[5] = int(values[5])      # position 1
        values[6] = int(values[6])      # position 2
        yield values

unique_crosslinks = list(read_crosslinks())
print('{} crosslinks transferred.'.format(len(unique_crosslinks)))

fdr_cutoff_value = ''

list_of_scores = list(map(lambda c: c[2], unique_crosslinks))
list_of_scores.sort()

def fdr_diagamm(list_crosslinks):

    temp2 = []
    temp1 = []

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(os.path.splitext(output_file_name)[0] + '_venn_input.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0,0, "Results")
    worksheet.write(2,0, "Total number of CSMs:")
    worksheet.write(3,0, "Total number of unique XLs:")
    worksheet.write(4,0, "All True crosslinks: ")
    worksheet.write(5,0, "Homeotypic crosslinks:")
    worksheet.write(6,0, "Non-homeotypic crosslinks:")
    worksheet.write(7,0, "False crosslinks")

    worksheet.write(9,0, "All crosslinks")
    worksheet.write(9,1, "True crosslinks")
    worksheet.write(9,2, "False crosslinks")

    worksheet.write(2,3,"number of XLs post-score cut-off 5%:")
    worksheet.write(3,3,"numebr of XLs post-score cut-off 1%:")

    worksheet.set_column(0,0,40)
    worksheet.set_column(0,1,40)
    worksheet.set_column(0,2,40)
    worksheet.set_column(0,3,40)

    
    # open the file in the write mode
    f = open(output_file_name, 'w', newline='')

    #define the header
    header_csv = ["Sequence A", "Sequence B","Accession A","Accession B","Position in protein A","Position in protein B","Score crosslink","Within same group"]

    # create the csv writer
    writer = csv.writer(f)
    writer.writerow(header_csv)

    list_true_XL_csv = []
    list_false_XL_csv = []

    

    total_number_of_CSMs = len(list_crosslinks)
    to_be_ploted_x = []
    to_be_ploted_y = []
    correct_no_homo_XL = []
    homo_XL = []
    false_XL = []

    def contains_sequence(group, sequence):
        return sequence in group or any(filter(lambda s: sequence in s, group))

    def check_decoy(csm):
        matches = list(filter(lambda g: contains_sequence(g, csm[0]) and contains_sequence(g, csm[1]), list_of_groups))
        return len(matches) > 0

    for score_index in range(len(list_of_scores)):
        all_crosslinks = 0
        correct_crosslinks = 0
        homeotypic = 0

        for index_csm in range(len(list_crosslinks)):
            csm = list_crosslinks[index_csm]
            score = csm[2]

            if score >= list_of_scores[score_index]:
                all_crosslinks += 1
                temp1.append(list([csm[0], csm[1], csm[3], csm[4], str(csm[5]), str(csm[6]), str("score_" + str(score))]))

                if check_decoy(csm):
                    correct_crosslinks += 1
                    temp2.append(list([csm[0], csm[1], csm[3], csm[4], str(csm[5]), str(csm[6]), str("score_" + str(score))]))
                    if score_index == 0:
                        list_true_XL_csv.append([csm[0], csm[1], csm[3], csm[4], str(csm[5]), str(csm[6]), score,"TRUE"])
                    if csm[0] == csm[1]:
                        homeotypic += 1
                elif score_index == 0:
                    list_false_XL_csv.append([csm[0], csm[1], csm[3], csm[4], csm[5], csm[6], score,"FALSE"])

        if score_index == 0:
            for i in range(all_crosslinks):
                temp1[i].sort()
                temp1[i] = str(temp1[i])
                worksheet.write(11 + i, 0, temp1[i])

            for i in range(len(temp2)):
                temp2[i].sort()
                temp2[i] = str(temp2[i])
                worksheet.write(11 + i, 1, temp2[i])

            temp3 = list(set(temp1) - set(temp2)) 
            for i in range(len(temp3)):
                worksheet.write(11 + i, 2, str(temp3[i]))          

        to_be_ploted_x.append(list_of_scores[score_index])
        to_be_ploted_y.append((all_crosslinks-correct_crosslinks)/all_crosslinks)
        correct_no_homo_XL.append(correct_crosslinks-homeotypic)
        homo_XL.append(homeotypic)
        false_XL.append(all_crosslinks-correct_crosslinks)
        
    
    plt.plot(to_be_ploted_x,to_be_ploted_y)

    plt.title('Real FDR dependent on the score')
    plt.xlabel('Score')
    plt.ylabel('FDR')
    alarm_005 = False
    alarm_001 = False

    try:
        worksheet.write(2,1,total_number_of_CSMs)
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
    score_bar = [to_be_ploted_x[0]]


    plt.scatter(to_be_ploted_x[0],to_be_ploted_y[0])
    plt.annotate((to_be_ploted_x[0],float("{0:.3f}".format(to_be_ploted_y[0]))),(to_be_ploted_x[0],to_be_ploted_y[0]))
    if to_be_ploted_y[0]>0.05:
        for score_index in range(len(to_be_ploted_x)):
            if to_be_ploted_y[score_index]<=0.05 and alarm_005 == False:
                plt.scatter(to_be_ploted_x[score_index],to_be_ploted_y[score_index])
                plt.annotate((to_be_ploted_x[score_index],float("{0:.3f}".format(to_be_ploted_y[score_index]))),(to_be_ploted_x[score_index],to_be_ploted_y[score_index]))
                alarm_005 = True
                worksheet.write(2,4,correct_no_homo_XL[score_index]+homo_XL[score_index]+false_XL[score_index])
                bar_graph.append("FDR 5%")
                gold.append(correct_no_homo_XL[score_index])
                silver.append(homo_XL[score_index])
                bronze.append(false_XL[score_index])
                score_bar.append(to_be_ploted_x[score_index])
                if to_be_ploted_y[score_index]<=0.01:
                    alarm_001 = True
                    worksheet.write(3,4,correct_no_homo_XL[score_index]+homo_XL[score_index]+false_XL[score_index])
                    bar_graph[1] = "FDR 1%"
                    #gold.append(correct_no_homo_XL[i])
                    #silver.append(homo_XL[i])
                    #bronze.append(false_XL[i])
            if to_be_ploted_y[score_index]<=0.01 and alarm_001 == False:
                plt.scatter(to_be_ploted_x[score_index],to_be_ploted_y[score_index])
                plt.annotate((to_be_ploted_x[score_index],float("{0:.3f}".format(to_be_ploted_y[score_index]))),(to_be_ploted_x[score_index],to_be_ploted_y[score_index]))
                alarm_001 = True
                worksheet.write(3,4,correct_no_homo_XL[score_index]+homo_XL[score_index]+false_XL[score_index])
                bar_graph.append("FDR 1%")
                gold.append(correct_no_homo_XL[score_index])
                silver.append(homo_XL[score_index])
                bronze.append(false_XL[score_index])
                score_bar.append(to_be_ploted_x[score_index])
    elif to_be_ploted_y[0]<=0.05 and to_be_ploted_y[0]>0.01:
        for score_index in range(len(to_be_ploted_x)):
            if to_be_ploted_y[score_index]<=0.01 and alarm_001 == False:
                plt.scatter(to_be_ploted_x[score_index],to_be_ploted_y[score_index])
                plt.annotate((to_be_ploted_x[score_index],float("{0:.3f}".format(to_be_ploted_y[score_index]))),(to_be_ploted_x[score_index],to_be_ploted_y[score_index]))
                alarm_001 = True
                worksheet.write(3,4,correct_no_homo_XL[score_index]+homo_XL[score_index]+false_XL[score_index])
                bar_graph.append("FDR 1%")
                gold.append(correct_no_homo_XL[score_index])
                silver.append(homo_XL[score_index])
                bronze.append(false_XL[score_index])
                score_bar.append(to_be_ploted_x[score_index])
        
    workbook.close()

    plt.savefig(os.path.splitext(output_file_name)[0] + "_ScorevsFDR.svg")
    plt.clf()

    
    b_bronze = list (np.add(gold, silver))

    plt.bar(bar_graph,gold,label="true",color="green")
    plt.bar(bar_graph,silver,bottom=gold, label="true homeotypic",color="lawngreen")
    plt.bar(bar_graph,bronze,bottom=b_bronze, label="false",color="red")
    
    #plt.ylabel("Number of crosslinks")
    #plt.title("FDR-CUT-OFF-SCORE ="+ fdr_cutoff_value)
    if is_grouped:
        plt.ylabel("Number of crosslinks")
    else:
        plt.ylabel("Number of CSMs")
    plt.legend()
    plt.tick_params(
    axis='x',
    which='both',
    bottom=False,
    top=False,
    labelbottom=False)

    cell_table = []
    cell_table.append(gold)
    cell_table.append(silver)
    cell_table.append(bronze)
    cell_table.append(score_bar)
    plt.table(cellText=cell_table, cellLoc='center', rowLabels=["true","true homeotypic","false","at score"],colLabels=bar_graph ,rowLoc='left' ,colLoc='center', loc='bottom', edges='closed')
    

    plt.savefig(os.path.splitext(output_file_name)[0] + "_numberXLs.svg",bbox_inches = "tight")

    plt.clf()
    plt.xlabel("Score")
    #plt.ylabel("Number of crosslinks")
    if is_grouped:
        plt.ylabel("Number of crosslinks")
    else:
        plt.ylabel("Number of CSMs")
    plt.stackplot(list_of_scores,correct_no_homo_XL,homo_XL,false_XL,labels=["true","true homeotypic","false"], colors=["green","lawngreen","red"])
    plt.legend()
    plt.savefig(os.path.splitext(output_file_name)[0] + "_ScorevsNumber.svg")

    writer.writerows(list_true_XL_csv)
    writer.writerows(list_false_XL_csv)
    f.close()

fdr_diagamm(unique_crosslinks)