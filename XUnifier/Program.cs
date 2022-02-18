using XUnifier;
using XUnifier.Models;
using XUnifier.Utils;
using XUnifier.Writers;

//var fileNameAnnika = @"C:\Users\stanek\Documents\test files\imp-x-fdr\Annika\reanal_pl1_DSSO_Annika_standard_pepength7.xlsx";
//var fileNameXlinkX = @"C:\Users\stanek\Documents\test files\imp-x-fdr\XlinkX\20210203_QExHFX3_RSLC10_Matzinger_Mechtler_IMP_XLMS_DSSO_pure.xlsx";

//var fileNamePlink = @"C:\Users\stanek\Documents\test files\test-data_Adrian\input files\DSSO_plink_rep1.csv";
//fileNamePlink = @"C:\Users\stanek\Documents\test files\imp-x-fdr\pLink\DSBSO_rep2_plink.csv";

//var meroxFileName = @"C:\Users\stanek\Documents\test files\imp-x-fdr\MeroX\rep3_DSSO-pl1_KSTY.zhrm";

//var fileNameXi = @"C:\Users\stanek\Documents\test files\imp-x-fdr\xiSearch\Cas_DSSO_E4data_20220120_Xi1.7.6.5_CSM_xiFDR2.1.5.5.csv";

if(!args.Any())
{
    Console.WriteLine("ERROR: Too few arguments.");
    return;
}

var inputFileName = args.First();

var outputFileName = args.Length > 1
    ? args[1]
    : Path.ChangeExtension(inputFileName, ".XUnified.csv");

var items = FormatReaderFactory.GetCrosslinkSpectrumMatches(inputFileName).ToArray();
var comparer = new CrosslinkEqualityComparer();

foreach (var item in items)
{
    item.LinkerSites = new LinkerSiteCollection(item.LinkerSites.OrderBy(l => l.Accession).ThenBy(l => l.Sequence).ThenBy(s => s.PeptideLink));

    var site1 = item.LinkerSites.First();
    var site2 = item.LinkerSites.Last();

   if(site1.Accession == site2.Accession)
    {
        if (site1.Sequence == site2.Sequence)
            item.CrosslinkType = CrosslinkType.IntraPeptide;
        else
            item.CrosslinkType = CrosslinkType.InterProtein;
    }
}

var groups = items.GroupBy(i => i.LinkerSites, comparer).ToArray();

Console.WriteLine($"{items.Length} CSMs");
Console.WriteLine($"{groups.Length} unique crosslinks");

Console.WriteLine($"Writing to {outputFileName}");

using var writer = new CommaSeparatedWriter<CrosslinkSpectrumMatch>(@"C:\temp\output.csv");
Assign(0);
Assign(1);
writer.Write(items);

Console.WriteLine("Finished.");
Console.ReadLine();

void Assign(int index)
{
    int number = index + 1;
    writer.Register($"Accession{number}", csm => csm.LinkerSites[index].Accession);
    writer.Register($"ProteinLink{number}", csm => csm.LinkerSites[index].ProteinLink);
    writer.Register($"Sequence{number}", csm => csm.LinkerSites[index].Sequence);
    writer.Register($"PeptideLink{number}", csm => csm.LinkerSites[index].PeptideLink);
}