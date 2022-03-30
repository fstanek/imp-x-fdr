namespace XUnifier.Models
{
    public class Crosslink : IEquatable<Crosslink>
    {
        public LinkerSiteCollection LinkerSites { get; set; }
        public double Score { get; set; }
        public bool Intra => LinkerSites.Select(s => s.Accession).Distinct().Count() == 1;

        public Crosslink()
        {
            LinkerSites = new LinkerSiteCollection();
        }

        public bool Equals(Crosslink? other)
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