using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    internal class AnnikaXLFormatHandler : FormatHandlerBase<ExcelReader>
    {
        public override string DisplayName => "Annika crosslinks";
        public override bool IsGrouped => true;

        protected override void Initialize()
        {
            Register<double>("Best CSM Score", (csm, value) => csm.Score = value);
            RegisterHandlers(c => c.Site1, "A");
            RegisterHandlers(c => c.Site2, "B");
        }

        private void RegisterHandlers(Func<Crosslink, LinkerSite> selector, string discriminator)
        {
            Register<string>($"Accession {discriminator}",
                (csm, value) => selector(csm).Accession = value);

            Register<string>($"Sequence {discriminator}",
                (csm, value) => selector(csm).Sequence = value);

            Register<int>($"In protein {discriminator}",
                (csm, value) => selector(csm).ProteinLink = value);

            Register<int>($"Position {discriminator}",
                (csm, value) => selector(csm).PeptideLink = value);
        }
    }
}
