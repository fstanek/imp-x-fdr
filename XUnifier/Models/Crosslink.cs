using System.Diagnostics;

namespace XUnifier.Models
{
    [DebuggerDisplay("{Site1.Sequence}:{Site2.Sequence}")]
    public class Crosslink : IEquatable<Crosslink>
    {
        public LinkerSite Site1 { get; set; }
        public LinkerSite Site2 { get; set; }
        public double Score { get; set; }
        public bool IsDecoy { get; set; }

        public bool IsHomeotypic => Site1.Sequence == Site2.Sequence;

        public Crosslink()
        {
            Site1 = new LinkerSite();
            Site2 = new LinkerSite();
        }

        public bool Equals(Crosslink? other)
        {
            return Site1 == other.Site1
                && Site2 == other.Site2
                && Score == other.Score;
        }

        public override int GetHashCode()
        {
            return Site1.GetHashCode() + Site2.GetHashCode() + Score.GetHashCode();
        }
    }
}