using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class XLinkXFormatHandler : IFormatHandler
    {
        public string DisplayName => "XlinkX";
        public Type ReaderType => typeof(ExcelReader<CrosslinkSpectrumMatch>);

        public IEnumerable<Func<TableReader<CrosslinkSpectrumMatch>, bool>> ColumnHandlers
        {
            get
            {
                foreach (var handler in GetColumnHandlers("A", 0))
                    yield return handler;

                foreach (var handler in GetColumnHandlers("B", 1))
                    yield return handler;

                yield return reader => reader.Register<double>("XlinkX Score", (csm, value) => csm.Score = value);
            }
        }

        private IEnumerable<Func<TableReader<CrosslinkSpectrumMatch>, bool>> GetColumnHandlers(string discriminator, int index)
        {
            yield return reader => reader.Register<string>($"Protein Accession {discriminator}",
                (csm, value) => csm.LinkerSites[index].Accession = value);

            yield return reader => reader.Register<string>($"Sequence {discriminator}",
                (csm, value) => csm.LinkerSites[index].Sequence = value);

            yield return reader => reader.Register<int>($"Leading Protein Position {discriminator}",
                (csm, value) => csm.LinkerSites[index].ProteinLink = value);

            yield return reader => reader.Register<int>($"Crosslinker Position {discriminator}",
                (csm, value) => csm.LinkerSites[index].PeptideLink = value);
        }
    }
}