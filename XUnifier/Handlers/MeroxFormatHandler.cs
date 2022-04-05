using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class MeroxFormatHandler : FormatHandlerBase<MeroxReader>
    {
        public const int Score = 0;

        public const int Accession1 = 7;
        public const int Accession2 = 11;

        public const int Sequence1 = 6;
        public const int Sequence2 = 10;

        public const int ProteinLink1 = 8;
        public const int ProteinLink2 = 12;

        public const int PeptideLink1 = 20;
        public const int PeptideLink2 = 21;

        public override string DisplayName => "MeroX";
        public override bool IsGrouped => false;

        protected override void Initialize()
        {
            Register<double>(Score, (csm, value) => csm.Score = value);

            Register<string>(Accession1, (csm, value) => csm.Site1.Accession = value);
            Register<string>(Accession2, (csm, value) => csm.Site2.Accession = value);

            Register<string>(Sequence1, (csm, value) => csm.Site1.Sequence = GetSequence(value));
            Register<string>(Sequence2, (csm, value) => csm.Site2.Sequence = GetSequence(value));

            Register<int>(ProteinLink1, (csm, value) => csm.Site1.ProteinLink = value);
            Register<int>(ProteinLink2, (csm, value) => csm.Site2.ProteinLink = value);

            Register<string>(PeptideLink1, (csm, value) => csm.Site1.PeptideLink = GetPeptideLink(value));
            Register<string>(PeptideLink2, (csm, value) => csm.Site2.PeptideLink = GetPeptideLink(value));
        }

        private string GetSequence(string value)
        {
            return value.Trim("[]{}".ToArray()).ToUpper();
        }

        private int GetPeptideLink(string value)
        {
            return int.Parse(value.Substring(1));
        }
    }
}