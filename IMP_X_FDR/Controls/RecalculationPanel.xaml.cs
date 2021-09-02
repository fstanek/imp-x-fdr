using IMP_X_FDR.Constants;
using IMP_X_FDR.Utils;
using Microsoft.Win32;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

namespace IMP_X_FDR.Controls
{
    /// <summary>
    /// Interaction logic for RecalculationPanel.xaml
    /// </summary>
    public partial class RecalculationPanel : DockPanel
    {
        private readonly OpenFileDialog inputFileDialog = new OpenFileDialog { Filter = FileFilters.All };
        private readonly OpenFileDialog libraryFileDialog = new OpenFileDialog { Filter = FileFilters.Excel };
        private readonly SaveFileDialog outputFileDialog = new SaveFileDialog { Filter = FileFilters.Csv };

        public RecalculationPanel()
        {
            InitializeComponent();
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
                var inputFileName = default(string);

                if(configuration.SearchEngine.FileConverter != null)
                {
                    inputFileName = Path.GetTempFileName();
                    configuration.SearchEngine.FileConverter.Convert(configuration.InputFileName, inputFileName);
                }

                var scriptFileName = configuration.SearchEngine.ReferenceScript ?? configuration.SearchEngine.ScriptName;
                var arguments = configuration.GetArguments(inputFileName).ToArray();
                PythonHelper.Run(scriptFileName, arguments, logPanel.AddMessage);

                if (File.Exists(inputFileName))
                    File.Delete(inputFileName);

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