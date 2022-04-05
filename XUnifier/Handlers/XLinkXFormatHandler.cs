using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class XLinkXFormatHandler : FormatHandlerBase<ExcelReader>
    {
        public override string DisplayName => "XlinkX";
        public override bool IsGrouped => false;

        protected override void Initialize()
        {
            RegisterColumns(c => c.Site1, "A");
            RegisterColumns(c => c.Site2, "B");
            Register<double>("XlinkX Score", (csm, value) => csm.Score = value);
        }

        private void RegisterColumns(Func<Crosslink, LinkerSite> selector, string discriminator)
        {
            Register<string>($"Protein Accession {discriminator}",
               (csm, value) => selector(csm).Accession = value);

            Register<string>($"Sequence {discriminator}",
                (csm, value) => selector(csm).Sequence = value);

            Register<int>($"Leading Protein Position {discriminator}",
                (csm, value) => selector(csm).ProteinLink = value);

            Register<int>($"Crosslinker Position {discriminator}",
                (csm, value) => selector(csm).PeptideLink = value);
        }
    }
}