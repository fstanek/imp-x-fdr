using System.Globalization;
using XUnifier.Models;

namespace XUnifier.Utils
{
    public static class CrosslinkHelper
    {
        private const char Separator = '\t';

        public static string GetLine(Crosslink csm)
        {
            return string.Join(Separator,
                csm.LinkerSites[0].Sequence,
                csm.LinkerSites[1].Sequence,
                csm.Score.ToString(CultureInfo.InvariantCulture),
                csm.LinkerSites[0].Accession,
                csm.LinkerSites[1].Accession,
                csm.LinkerSites[0].ProteinLink,
                csm.LinkerSites[1].ProteinLink);
        }
    }
}