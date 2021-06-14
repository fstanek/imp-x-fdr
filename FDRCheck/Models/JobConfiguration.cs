using System.Collections.Generic;

namespace FDRCheck.Models
{
    public class JobConfiguration : BaseModel
    {
        private string inputFileName;
        private string libraryFileName;
        private string outputFileName;

        public string InputFileName
        {
            get => inputFileName;
            set { inputFileName = value; OnPropertyChanged(nameof(InputFileName)); }
        }

        public string LibraryFileName
        {
            get => libraryFileName;
            set { libraryFileName = value; OnPropertyChanged(nameof(LibraryFileName)); }
        }

        public string OutputFileName
        {
            get => outputFileName;
            set { outputFileName = value; OnPropertyChanged(nameof(OutputFileName)); }
        } 

        public void Reset()
        {
            InputFileName = null;
            LibraryFileName = null;
            OutputFileName = null;
        }

        public virtual IEnumerable<string> GetArguments()
        {
            yield return InputFileName;
            yield return LibraryFileName;
            yield return OutputFileName;
        }

        public SearchEngine SearchEngine { get; set; }

        // TODO read from json
        public SearchEngineCollection SearchEngines { get; set; } = new SearchEngineCollection
        {
            new SearchEngine
            {
                DisplayName = "MeroX",
                ScriptName = "Resources/scripts/merox_master.py"
            },
            new SearchEngine
            {
                DisplayName = "MS Annika",
                ScriptName = "Resources/scripts/annika_master_score.py"
            },
            new SearchEngine
            {
                DisplayName = "PLINK",
                ScriptName = "Resources/scripts/plink_master_score.py"
            },
            new SearchEngine
            {
                DisplayName = "XlinkX",
                ScriptName = "Resources/scripts/xlinkx_master_score.py"
            },
        };
    }
}