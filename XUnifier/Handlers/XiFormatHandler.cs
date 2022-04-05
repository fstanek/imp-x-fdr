using System.Text.RegularExpressions;
using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class XiFormatHandler : FormatHandlerBase<CommaSeparatedReader>
    {
        private readonly Regex sequenceParser = new Regex("[^A-Z]*", RegexOptions.Compiled);

        public override string DisplayName => "Xi";
        public override bool IsGrouped => false;

        protected override void Initialize()
        {
            RegisterHandlers(c => c.Site1, 1);
            RegisterHandlers(c => c.Site2, 2);
            Register<double>("Score", (csm, value) => csm.Score = value);
        }

        private void RegisterHandlers(Func<Crosslink, LinkerSite> selector, int number)
        {
            Register<string>($"Protein{number}",
                (csm, value) => selector(csm).Accession = value);

            Register<string>($"PepSeq{number}",
                (csm, value) => selector(csm).Sequence = sequenceParser.Replace(value, string.Empty));

            Register<int>($"ProteinLinkPos{number}",
                (csm, value) => selector(csm).ProteinLink = value);

            Register<int>($"LinkPos{number}",
                (csm, value) => selector(csm).PeptideLink = value);
        }
    }
}