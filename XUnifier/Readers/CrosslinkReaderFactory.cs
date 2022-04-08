using XUnifier.Constants;
using XUnifier.Models;
using XUnifier.Readers;
using XUnifier.Utils;

namespace XUnifier
{
    public static class CrosslinkReaderFactory
    {
        public static IEnumerable<Crosslink> GetCrosslinks(string fileName, out bool isGrouped)
        {
            var reader = GetReader(fileName);
            isGrouped = reader.FormatHandler.IsGrouped;
            return reader?.Read();
        }

        public static IEnumerable<Crosslink> Group(IEnumerable<Crosslink> crosslinks)
        {
            return crosslinks.GroupBy(i => (i.Site1, i.Site2)).Select(g => new Crosslink
            {
                Site1 = g.Key.Site1,
                Site2 = g.Key.Site2,
                Score = g.Max(i => i.Score)
            });
        }

        public static IEnumerable<Crosslink> Order(IEnumerable<Crosslink> crosslinks)
        {
            foreach (var crosslink in crosslinks)
            {
                var orderedSites = new[] { crosslink.Site1, crosslink.Site2 }.OrderBy(s => s.Sequence).ToArray();
                crosslink.Site1 = orderedSites.First();
                crosslink.Site2 = orderedSites.Last();
                yield return crosslink;
            }
        }

        private static CrosslinkReader GetReader(string fileName)
        {
            var stream = File.OpenRead(fileName);

            switch (Path.GetExtension(fileName))
            {
                case FileExtensions.Text:
                case FileExtensions.CommaSeparated:
                    return new CommaSeparatedReader(stream);

                case FileExtensions.Excel:
                    return new ExcelReader(stream);

                case FileExtensions.Zhrm:
                    return new MeroxReader(stream);

                default:
                    return null;
            }
        }
    }
}