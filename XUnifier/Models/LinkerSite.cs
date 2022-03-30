namespace XUnifier.Models
{
    public class LinkerSite : IEquatable<LinkerSite>
    {
        public string Accession { get; set; }
        public string Sequence { get; set; }

        public int ProteinLink { get; set; }
        public int PeptideLink { get; set; }

        public bool Equals(LinkerSite? other)
        {
            return Accession == other.Accession
                && ProteinLink == other.ProteinLink;
        }

        public override int GetHashCode()
        {
            return Accession.GetHashCode() * ProteinLink.GetHashCode();
        }
    }
}