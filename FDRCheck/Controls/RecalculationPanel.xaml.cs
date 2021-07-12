using FDRCheck.Constants;
using FDRCheck.Utils;
using Microsoft.Win32;
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
        private readonly OpenFileDialog inputFileDialog = new OpenFileDialog { Filter = FileFilters.All };
        private readonly OpenFileDialog libraryFileDialog = new OpenFileDialog { Filter = FileFilters.Excel };
        private readonly SaveFileDialog outputFileDialog = new SaveFileDialog { Filter = FileFilters.Csv };

        public RecalculationPanel()
        {
            InitializeComponent();

            pythonEngine.MessageReceived += logPanel.AddMessage;
            jobConfiguration.LibraryFileName = Path.GetFullPath("Resources/libraries/support.xlsx");

            foreach (var searchEngine in ScriptHelper.GetSearchEngines("Resources/search-engines/"))
                jobConfiguration.SearchEngines.Add(searchEngine);
        }

        private void BrowseInput_Click(object sender, RoutedEventArgs e)
        {
            if (inputFileDialog.ShowDialog(Window.GetWindow(this)) == true)
            {
                jobConfiguration.InputFileName = inputFileDialog.FileName;

                if (string.IsNullOrWhiteSpace(jobConfiguration.OutputFileName))
                    jobConfiguration.OutputFileName = Path.GetDirectoryName(jobConfiguration.InputFileName);
            }
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
                WindowHelper.ShowError(this, "Input file does not exist.");
                return;
            }

            if (!File.Exists(jobConfiguration.LibraryFileName))
            {
                WindowHelper.ShowError(this, "Library file does not exist.");
                return;
            }

            if (!FileHelper.IsValidFileName(jobConfiguration.OutputFileName))
            {
                WindowHelper.ShowError(this, "Invalid output path.");
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
            jobConfiguration.Clear();
        }
    }
}