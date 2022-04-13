#!/usr/bin/env python3

# MaXLinker Result file to MS Annika Result file converter
# 2022 (c) Micha Johannes Birklbauer
# https://github.com/michabirklbauer/
# micha.birklbauer@gmail.com

import json
import argparse
import pandas as pd
import traceback as tb

__version = "1.0.0"
__date = "20220413"

"""
DESCRIPTION:
A script to convert MaXLinker *.tsv result files to MS Annika format as
Microsoft Excel worksheets for usage with IMP-X-FDR.

USAGE:
maxlinkerToAnnikaFormatConverter.py f [f ...]
                                    [-o OUTPUT]
                                    [-xl CROSSLINKER]
                                    [-xlmod CROSSLINKER_MODIFICATION]
                                    [-mod MODIFICATIONS]
                                    [-h]
                                    [--version]

positional arguments:
  f                     MaXLinker result file to process, if second filename
                        is given it will be used as the output name!

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Name of the output file.
  -xl CROSSLINKER, --crosslinker CROSSLINKER
                        Name of the Crosslinker e.g. DSSO.
  -xlmod CROSSLINKER_MODIFICATION, --crosslinker-modification CROSSLINKER_MODIFICATION
                        Residue that the Crosslinker binds to e.g. K for DSSO.
  -mod MODIFICATIONS, --modifications MODIFICATIONS
                        Modifications as dictionary string / in json format.
  --version             show program's version number and exit
"""

#### MS Annika Result columns mapping ####
# Checked: (bool) TRUE | FALSE                             -> create with FALSE
# Crosslinker:  (string) e.g. DSSO                         -> create with crosslinker name
# Crosslink Type: (string selection) Intra | Inter         -> need function of protein id A and protein id B
# # CSMs: (int)                                            -> mapped #CSMs
# # Proteins: (int)                                        -> create with zeros
# Sequence A: (string) e.g. [K]SSAAR                       -> converter function for modifications
# Accession A: (string) e.g. P0A7X3                        -> mapped Protein_A id
# Position A: int                                          -> get from Peptide A, need function
# Sequence B: (string)                                     -> f
# Accession B: (string)                                    -> mapped Protein_B id
# Position B: (int)                                        -> f
# Protein Descriptions A: (string)                         -> mapped Protein_a description
# Protein Descriptions B: (string)                         -> mapped Protein_b description
# Best CSM Score: (double)                                 -> mapped Score
# In protein A: (int)                                      -> create with zeros
# In protein B: (int)                                      -> create with zeros
# Decoy: (bool) TRUE | FALSE                               -> create with FALSE
# Modifications A: (string) e.g. K1(DSSO);M1(Oxidation)    -> f
# Modifications B: (string)                                -> f
# Confidence: (string selection) High | Medium | Low       -> create with High

# function that returns the type of crosslink made
# protein_idA = string (Accession of Protein A)
# protein_idB = string (Accession of Protein B)
def create_crosslinker_type(protein_idA, protein_idB):
    if protein_idA.upper() == protein_idB.upper():
        return "Intra"
    else:
        return "Inter"

# function that returns sequence in annika format, position of crosslinker, modifications
# sequence = string (MaXLinker Sequence)
# crosslinker = string (crosslinker name)
# crosslinker_aa = string (upper case)
# possible_modifications = dictionary AA:Modification (AA in upper case)
def create_modifications(sequence, crosslinker, crosslinker_aa, possible_modifications):
    annika_sequence = ""
    position = 1
    modifications = ""

    i = 1
    for AA in sequence:
        if AA.isupper():
            annika_sequence += AA
        else:
            if AA.upper() == crosslinker_aa:
                position = i
                modifications += AA.upper() + str(i) + "(" + crosslinker + ");"
                annika_sequence += "[" + AA.upper() + "]"
            else:
                modifications += AA.upper() + str(i) + "(" + possible_modifications[AA.upper()] + ");"
                annika_sequence += AA.upper()
        i += 1;

    modifications.rstrip(";")
    return {"Sequence": annika_sequence, "Position": position, "Modifications": modifications}

