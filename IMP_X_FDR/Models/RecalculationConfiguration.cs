namespace IMP_X_FDR.Models
{
    public class RecalculationConfiguration : JobConfiguration
    {
        private bool groupCSMs;

        public override string ScriptName => "Resources/search-engines/annika_master_score.py";

        public bool GroupCSMs
        {
            get => groupCSMs;
            set { groupCSMs = value; OnPropertyChanged(nameof(GroupCSMs)); }
        }
    }
}