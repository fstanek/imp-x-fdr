using XUnifier.Constants;
using XUnifier.Handlers;
using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier
{
    public static class CrosslinkReaderFactory
    {
        public static IEnumerable<Crosslink> GetCrosslinks(string fileName, out string displayName)
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

            foreach (var item in items)
            {
                var orderedSites = new[] { item.Site1, item.Site2 }.OrderBy(s => s.Sequence).ToArray();
                item.Site1 = orderedSites.First();
                item.Site2 = orderedSites.Last();
            }

            return items;
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

        private static IEnumerable<IFormatHandler> GetFormatHandlers()
        {
            // TODO read from assembly?

            yield return new AnnikaFormatHandler();
            yield return new MaxLynxFormatHandler();
            yield return new PlinkFormatHandler();
            yield return new XiFormatHandler();
            yield return new XLinkXFormatHandler();

            yield return new MeroxFormatHandler();
        }
    }
}