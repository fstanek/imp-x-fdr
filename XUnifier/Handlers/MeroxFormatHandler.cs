﻿using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class MeroxFormatHandler : FormatHandlerBase<MeroxReader>
    {
        public const int Score = 0;

        public const int Accession1 = 7;
        public const int Sequence1 = 6;
        public const int ProteinLink1 = 8;
        public const int PeptideLink1 = 20;

        public const int Accession2 = 11;
        public const int Sequence2 = 10;
        public const int ProteinLink2 = 12;
        public const int PeptideLink2 = 21;

        public override string DisplayName => "MeroX";

        protected override void Initialize()
        {
            Register<double>(Score, (csm, value) => csm.Score = value);
            RegisterColumns(c => c.Site1, Accession1, Sequence1, ProteinLink1, PeptideLink1);
            RegisterColumns(c => c.Site2, Accession2, Sequence2, ProteinLink2, PeptideLink2);
        }

        private void RegisterColumns(Func<Crosslink, LinkerSite> selector, int accession, int sequence, int proteinLink, int peptideLink)
        {
            Register<string>(accession,
                (csm, value) => selector(csm).Accession = value);

            Register<string>(sequence,
                (csm, value) => selector(csm).Sequence = value.Trim('[', ']'));

            Register<int>(proteinLink,
                (csm, value) => selector(csm).ProteinLink = value);

            Register<string>(peptideLink,
                (csm, value) => selector(csm).PeptideLink = int.Parse(value.Substring(1)));
        }
    }
}