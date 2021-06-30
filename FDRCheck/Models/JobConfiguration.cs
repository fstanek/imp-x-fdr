using FDRCheck.Utils;
using System.Collections.Generic;
using System.IO;

namespace FDRCheck.Models
{
    public class JobConfiguration : BaseModel
    {
        private string inputFileName;
        private string libraryFileName;
        private string outputFileName;
        private bool isIdle = true;

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

        public bool IsIdle
        {
            get => isIdle;
            set { isIdle = value; OnPropertyChanged(nameof(IsIdle)); }
        }

        public JobConfiguration()
        {
            LibraryFileName = Path.GetFullPath("Resources/libraries/support.xlsx");
            SearchEngines = new SearchEngineCollection(ScriptHelper.GetSearchEngines());
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
        public SearchEngineCollection SearchEngines { get; set; }
    }
}