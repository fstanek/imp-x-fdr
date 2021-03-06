#MS Annika
import csv
import sys
import xlrd
import os
import xlsxwriter
import numpy as np
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True
import matplotlib.pyplot as plt

#print(sys.argv)

support_file_name = sys.argv[1]
output_file_name = sys.argv[2]
is_grouped = len(sys.argv) > 3 and sys.argv[3] == 'true'

### BEGIN LIBRARY -------------------------------------------------------------------
# open the sheetspreadfile and the respective sheet

print('Reading library file...')
#print(support_file_name)

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

print('Transferring crosslinks to script...')

def read_crosslinks():
    for line in sys.stdin:
    #for line in open('C:/Users/stanek/source/repos/imp-x-fdr/IMP_X_FDR/Resources/search-engines/annika_input.csv', 'r'):
        values = line.strip().split('\t')
        values[2] = float(values[2])    # score
        values[5] = int(values[5])      # position 1
        values[6] = int(values[6])      # position 2
        yield values

unique_crosslinks = list(read_crosslinks())
print('{} crosslinks transferred.'.format(len(unique_crosslinks)))

list_of_scores_xlinkx = list(set(map(lambda c: c[2], unique_crosslinks)))
list_of_scores_xlinkx.sort()

temp1 = []
temp2 = []

