using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class MaxLynxFormatHandler : FormatHandlerBase<CommaSeparatedReader>
    {
        public override string DisplayName => "MaxLynx";

        protected override void Initialize()
        {
            Register<double>("Score", (c, value) => c.Score = value);

            Register<string>("Protein1", (c, value) => c.Site1.Accession = value);
            Register<string>("Protein2", (c, value) => c.Site2.Accession = value);

            Register<int>("ProInterLink1", (c, value) => c.Site1.ProteinLink = value);
            Register<int>("ProInterLink2", (c, value) => c.Site2.ProteinLink = value);

            Register<string>("Sequence1", (c, value) => c.Site1.Sequence = value);
            Register<string>("Sequence2", (c, value) => c.Site2.Sequence = value);

            Filter<string>("Decoy", value => value == "forward");
        }
    }
}
