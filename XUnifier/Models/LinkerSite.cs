namespace XUnifier.Models
{
    public class LinkerSite
    {
        public string Accession { get; set; }
        public string Sequence { get; set; }

        public int ProteinLink { get; set; }
        public int PeptideLink { get; set; }
    }
}