namespace XUnifier.Models
{
    public class Crosslink /*: IEquatable<Crosslink>*/
    {
        //public LinkerSiteCollection LinkerSites { get; set; }
        public LinkerSite Site1 { get; set; }
        public LinkerSite Site2 { get; set; }
        public double Score { get; set; }

        public bool Intra => Site1 == Site2;

        public Crosslink()
        {
            Site1 = new LinkerSite();
            Site2 = new LinkerSite();
        }

        //public bool Equals(Crosslink? other)
        //{
        //    if (other is null)
        //        return false;

        //    return LinkerSites.ToHashSet().SetEquals(other.LinkerSites);
        //}

        //public override int GetHashCode()
        //{
        //    return LinkerSites.Sum(s => s.GetHashCode());
        //}
    }
}