def fdr_diagamm(is_grouped):
    print('Plotting diagram...')
    temp1 = []
    temp2 = []

    workbook = xlsxwriter.Workbook(os.path.splitext(output_file_name)[0]+"_venn_input.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write(0,0, "Results")
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


    worksheet.set_column(0,0,40)
    worksheet.set_column(0,1,40)
    worksheet.set_column(0,2,40)
    worksheet.set_column(0,3,40)

    # open the file in the write mode
    f = open((output_file_name), 'w', newline='')

    #define the header
    header_csv = ["Sequence A", "Sequence B","Accession A","Accession B","Position in protein A","Position in protein B","Score crosslink","Within same group"]

    # create the csv writer
    writer = csv.writer(f)
    writer.writerow(header_csv)

    list_true_XL_csv = []
    list_false_XL_csv = []

    to_be_ploted_x = []
    to_be_ploted_y = []
    correct_no_homo_XL = []
    homo_XL = []
    false_XL = []

    correct_set = set()
    homo_set = set()

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

    for index_score in range(len(list_of_scores_xlinkx)):
        all_crosslinks = 0
        correct_crosslinks = 0
        homeotypic = 0
        
        for index_crosslink in range(len(unique_crosslinks)):
            score = unique_crosslinks[index_crosslink][2]
            seq1 = unique_crosslinks[index_crosslink][0]
            seq2 = unique_crosslinks[index_crosslink][1]

            if score >=list_of_scores_xlinkx[index_score]:
                all_crosslinks = all_crosslinks +1
                temp1.append(list([seq1, seq2,
                                   unique_crosslinks[index_crosslink][3],unique_crosslinks[index_crosslink][4],
                                   str(unique_crosslinks[index_crosslink][5]),str(unique_crosslinks[index_crosslink][6]),str("score_" + str(unique_crosslinks[index_crosslink][2]))]))
                found = False
                index_group = 0

                # cycle through library groups
                while(index_group < number_groups and found == False):
                    index_sequence = 0

                    # cycle through sequences
                    while(index_sequence < peptides_per_group[index_group] and found == False):
                        if seq1 == list_of_groups[index_group][index_sequence] or seq1 in list_of_groups[index_group][index_sequence] :
                            m = 0
                            while(m<peptides_per_group[index_group] and found== False):
                                if (unique_crosslinks[index_crosslink][1]== list_of_groups[index_group][m] or unique_crosslinks[index_crosslink][1] in list_of_groups[index_group][m]):
                                    found = True
                                    correct_crosslinks = correct_crosslinks +1
                                    correct_set.add(index_crosslink)
                                    temp2.append(list([unique_crosslinks[index_crosslink][0],unique_crosslinks[index_crosslink][1],
                                                       unique_crosslinks[index_crosslink][3],unique_crosslinks[index_crosslink][4],
                                                       str(unique_crosslinks[index_crosslink][5]),str(unique_crosslinks[index_crosslink][6]),str("score_" + str(unique_crosslinks[index_crosslink][2]))]))
                                    if index_score==0:
                                        list_true_XL_csv.append([unique_crosslinks[index_crosslink][0],unique_crosslinks[index_crosslink][1],
                                                          unique_crosslinks[index_crosslink][3],unique_crosslinks[index_crosslink][4],
                                                          str(unique_crosslinks[index_crosslink][5]),str(unique_crosslinks[index_crosslink][6]),unique_crosslinks[index_crosslink][2],"TRUE"])
                                    if unique_crosslinks[index_crosslink][0] == unique_crosslinks[index_crosslink][1]:
                                        homeotypic = homeotypic+1
                                        homo_set.add(index_crosslink)
                                else:
                                    m = m+1

                        index_sequence = index_sequence+1
                    index_group = index_group+1
                if index_score==0 and found == False:
                    list_false_XL_csv.append([unique_crosslinks[index_crosslink][0],unique_crosslinks[index_crosslink][1],
                                                          unique_crosslinks[index_crosslink][3],unique_crosslinks[index_crosslink][4],
                                                          str(unique_crosslinks[index_crosslink][5]),str(unique_crosslinks[index_crosslink][6]),unique_crosslinks[index_crosslink][2],"FALSE"])

        to_be_ploted_x.append(list_of_scores_xlinkx[index_score])
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
        worksheet.write(3,1,correct_no_homo_XL[0]+homo_XL[0]+false_XL[0])
        worksheet.write(4,1,correct_no_homo_XL[0]+homo_XL[0])
        worksheet.write(5,1,homo_XL[0])
        worksheet.write(6,1,correct_no_homo_XL[0])
        worksheet.write(7,1,false_XL[0])
    except:
        print("ATTENZIONE")

    bar_graph = ["real FDR"+" " +str(float("{0:.1f}".format((false_XL[0]/(correct_no_homo_XL[0]+homo_XL[0]+false_XL[0]))*100)))+"%"]

    gold = [correct_no_homo_XL[0]]
    silver = [homo_XL[0]]
    bronze = [false_XL[0]]
    score_bar = [to_be_ploted_x[0]]


    plt.scatter(to_be_ploted_x[0],to_be_ploted_y[0])
    plt.annotate((to_be_ploted_x[0],float("{0:.3f}".format(to_be_ploted_y[0]))),(to_be_ploted_x[0],to_be_ploted_y[0]))
    if to_be_ploted_y[0]>0.05:
        for index_score in range(len(to_be_ploted_x)):
            if to_be_ploted_y[index_score]<=0.05 and alarm_005 == False:
                plt.scatter(to_be_ploted_x[index_score],to_be_ploted_y[index_score])
                plt.annotate((to_be_ploted_x[index_score],float("{0:.3f}".format(to_be_ploted_y[index_score]))),(to_be_ploted_x[index_score],to_be_ploted_y[index_score]))
                alarm_005 = True
                worksheet.write(2,4,correct_no_homo_XL[index_score]+homo_XL[index_score]+false_XL[index_score])
                bar_graph.append("FDR 5%")
                gold.append(correct_no_homo_XL[index_score])
                silver.append(homo_XL[index_score])
                bronze.append(false_XL[index_score])
                score_bar.append(to_be_ploted_x[index_score])
                if to_be_ploted_y[index_score]<=0.01:
                    alarm_001 = True
                    worksheet.write(3,4,correct_no_homo_XL[index_score]+homo_XL[index_score]+false_XL[index_score])
                    bar_graph[1] = "FDR 1%"
            if to_be_ploted_y[index_score]<=0.01 and alarm_001 == False:
                plt.scatter(to_be_ploted_x[index_score],to_be_ploted_y[index_score])
                plt.annotate((to_be_ploted_x[index_score],float("{0:.3f}".format(to_be_ploted_y[index_score]))),(to_be_ploted_x[index_score],to_be_ploted_y[index_score]))
                alarm_001 = True
                worksheet.write(3,4,correct_no_homo_XL[index_score]+homo_XL[index_score]+false_XL[index_score])
                bar_graph.append("FDR 1%")
                gold.append(correct_no_homo_XL[index_score])
                silver.append(homo_XL[index_score])
                bronze.append(false_XL[index_score])
                score_bar.append(to_be_ploted_x[index_score])
    elif to_be_ploted_y[0]<=0.05 and to_be_ploted_y[0]>0.01:
        for index_score in range(len(to_be_ploted_x)):
            if to_be_ploted_y[index_score]<=0.01 and alarm_001 == False:
                plt.scatter(to_be_ploted_x[index_score],to_be_ploted_y[index_score])
                plt.annotate((to_be_ploted_x[index_score],float("{0:.3f}".format(to_be_ploted_y[index_score]))),(to_be_ploted_x[index_score],to_be_ploted_y[index_score]))
                alarm_001 = True
                worksheet.write(3,4,correct_no_homo_XL[index_score]+homo_XL[index_score]+false_XL[index_score])
                bar_graph.append("FDR 1%")
                gold.append(correct_no_homo_XL[index_score])
                silver.append(homo_XL[index_score])
                bronze.append(false_XL[index_score])
                score_bar.append(to_be_ploted_x[index_score])

    workbook.close()  
 
    plt.savefig(os.path.splitext(output_file_name)[0]+"_FDR-at-Score.svg")
    plt.clf()

    b_bronze = list (np.add(gold, silver))

    plt.bar(bar_graph,gold,label="true",color="green",align='center')
    plt.bar(bar_graph,silver,bottom=gold, label="true homeotypic",color="lawngreen",align='center')
    plt.bar(bar_graph,bronze,bottom=b_bronze, label="false",color="red",align='center')

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
    plt.table(cellText=cell_table, cellLoc='center', rowLabels=["true","true homeotypic","false","score cut-off"],colLabels=bar_graph ,rowLoc='left' ,colLoc='center', loc='bottom', edges='closed')
    
    plt.savefig(os.path.splitext(output_file_name)[0]+"_Number-XL.svg",bbox_inches = "tight")

    plt.clf()
    plt.xlabel("Score")
    #plt.ylabel("Number of crosslinks")
    if is_grouped:
        plt.ylabel("Number of crosslinks")
    else:
        plt.ylabel("Number of CSMs")
    plt.stackplot(list_of_scores_xlinkx,correct_no_homo_XL,homo_XL,false_XL,labels=["true","true homeotypic","false"], colors=["green","lawngreen","red"])
    plt.legend()
    plt.savefig(os.path.splitext(output_file_name)[0]+"_Score-vs-Number.svg")

    writer.writerows(list_true_XL_csv)
    writer.writerows(list_false_XL_csv)
    f.close()

fdr_diagamm(is_grouped)