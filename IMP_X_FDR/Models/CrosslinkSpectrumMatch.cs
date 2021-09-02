namespace IMP_X_FDR.Models
{
    public class CrosslinkSpectrumMatch
    {
        public float Score { get; set; }

        public string Protein1 { get; set; }
        public string Protein2 { get; set; }

        public int ProInterLink1 { get; set; }
        public int ProInterLink2 { get; set; }

        public string Sequence1 { get; set; }
        public string Sequence2 { get; set; }
    }
}