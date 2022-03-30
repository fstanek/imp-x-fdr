using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class AnnikaFormatHandler : FormatHandlerBase<ExcelReader>
    {
        public override string DisplayName => "Annika";

        protected override void Initialize()
        {
            Register<double>("Combined Score", (csm, value) => csm.Score = value);
            RegisterHandlers("A", 0);
            RegisterHandlers("B", 1);
        }

        private void RegisterHandlers(string discriminator, int index)
        {
            Register<string>($"Accession {discriminator}",
                (csm, value) => csm.LinkerSites[index].Accession = value);

            Register<string>($"Sequence {discriminator}",
                (csm, value) => csm.LinkerSites[index].Sequence = value);

            Register<int>($"{discriminator} in protein",
                (csm, value) => csm.LinkerSites[index].ProteinLink = value);

            Register<int>($"Crosslinker Position {discriminator}",
                (csm, value) => csm.LinkerSites[index].PeptideLink = value);
        }
    }
}