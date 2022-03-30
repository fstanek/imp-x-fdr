using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class XLinkXFormatHandler : FormatHandlerBase<ExcelReader>
    {
        public override string DisplayName => "XlinkX";

        protected override void Initialize()
        {
            RegisterColumns("A", 0);
            RegisterColumns("B", 1);
            Register<double>("XlinkX Score", (csm, value) => csm.Score = value);
        }

        private void RegisterColumns(string discriminator, int index)
        {
            Register<string>($"Protein Accession {discriminator}",
               (csm, value) => csm.LinkerSites[index].Accession = value);

            Register<string>($"Sequence {discriminator}",
                (csm, value) => csm.LinkerSites[index].Sequence = value);

            Register<int>($"Leading Protein Position {discriminator}",
                (csm, value) => csm.LinkerSites[index].ProteinLink = value);

            Register<int>($"Crosslinker Position {discriminator}",
                (csm, value) => csm.LinkerSites[index].PeptideLink = value);
        }
    }
}