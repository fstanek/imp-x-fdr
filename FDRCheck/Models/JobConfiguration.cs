﻿using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace FDRCheck.Models
{
    public class JobConfiguration : ConfigurationBase
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

        public SearchEngine SearchEngine { get; set; }
        public ObservableCollection<SearchEngine> SearchEngines { get; } = new ObservableCollection<SearchEngine>();

        public override string ScriptName => SearchEngine.ScriptName;

        public override IEnumerable<string> GetArguments()
        {
            yield return InputFileName;
            yield return LibraryFileName;
            yield return OutputFileName;
        }

        public override void Clear()
        {
            InputFileName = null;
            LibraryFileName = null;
            OutputFileName = null;
        }
    }
}