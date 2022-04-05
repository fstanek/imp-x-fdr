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
        public override bool IsGrouped => false;

        protected override void Initialize()
        {
            Register<string>("Proteins", ParseProteins);
            Register<string>("Peptide", ParsePeptides);
            Register<double>("Score", (csm, value) => csm.Score = -Math.Log10(value));
        }

        private void ParseProteins(Crosslink csm, string value)
        {
            var matches = proteinRegex.Matches(value);

            void ParseProteinSite(LinkerSite site, Match match)
            {
                site.Accession = match.GetString("acc");
                site.ProteinLink = match.GetInt32("pos");
            }

            ParseProteinSite(csm.Site1, matches.ElementAt(0));
            ParseProteinSite(csm.Site2, matches.ElementAt(1));
        }

        private void ParsePeptides(Crosslink csm, string value)
        {
            var matches = peptideRegex.Matches(value);

            void ParsePeptideSite(LinkerSite site, Match match)
            {
                site.Sequence = match.GetString("seq");
                site.PeptideLink = match.GetInt32("pos");
            }

            ParsePeptideSite(csm.Site1, matches.ElementAt(0));
            ParsePeptideSite(csm.Site2, matches.ElementAt(1));
        }
    }
}