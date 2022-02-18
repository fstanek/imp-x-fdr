using System.Text.RegularExpressions;
using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class XiFormatHandler : IFormatHandler
    {
        private readonly Regex sequenceParser = new Regex("[^A-Z]*", RegexOptions.Compiled);

        public string DisplayName => "Xi";
        public Type ReaderType => typeof(CommaSeparatedReader<CrosslinkSpectrumMatch>);

        public IEnumerable<Func<TableReader<CrosslinkSpectrumMatch>, bool>> ColumnHandlers
        {
            get
            {
                foreach (var handler in Enumerable.Range(0, 2).SelectMany(GetColumnHandlers))
                    yield return handler;

                yield return reader => reader.Register<double>("Score", (csm, value) => csm.Score = value);
            }
        }

        private IEnumerable<Func<TableReader<CrosslinkSpectrumMatch>, bool>> GetColumnHandlers(int index)
        {
            var number = index + 1;

            yield return reader => reader.Register<string>($"Protein{number}",
                (csm, value) => csm.LinkerSites[index].Accession = value);

            yield return reader => reader.Register<string>($"PepSeq{number}",
                (csm, value) => csm.LinkerSites[index].Sequence = sequenceParser.Replace(value, string.Empty));

            yield return reader => reader.Register<int>($"ProteinLinkPos{number}",
                (csm, value) => csm.LinkerSites[index].ProteinLink = value);

            yield return reader => reader.Register<int>($"LinkPos{number}",
                (csm, value) => csm.LinkerSites[index].PeptideLink = value);
        }
    }
}