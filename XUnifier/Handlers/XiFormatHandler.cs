using System.Text.RegularExpressions;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class XiFormatHandler : FormatHandlerBase<CommaSeparatedReader>
    {
        private readonly Regex sequenceParser = new Regex("[^A-Z]*", RegexOptions.Compiled);

        public override string DisplayName => "Xi";

        protected override void Initialize()
        {
            RegisterHandlers(0);
            RegisterHandlers(1);
            Register<double>("Score", (csm, value) => csm.Score = value);
        }

        private void RegisterHandlers(int index)
        {
            var number = index + 1;

            Register<string>($"Protein{number}",
                (csm, value) => csm.LinkerSites[index].Accession = value);

            Register<string>($"PepSeq{number}",
                (csm, value) => csm.LinkerSites[index].Sequence = sequenceParser.Replace(value, string.Empty));

            Register<int>($"ProteinLinkPos{number}",
                (csm, value) => csm.LinkerSites[index].ProteinLink = value);

            Register<int>($"LinkPos{number}",
                (csm, value) => csm.LinkerSites[index].PeptideLink = value);
        }
    }
}