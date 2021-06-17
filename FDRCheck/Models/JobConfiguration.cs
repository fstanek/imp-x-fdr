using System.Collections.Generic;
using System.Collections.ObjectModel;

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

        public ObservableCollection<LogMessage> LogMessages { get; } = new ObservableCollection<LogMessage>();

        public JobConfiguration()
        {
            inputFileName = @"C:\Users\stanek\Documents\test files\test-data_Adrian\plink\DSSO_peplib2_rep2_plink.csv";
            libraryFileName = @"C:\Users\stanek\Documents\test files\test-data_Adrian\plink\DSSO_peplib2_rep2_plink.csv";
            outputFileName = @"C:\Users\stanek\Documents\test files\test-data_Adrian\plink\DSSO_peplib2_rep2_plink.xlsx";
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
                DisplayName = "Test",
                ScriptName = "Resources/scripts/test.py"
            },
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