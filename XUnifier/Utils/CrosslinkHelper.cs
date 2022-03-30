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
                csm.Site1.Sequence,
                csm.Site2.Sequence,
                csm.Score.ToString(CultureInfo.InvariantCulture),
                csm.Site1.Accession,
                csm.Site2.Accession,
                csm.Site1.ProteinLink,
                csm.Site2.ProteinLink);
        }
    }
}