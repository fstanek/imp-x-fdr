using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class MeroxFormatHandler : FormatHandlerBase<MeroxReader>
    {
        public override string DisplayName => "MeroX";
        public override bool IsGrouped => false;

        protected override void Initialize()
        {
            Register<double>(0, (csm, value) => csm.Score = value);

            Register<string>(6, (csm, value) => csm.Site1.Sequence = GetSequence(value), FilterSequence);
            Register<string>(10, (csm, value) => csm.Site2.Sequence = GetSequence(value), FilterSequence);

            Register<string>(7, (csm, value) => csm.Site1.Accession = value);
            Register<string>(11, (csm, value) => csm.Site2.Accession = value);

            Register<string>(20, (csm, value) => csm.Site1.PeptideLink = GetPeptideLink(value));
            Register<string>(21, (csm, value) => csm.Site2.PeptideLink = GetPeptideLink(value));

            Register<int>(8, (csm, value) => csm.Site1.ProteinLink = csm.Site1.PeptideLink + value);
            Register<int>(12, (csm, value) => csm.Site2.ProteinLink = csm.Site2.PeptideLink + value);
        }

        private string GetSequence(string value)
        {
            return value.Trim("[]{}".ToArray()).ToUpper().Replace('B', 'C');
        }

        private bool FilterSequence(string sequence)
        {
            return sequence != "0" && sequence != "1";
        }

        private int GetPeptideLink(string value)
        {
            return int.Parse(value.Substring(1)) - 1;
        }
    }
}