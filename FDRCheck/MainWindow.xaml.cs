using FDRCheck.Constants;
using Microsoft.Win32;
using System;
using System.Diagnostics;
using System.IO;
using System.Windows;

namespace FDRCheck
{
    /// <summary>
    /// Interaction logic for JobDialog.xaml
    /// </summary>
    public partial class JobDialog : Window
    {
        private readonly OpenFileDialog inputFileDialog = new OpenFileDialog();
        private readonly OpenFileDialog libraryFileDialog = new OpenFileDialog { Filter = FileFilters.Excel };
        private readonly SaveFileDialog outputFileDialog = new SaveFileDialog { Filter = FileFilters.Excel };
        private readonly PythonEngine pythonEngine = new PythonEngine();

        public JobDialog()
        {
            InitializeComponent();
        }

        private void BrowseInput_Click(object sender, RoutedEventArgs e)
        {
            if (inputFileDialog.ShowDialog(this) == true)
                jobConfiguration.InputFileName = inputFileDialog.FileName;
        }

        private void BrowseLibrary_Click(object sender, RoutedEventArgs e)
        {
                if (libraryFileDialog.ShowDialog(this) == true)
                jobConfiguration.LibraryFileName = libraryFileDialog.FileName;
        }

        private void BrowseOutput_Click(object sender, RoutedEventArgs e)
        {
            if (outputFileDialog.ShowDialog(this) == true)
                jobConfiguration.OutputFileName = outputFileDialog.FileName;
        }

        private void Run_Click(object sender, RoutedEventArgs e)
        {
            if (!File.Exists(jobConfiguration.InputFileName))
            {
                ShowError("Input file does not exist.");
                return;
            }

            if (!File.Exists(jobConfiguration.LibraryFileName))
            {
                ShowError("Library file does not exist.");
                return;
            }

            try
            {
                _ = new FileInfo(jobConfiguration.OutputFileName);
            }
            catch (Exception)
            {
                ShowError("Invalid output file path.");
                return;
            }

            pythonEngine.Run(jobConfiguration);
        }

        private void Open_Click(object sender, RoutedEventArgs e)
        {
            if (!string.IsNullOrWhiteSpace(jobConfiguration.OutputFileName))
            {
                var directoryInfo = new DirectoryInfo(jobConfiguration.OutputFileName);
                if (directoryInfo.Parent.Exists)
                    Process.Start("explorer.exe", directoryInfo.Parent.FullName);
            }
        }

        private void Clear_Click(object sender, RoutedEventArgs e)
        {
            jobConfiguration.Reset();
        }

        private void ShowError(string text)
        {
            MessageBox.Show(this, text, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        private void ComboBox_DropDownClosed(object sender, EventArgs e)
        {
            // TODO set search engine parameters
        }
    }
}