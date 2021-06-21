using FDRCheck.Utils;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;

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
            inputFileName = @"C:\Users\stanek\Documents\test files\test-data_Adrian\input files\DSSO_plink_rep1.csv";
            libraryFileName = @"C:\Users\stanek\Documents\test files\test-data_Adrian\support file\support.xlsx";
            outputFileName = @"C:\Users\stanek\Documents\test files\test-data_Adrian\output\plink.xlsx";

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