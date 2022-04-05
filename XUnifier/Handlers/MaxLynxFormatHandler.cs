using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class MaxLynxFormatHandler : FormatHandlerBase<CommaSeparatedReader>
    {
        public override string DisplayName => "MaxLynX";
        public override bool IsGrouped => false;

        protected override void Initialize()
        {
            Register<double>("Score", (c, value) => c.Score = value);

            Register<string>("Proteins1", (c, value) => c.Site1.Accession = value);
            Register<string>("Proteins2", (c, value) => c.Site2.Accession = value);

            Register<string>("Pro_InterLink1", (c, value) => c.Site1.ProteinLink = int.Parse(value.Trim(';')));
            Register<string>("Pro_InterLink2", (c, value) => c.Site2.ProteinLink = int.Parse(value.Trim(';')));

            Register<string>("Sequence1", (c, value) => c.Site1.Sequence = value);
            Register<string>("Sequence2", (c, value) => c.Site2.Sequence = value);

            Filter<string>("Sequence2", value => value != "-");
        }
    }
}