# function that returns pandas dataframe in annika format
# maxlinker_filename = string (path to the file)
# crosslinker = string (crosslinker name)
# crosslinker_aa = string (upper case)
# possible_modifications = dictionary AA:Modification (AA in upper case)
def create_annika_result(maxlinker_filename, crosslinker = "DSSO", crosslinker_aa = "K", possible_modifications = {"M": "Oxidation", "C": "Carbamidomethyl"}):
    # load file
    maxlinker_df = pd.read_csv(maxlinker_filename, sep = "\t", engine = "python")
    nrows = maxlinker_df.shape[0]

    # columns
    Checked = ["FALSE" for i in range(nrows)]
    Crosslinker = [crosslinker for i in range(nrows)]
    Crosslink_Type = []
    CSMs = []
    Proteins = [0 for i in range(nrows)]
    Sequence_A = []
    Accession_A = []
    Position_A = []
    Sequence_B = []
    Accession_B = []
    Position_B = []
    Protein_Descriptions_A = []
    Protein_Descriptions_B = []
    Best_CSM_Score = []
    In_protein_A = [0 for i in range(nrows)]
    In_protein_B = [0 for i in range(nrows)]
    Decoy = ["FALSE" for i in range(nrows)]
    Modifications_A = []
    Modifications_B = []
    Confidence = ["High" for i in range(nrows)]

    # fill columns
    Crosslinker_Type = maxlinker_df.apply(lambda row: create_crosslinker_type(row["Protein_A id"], row["Protein_B id"]), axis = 1).tolist()
    CSMs = maxlinker_df["#CSMs"].tolist()
    Info_A = maxlinker_df.apply(lambda row: create_modifications(row["Peptide A"], crosslinker, crosslinker_aa, possible_modifications), axis = 1).tolist()
    for item in Info_A:
        Sequence_A.append(item["Sequence"])
        Position_A.append(item["Position"])
        Modifications_A.append(item["Modifications"])
    Info_B = maxlinker_df.apply(lambda row: create_modifications(row["Peptide_B"], crosslinker, crosslinker_aa, possible_modifications), axis = 1).tolist()
    for item in Info_B:
        Sequence_B.append(item["Sequence"])
        Position_B.append(item["Position"])
        Modifications_B.append(item["Modifications"])
    Accession_A = maxlinker_df["Protein_A id"].tolist()
    Accession_B = maxlinker_df["Protein_B id"].tolist()
    Protein_Descriptions_A = maxlinker_df["Protein_a description"].tolist()
    Protein_Descriptions_B = maxlinker_df["Protein_b description"].tolist()
    Best_CSM_Score = maxlinker_df["Score"].tolist()

    # create annika dataframe
    annika_df = pd.DataFrame({"Checked": Checked,
                              "Crosslinker": Crosslinker,
                              "Crosslink Type": Crosslinker_Type,
                              "# CSMs": CSMs,
                              "# Proteins": Proteins,
                              "Sequence A": Sequence_A,
                              "Accession A": Accession_A,
                              "Position A": Position_A,
                              "Sequence B": Sequence_B,
                              "Accession B": Accession_B,
                              "Position B": Position_B,
                              "Protein Descriptions A": Protein_Descriptions_A,
                              "Protein Descriptions B": Protein_Descriptions_B,
                              "Best CSM Score": Best_CSM_Score,
                              "In protein A": In_protein_A,
                              "In protein B": In_protein_B,
                              "Decoy": Decoy,
                              "Modifications A": Modifications_A,
                              "Modifications B": Modifications_B,
                              "Confidence": Confidence})

    return annika_df

# read MaXLinker result and write MS Annika result (in xlsx format)
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(metavar = "f",
                        dest = "files",
                        help = "MaXLinker result file to process, if second filename is given it will be used as the output name!",
                        type = str,
                        nargs = "+")
    parser.add_argument("-o", "--output",
                        dest = "output",
                        default = None,
                        help = "Name of the output file.",
                        type = str)
    parser.add_argument("-xl", "--crosslinker",
                        dest = "crosslinker",
                        default = "DSSO",
                        help = "Name of the Crosslinker e.g. DSSO.",
                        type = str)
    parser.add_argument("-xlmod", "--crosslinker-modification",
                        dest = "crosslinker_modification",
                        default = "K",
                        help = "Residue that the Crosslinker binds to e.g. K for DSSO.",
                        type = str)
    parser.add_argument("-mod", "--modifications",
                        dest = "modifications",
                        default = "{\"M\": \"Oxidation\", \"C\": \"Carbamidomethyl\"}",
                        help = "Modifications as dictionary string / in json format.",
                        type = str)
    parser.add_argument("--version",
                        action = "version",
                        version = __version)
    args = parser.parse_args()

    try:
        modifications = json.loads(args.modifications)
    except Exception as e:
        print("ERROR parsing modifications! Are they in the correct format?")
        tb.print_exc()
        print(repr(e))

    input_file = args.files[0]
    output_file = args.files[0].split(".tsv")[0] + ".xlsx"

    if len(args.files) > 1:
        output_file = args.files[1].split(".xlsx")[0] + ".xlsx"

    if args.output is not None:
        output_file = args.output.split(".xlsx")[0] + ".xlsx"

    maxlinker_resultdf = create_annika_result(input_file, args.crosslinker, args.crosslinker_modification, modifications)
    maxlinker_resultdf.to_excel(output_file, sheet_name = "Crosslinks", index = False, engine = "xlsxwriter")

if __name__ == "__main__":
    main()
