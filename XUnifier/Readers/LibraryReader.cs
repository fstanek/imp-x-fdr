using OfficeOpenXml;
using XUnifier.Models;

namespace XUnifier.Readers
{
    public class LibraryReader : IDisposable
    {
        private const string GroupPrefix = "Group";

        private readonly ExcelPackage package;

        public LibraryReader(string fileName)
        {
            ExcelPackage.LicenseContext = LicenseContext.NonCommercial;
            package = new ExcelPackage(fileName);
        }

        public IEnumerable<LibraryGroup> Read()
        {
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

        public void Dispose()
        {
            package.Dispose();
        }
    }
}