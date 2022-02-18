using System.Text.RegularExpressions;
using XUnifier.Extensions;
using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class PlinkFormatHandler : IFormatHandler
    {
        private readonly Regex proteinRegex = new Regex(@"(?<acc>[^-\/]+)\((?<pos>\d+)\)", RegexOptions.Compiled);
        private readonly Regex peptideRegex = new Regex(@"(?<seq>[^(-]+)\((?<pos>\d+)\)", RegexOptions.Compiled);

        public string DisplayName => "pLink";
        public Type ReaderType => typeof(CommaSeparatedReader<CrosslinkSpectrumMatch>);

        public IEnumerable<Func<TableReader<CrosslinkSpectrumMatch>, bool>> ColumnHandlers
        {
            get
            {
                yield return reader => reader.Register<string>("Proteins", ParseProteins);
                yield return reader => reader.Register<string>("Peptide", ParsePeptides);
            }
        }

        private void ParseProteins(CrosslinkSpectrumMatch csm, string value)
        {
            var matches = proteinRegex.Matches(value);

            for (int i = 0; i < matches.Count; i++)
            {
                var match = matches[i];
                var site = csm.LinkerSites[i];

                site.Accession = match.GetString("acc");
                site.ProteinLink = match.GetInt32("pos");
            }
        }

        private void ParsePeptides(CrosslinkSpectrumMatch csm, string value)
        {
            var matches = peptideRegex.Matches(value);

            for (int i = 0; i < matches.Count; i++)
            {
                var match = matches[i];
                var site = csm.LinkerSites[i];

                site.Sequence = match.GetString("seq");
                site.PeptideLink = match.GetInt32("pos");
            }
        }
    }
}