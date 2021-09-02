using IMP_X_FDR.Utils;
using System.Collections.Generic;

namespace IMP_X_FDR.Models
{
    public abstract class JobConfiguration : ConfigurationBase
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

        public override IEnumerable<string> GetArguments(string inputFileName = null)
        {
            yield return inputFileName ?? InputFileName;
            yield return LibraryFileName;
            yield return OutputFileName;
        }

        public override void Reset()
        {
            InputFileName = null;
            OutputFileName = null;
            LibraryFileName = ScriptHelper.GetDefaultLibraryFileName();
        }
    }
}