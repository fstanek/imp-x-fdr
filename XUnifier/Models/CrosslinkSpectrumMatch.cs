namespace XUnifier.Models
{
    public class CrosslinkSpectrumMatch : IEquatable<CrosslinkSpectrumMatch>
    {
        public LinkerSiteCollection LinkerSites { get; set; }
        public double Score { get; set; }
        public CrosslinkType CrosslinkType { get; set; }

        public CrosslinkSpectrumMatch()
        {
            LinkerSites = new LinkerSiteCollection();
        }

        public bool Equals(CrosslinkSpectrumMatch? other)
        {
            if (other is null)
                return false;

            return LinkerSites.ToHashSet().SetEquals(other.LinkerSites);
        }

        public override int GetHashCode()
        {
            return LinkerSites.Sum(s => s.GetHashCode());
        }
    }
}