# IMP-X-FDR

## Features

This software provides an easy to use and automated way for validation of the false discovery rate (FDR) of crosslink search results from the search enignes MeroX, Annika, XlinkX, pLink 2, MaxLynx and xiSearch. Therby data optined from a synthetic peptide library system is used where every correct crosslink is known since the crosslink reaciton was performed on peptides in seperate groups.
The following formula describes the basic validation step performed by IMP-X-FDR to calculate the an experimentally validated FDR:
FDR_(experimentally validated)=(#target XLs across peptides not within same XL group)/(#target XLs total)

IMP-X-FDR can be used for other than the above mentioned serach engines as well, if the used crosslink input (csv-)list is adopted to one of the formats that corresponds to one of these supported search engines.
This makes IMP-X-FDR a valuable tool for testing novel crosslinkers, to compare acquisition strategies or to benchmark crosslink search algorithms.

Additional functionalities are the comparison of crosslink IDs found from different replicates or across different search engines using Venn diagrams as well as to investigate intrinsic properties (mass, pI value, amino-acid sequences analyses, ...) of the crosslinks dependent on retention time. The tool thereby allows a comparison of the physicochemical properties of identified crosslinks vs those theoretically formed within the peptide library used.

## Getting started

### Software requirements
> **Note that the tool is only compatible to Windows at the moment.**

In order to run the application you need the following software installed:
- [.NET 6 Desktop Runtime](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-desktop-6.0.3-windows-x64-installer)
- [Python 3.9 (or higher)](https://www.python.org/downloads/)
  - Missing packages will be installed automatically

### Installation

1. Download the [latest release](https://github.com/fstanek/imp-x-fdr/releases/latest)
2. Unpack the archive
3. Run `IMP_X_FDR.exe`

In case of missing supporting programs -like Python- on your system, you will be automatically redirected to the respective installation website. Install the suitable version for your computer.
 
Please refer to the users manual for additional information.

## Citation
Matzinger et al. Mimicked synthetic ribosomal protein complex for benchmarking crosslinking mass spectrometry workflows. https://doi.org/10.1101/2021.10.21.465295
