using FDRCheck.Constants;
using FDRCheck.Models;
using FDRCheck.Utils;
using Microsoft.Win32;
using System;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

namespace FDRCheck.Controls
{
    /// <summary>
    /// Interaction logic for RecalculationPanel.xaml
    /// </summary>
    public partial class RecalculationPanel : DockPanel
    {
        private readonly PythonEngine pythonEngine = new PythonEngine();
        private readonly OpenFileDialog inputFileDialog = new OpenFileDialog();
        private readonly OpenFileDialog libraryFileDialog = new OpenFileDialog { Filter = FileFilters.Excel };
        private readonly SaveFileDialog outputFileDialog = new SaveFileDialog { Filter = FileFilters.Excel };

        public RecalculationPanel()
        {
            InitializeComponent();

            pythonEngine.MessageReceived += logPanel.AddMessage;
        }

        private void BrowseInput_Click(object sender, RoutedEventArgs e)
        {
            if (inputFileDialog.ShowDialog(Window.GetWindow(this)) == true)
                jobConfiguration.InputFileName = inputFileDialog.FileName;
        }

        private void BrowseLibrary_Click(object sender, RoutedEventArgs e)
        {
            if (libraryFileDialog.ShowDialog(Window.GetWindow(this)) == true)
                jobConfiguration.LibraryFileName = libraryFileDialog.FileName;
        }

        private void BrowseOutput_Click(object sender, RoutedEventArgs e)
        {
            if (outputFileDialog.ShowDialog(Window.GetWindow(this)) == true)
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

            if (!FileHelper.IsValidPath(jobConfiguration.OutputFileName))
            {
                ShowError("Invalid output file path.");
                return;
            }

            Task.Run(() =>
            {
                jobConfiguration.IsIdle = false;
                pythonEngine.Run(jobConfiguration.SearchEngine.ScriptName, jobConfiguration.GetArguments());
                jobConfiguration.IsIdle = true;
            });
        }

        private void Open_Click(object sender, RoutedEventArgs e)
        {
            FileHelper.TryOpenDirectory(jobConfiguration.OutputFileName);
        }

        private void Clear_Click(object sender, RoutedEventArgs e)
        {
            jobConfiguration.Reset();
        }

        private void ShowError(string text)
        {
            MessageBox.Show(Window.GetWindow(this), text, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        private void ComboBox_DropDownClosed(object sender, EventArgs e)
        {
            // TODO set search engine parameters
        }
    }
}