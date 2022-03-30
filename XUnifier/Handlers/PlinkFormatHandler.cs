using System.Text.RegularExpressions;
using XUnifier.Extensions;
using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class PlinkFormatHandler : FormatHandlerBase<CommaSeparatedReader>
    {
        private readonly Regex proteinRegex = new Regex(@"(?<acc>[^-\/]+)\((?<pos>\d+)\)", RegexOptions.Compiled);
        private readonly Regex peptideRegex = new Regex(@"(?<seq>[^(-]+)\((?<pos>\d+)\)", RegexOptions.Compiled);

        public override string DisplayName => "pLink";

        protected override void Initialize()
        {
            Register<string>("Proteins", ParseProteins);
            Register<string>("Peptide", ParsePeptides);
            Register<double>("Score", (csm, value) => csm.Score = value);
        }

        private void ParseProteins(Crosslink csm, string value)
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

        private void ParsePeptides(Crosslink csm, string value)
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