using System.Diagnostics.CodeAnalysis;
using XUnifier.Models;

namespace XUnifier.Utils
{
    public class LinkerSiteCollectionEqualityComparer : IEqualityComparer<LinkerSiteCollection>, IEqualityComparer<LinkerSite>
    {
        public bool Equals(LinkerSite? site1, LinkerSite? site2)
        {
            return site1?.Accession == site2?.Accession
                && site1.Sequence == site2?.Sequence
                && site1.ProteinLink == site2?.ProteinLink
                && site1.PeptideLink == site2?.PeptideLink;
        }

        public int GetHashCode([DisallowNull] LinkerSite site)
        {
            return site.Accession?.GetHashCode() ?? 1
                 * site.Sequence?.GetHashCode() ?? 1
                 * site.ProteinLink.GetHashCode()
                 * site.PeptideLink.GetHashCode();
        }

        public bool Equals(LinkerSiteCollection? collection1, LinkerSiteCollection? collection2)
        {
            return collection1.All(l => collection2.Contains(l, this));
        }

        public int GetHashCode([DisallowNull] LinkerSiteCollection collection)
        {
            var hash = 42;

            foreach (var site in collection)
                return hash += GetHashCode(site);

            return hash;
        }
    }
}