using IMP_X_FDR.Converters;

namespace IMP_X_FDR.Models
{
    public class SearchEngine
    {
        public string DisplayName { get; set; }
        public string ScriptName { get; set; }

        public string ReferenceScript { get; set; }
        public IFileConverter FileConverter { get; set; }

        // TODO extended parameters (merox)
    }
}