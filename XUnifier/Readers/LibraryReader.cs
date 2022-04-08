using OfficeOpenXml;
using XUnifier.Models;

namespace XUnifier.Readers
{
    public static class LibraryReader
    {
        private const string GroupPrefix = "Group";

        static LibraryReader()
        {
            ExcelPackage.LicenseContext = LicenseContext.NonCommercial;
        }

        public static IEnumerable<LibraryGroup> Read(string fileName)
        {
            using var package = new ExcelPackage(fileName);

            var sheet = package.Workbook.Worksheets.First();
            var values = Enumerable.Range(1, sheet.Dimension.Rows).Select(i => sheet.GetValue<string>(i, 1)).ToArray();

            while (values.Any())
            {
                var name = values.First();
                values = values.Skip(1).ToArray();

                var sequences = values.TakeWhile(v => !v.StartsWith(GroupPrefix)).ToList();
                values = values.Skip(sequences.Count).ToArray();

                yield return new LibraryGroup
                {
                    Name = name,
                    Sequences = sequences.ToHashSet()
                };
            }
        }
    }
}