using FDRCheck.Constants;
using FDRCheck.Utils;
using Microsoft.Win32;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using DialogResult = System.Windows.Forms.DialogResult;
using FolderBrowserDialog = System.Windows.Forms.FolderBrowserDialog;

namespace FDRCheck.Controls
{
    /// <summary>
    /// Interaction logic for AnnikaPanel.xaml
    /// </summary>
    public partial class AnnikaPanel : DockPanel
    {
        private readonly PythonEngine pythonEngine = new PythonEngine();
        private readonly OpenFileDialog inputFileDialog = new OpenFileDialog { Filter = FileFilters.All };
        private readonly OpenFileDialog libraryFileDialog = new OpenFileDialog { Filter = FileFilters.Excel };
        private readonly FolderBrowserDialog outputFolderDialog = new FolderBrowserDialog();

        public AnnikaPanel()
        {
            InitializeComponent();

            pythonEngine.MessageReceived += logPanel.AddMessage;
        }

        private void BrowseInput_Click(object sender, RoutedEventArgs e)
        {
            if (inputFileDialog.ShowDialog(Window.GetWindow(this)) == true)
            {
                annikaConfiguration.InputFileName = inputFileDialog.FileName;
                annikaConfiguration.OutputFileName = FileHelper.GetOutputFolderName(annikaConfiguration.InputFileName);
            }
        }

        private void BrowseLibrary_Click(object sender, RoutedEventArgs e)
        {
            if (libraryFileDialog.ShowDialog(Window.GetWindow(this)) == true)
                annikaConfiguration.LibraryFileName = libraryFileDialog.FileName;
        }

        private void BrowseOutput_Click(object sender, RoutedEventArgs e)
        {
            if (outputFolderDialog.ShowDialog(WindowHelper.GetWin32Window(this)) == DialogResult.OK)
                annikaConfiguration.OutputFileName = outputFolderDialog.SelectedPath;
        }

        private void Run_Click(object sender, RoutedEventArgs e)
        {
            if (!File.Exists(annikaConfiguration.InputFileName))
            {
                WindowHelper.ShowError(this, "Input file does not exist.");
                return;
            }

            if (!File.Exists(annikaConfiguration.LibraryFileName))
            {
                WindowHelper.ShowError(this, "Library file does not exist.");
                return;
            }

            if (!FileHelper.IsValidFileName(annikaConfiguration.OutputFileName))
            {
                WindowHelper.ShowError(this, "Invalid output file path.");
                return;
            }

            Task.Run(() =>
            {
                annikaConfiguration.IsIdle = false;
                pythonEngine.Run(annikaConfiguration.ScriptName, annikaConfiguration.Arguments);
                annikaConfiguration.IsIdle = true;
            });
        }

        private void Open_Click(object sender, RoutedEventArgs e)
        {
            FileHelper.TryOpenDirectory(annikaConfiguration.OutputFileName);
        }

        private void Clear_Click(object sender, RoutedEventArgs e)
        {
            annikaConfiguration.Reset();
        }
    }
}