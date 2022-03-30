using XUnifier;
using XUnifier.Utils;

var fileNameAnnika = @"C:\Users\stanek\Documents\test files\imp-x-fdr\Annika\reanal_pl1_DSSO_Annika_standard_pepength7.xlsx";
//fileNameAnnika = @"C:\Users\stanek\Documents\test files\imp-x-fdr\Annika\reanal_pl1_DSSO_Annika_standard_pepength7_shrinked.xlsx";
var fileNameXlinkX = @"C:\Users\stanek\Documents\test files\imp-x-fdr\XlinkX\20210203_QExHFX3_RSLC10_Matzinger_Mechtler_IMP_XLMS_DSSO_pure.xlsx";

//var fileNamePlink = @"C:\Users\stanek\Documents\test files\test-data_Adrian\input files\DSSO_plink_rep1.csv";
//fileNamePlink = @"C:\Users\stanek\Documents\test files\imp-x-fdr\pLink\DSBSO_rep2_plink.csv";
//var meroxFileName = @"C:\Users\stanek\Documents\test files\imp-x-fdr\MeroX\rep3_DSSO-pl1_KSTY.zhrm";
//var fileNameXi = @"C:\Users\stanek\Documents\test files\imp-x-fdr\xiSearch\Cas_DSSO_E4data_20220120_Xi1.7.6.5_CSM_xiFDR2.1.5.5.csv";

//var fileName = @"C:\Users\stanek\source\repos\imp-x-fdr\IMP_X_FDR\Resources\libraries\main_library.xlsx";
//using var libraryReader = new LibraryReader(fileName);
//var libraryGroups = libraryReader.Read().ToArray();

var inputFileName = fileNameAnnika;
var libraryFileName = @"C:\Users\stanek\source\repos\imp-x-fdr\IMP_X_FDR\Resources\libraries\\main_library.xlsx";
var outputFileName = @"C:\Users\stanek\Documents\test files\imp-x-fdr\Annika\reanal_pl1_DSSO_Annika_standard_pepength7_scriptoutput.csv";

var items = CrosslinkReaderFactory.GetCrosslinks(inputFileName, false, out var displayName);

var pythonFileName = @"C:\Users\stanek\source\repos\imp-x-fdr\IMP_X_FDR\Resources\read_stdin.py";
pythonFileName = @"C:\Users\stanek\source\repos\imp-x-fdr\IMP_X_FDR\Resources\search-engines\annika_master_score.py";
//pythonFileName = @"C:\Users\stanek\source\repos\imp-x-fdr\IMP_X_FDR\Resources\search-engines\test.py";

//using var stream = new MemoryStream();
//using var inputWriter = new StreamWriter(stream);
//foreach(var item in items)
//{
//    inputWriter.WriteLine(string.Join('\t',
//        item.LinkerSites[0].Sequence,
//        item.LinkerSites[1].Sequence,
//        item.Score.ToString(CultureInfo.InvariantCulture),
//        item.LinkerSites[0].Accession,
//        item.LinkerSites[1].Accession,
//        item.LinkerSites[0].ProteinLink,
//        item.LinkerSites[1].ProteinLink));
//}
//inputWriter.Flush();
//stream.Seek(0, SeekOrigin.Begin);

var pythonHandler = new PythonHandler();
pythonHandler.AddArgument(pythonFileName);
pythonHandler.AddArgument(libraryFileName);
pythonHandler.AddArgument(outputFileName);
pythonHandler.OutputReceived += Console.WriteLine;
pythonHandler.ErrorReceived += text => Console.WriteLine($"ERROR: {text}");
var exitCode = pythonHandler.Run(items.Select(CrosslinkHelper.GetLine));

Console.ReadLine();