using XUnifier.Constants;
using XUnifier.Handlers;
using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier
{
    public static class FormatReaderFactory
    {
        public static IEnumerable<CrosslinkSpectrumMatch> GetCrosslinkSpectrumMatches(string fileName)
        {
            var reader = GetReader(fileName);
            var handlers = GetFormatHandlers().Where(h => h.ReaderType.IsAssignableTo(reader.GetType())).ToArray();

            foreach (var handler in handlers)
            {
                if (handler.ColumnHandlers.All(h => h(reader)))
                {
                    Console.WriteLine($"Format: {handler.DisplayName}");
                    break;
                }
                else
                {
                    reader.Clear();
                }
            }

            return reader.Read();
        }

        private static TableReader<CrosslinkSpectrumMatch> GetReader(string fileName)
        {
            var stream = File.OpenRead(fileName);

            switch (Path.GetExtension(fileName))
            {
                case FileExtensions.CommaSeparated:
                    return new CommaSeparatedReader<CrosslinkSpectrumMatch>(stream);

                case FileExtensions.Excel:
                    return new ExcelReader<CrosslinkSpectrumMatch>(stream);

                case FileExtensions.Zhrm:
                    return new MeroxReader(stream);

                default:
                    return null;
            }
        }

        private static IEnumerable<IFormatHandler> GetFormatHandlers()
        {
            yield return new AnnikaFormatHandler();
            yield return new PlinkFormatHandler();
            yield return new XiFormatHandler();
            yield return new XLinkXFormatHandler();

            yield return new MeroxFormatHandler();
        }
    }
}