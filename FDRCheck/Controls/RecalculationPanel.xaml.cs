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
        }

        private void BrowseInput_Click(object sender, RoutedEventArgs e)
        {
            if (inputFileDialog.ShowDialog(Window.GetWindow(this)) == true)
            {
                configuration.InputFileName = inputFileDialog.FileName;
                configuration.OutputFileName = FileHelper.GetOutputFileName(configuration.InputFileName, ".csv");
            }
        }

        private void BrowseLibrary_Click(object sender, RoutedEventArgs e)
        {
            if (libraryFileDialog.ShowDialog(Window.GetWindow(this)) == true)
                configuration.LibraryFileName = libraryFileDialog.FileName;
        }

        private void BrowseOutput_Click(object sender, RoutedEventArgs e)
        {
            if (outputFileDialog.ShowDialog(Window.GetWindow(this)) == true)
                configuration.OutputFileName = outputFileDialog.FileName;
        }

        private void Run_Click(object sender, RoutedEventArgs e)
        {
            if (!File.Exists(configuration.InputFileName))
            {
                WindowHelper.ShowError(this, "Input file does not exist.");
                return;
            }

            if (!File.Exists(configuration.LibraryFileName))
            {
                WindowHelper.ShowError(this, "Library file does not exist.");
                return;
            }

            if (!FileHelper.IsValidFileName(configuration.OutputFileName))
            {
                WindowHelper.ShowError(this, "Invalid output path.");
                return;
            }

            Task.Run(() =>
            {
                configuration.IsIdle = false;
                pythonEngine.Run(configuration.SearchEngine.ScriptName, configuration.Arguments);
                configuration.IsIdle = true;
            });
        }

        private void Open_Click(object sender, RoutedEventArgs e)
        {
            FileHelper.TryOpenDirectory(configuration.OutputFileName);
        }

        private void Clear_Click(object sender, RoutedEventArgs e)
        {
            configuration.Reset();
        }
    }
}