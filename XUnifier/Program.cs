//using XUnifier.Models;

//var input = @"C:\Users\stanek\source\repos\imp-x-fdr\IMP_X_FDR\Resources\search-engines\merox_input.csv";
//var output = @"C:\Users\stanek\source\repos\imp-x-fdr\IMP_X_FDR\Resources\search-engines\merox_output.csv";

//var lines1 = File.ReadLines(input).Select(l => l.Trim()).ToHashSet();
//var lines2 = File.ReadLines(output).Select(l => l.Trim()).ToHashSet();

//IEnumerable<Crosslink> Read(string fileName)
//{
//    var items = File.ReadLines(fileName).Select(line =>
//    {
//        var values = line.Split("\t");

//        return new Crosslink
//        {
//            Score = double.Parse(values[2]),
//            Site1 = new LinkerSite
//            {
//                Accession = values[3],
//                Sequence = values[0].Replace('B', 'C'),
//                ProteinLink = int.Parse(values[5])
//            },
//            Site2 = new LinkerSite
//            {
//                Accession = values[4],
//                Sequence = values[1].Replace('B', 'C'),
//                ProteinLink = int.Parse(values[6])
//            }
//        };
//    }).ToArray();

//    foreach (var item in items)
//    {
//        var sites = new[] { item.Site1, item.Site2 }.OrderBy(s => s.Accession).ThenBy(s => s.Sequence).ThenBy(s => s.ProteinLink).ToArray();
//        item.Site1 = sites.First();
//        item.Site2 = sites.Last();
//    }

//    return items;
//}

//var matc = lines1.Where(lines2.Contains).ToArray();

//var crosslinks1 = Read(input).OrderBy(c => c.Score).ToArray();
//var crosslinks2 = Read(output).OrderBy(c => c.Score).ToArray();

//var found = new List<Crosslink>();

//foreach (var crosslink1 in crosslinks1)
//{
//    var matches = crosslinks2.Where(c => c.Score == crosslink1.Score)
//        .Where(c => (c.Site1 == crosslink1.Site1 && c.Site2 == crosslink1.Site2) || (c.Site1 == crosslink1.Site2 && c.Site2 == crosslink1.Site1))
//        .ToArray();

//    if(matches.Length > 1)
//    {

//    }
//    else if(matches.Length == 1)
//    {
//        found.Add(matches.First());
//    }
//}

//Console.ReadLine();