using System.Collections.Generic;

namespace FDRCheck.Models
{
    public class AnnikaConfiguration : ConfigurationBase
    {
        private string inputFileName;
        private string libraryFileName;
        private string outputFolderName;
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

        public string OutputFolderName
        {
            get => outputFolderName;
            set { outputFolderName = value; OnPropertyChanged(nameof(OutputFolderName)); }
        }

        public bool IsIdle
        {
            get => isIdle;
            set { isIdle = value; OnPropertyChanged(nameof(IsIdle)); }
        }

        public override string ScriptName => "Resources/annika_master_score.py";

        public override IEnumerable<string> GetArguments()
        {
            yield return InputFileName;
            yield return LibraryFileName;
            yield return OutputFolderName;
        }

        public override void Clear()
        {
            InputFileName = null;
            LibraryFileName = null;
            OutputFolderName = null;
        }
    }
}