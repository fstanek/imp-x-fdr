using XUnifier.Constants;
using XUnifier.Handlers;
using XUnifier.Models;
using XUnifier.Readers;
using XUnifier.Utils;

namespace XUnifier
{
    public static class CrosslinkReaderFactory
    {
        public static IEnumerable<Crosslink> GetCrosslinks(string fileName, bool groupCSMs, out string displayName)
        {
            displayName = null;

            var reader = GetReader(fileName);
            if (reader is null)
                return null;

            var handler = GetFormatHandlers().FirstOrDefault(h => h.CanRead(reader));
            if (handler is null)
                return null;

            displayName = handler.DisplayName;
            handler.Apply(reader);

            var items = reader.Read().ToArray();

            if (groupCSMs)
            {
                var comparer = new LinkerSiteCollectionEqualityComparer();
                items = items.GroupBy(i => i.LinkerSites, comparer).Select(g => new Crosslink
                {
                    LinkerSites = g.Key,
                    Score = g.Max(i => i.Score)
                }).ToArray();
            }

            foreach (var item in items)
                item.LinkerSites = new LinkerSiteCollection(item.LinkerSites.OrderBy(l => l.Sequence));

            return items;
        }

        private static CrosslinkReader GetReader(string fileName)
        {
            var stream = File.OpenRead(fileName);

            switch (Path.GetExtension(fileName))
            {
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

        private static IEnumerable<IFormatHandler> GetFormatHandlers()
        {
            // TODO read from assembly?

            yield return new AnnikaFormatHandler();
            yield return new PlinkFormatHandler();
            yield return new XiFormatHandler();
            yield return new XLinkXFormatHandler();

            yield return new MeroxFormatHandler();
        }
    }
}