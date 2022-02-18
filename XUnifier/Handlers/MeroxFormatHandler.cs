using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public class MeroxFormatHandler : IFormatHandler
    {
        public const int Accession1 = 7;
        public const int Sequence1 = 6;
        public const int ProteinLink1 = 8;
        public const int PeptideLink1 = 20;

        public const int Accession2 = 11;
        public const int Sequence2 = 10;
        public const int ProteinLink2 = 12;
        public const int PeptideLink2 = 21;

        public const int Score = 0;

        public string DisplayName => "MeroX";
        public Type ReaderType => typeof(MeroxReader);

        public IEnumerable<Func<TableReader<CrosslinkSpectrumMatch>, bool>> ColumnHandlers
        {
            get
            {
                return GetColumnHandlers(0, Accession1, Sequence1, ProteinLink1, PeptideLink1).Concat(
                    GetColumnHandlers(1, Accession2, Sequence2, ProteinLink2, PeptideLink2))
                    .Append(reader => reader.Register<double>(Score, (csm, value) => csm.Score = value));
            }
        }

        private IEnumerable<Func<TableReader<CrosslinkSpectrumMatch>, bool>> GetColumnHandlers(int index, int accession, int sequence, int proteinLink, int peptideLink)
        {
            yield return reader => reader.Register<string>(accession,
                (csm, value) => csm.LinkerSites[index].Accession = value);

            yield return reader => reader.Register<string>(sequence,
                (csm, value) => csm.LinkerSites[index].Sequence = value.Trim('[', ']'));

            yield return reader => reader.Register<int>(proteinLink,
                (csm, value) => csm.LinkerSites[index].ProteinLink = value);

            yield return reader => reader.Register<string>(peptideLink,
                (csm, value) => csm.LinkerSites[index].PeptideLink = int.Parse(value.Substring(1)));
        }
    }
}