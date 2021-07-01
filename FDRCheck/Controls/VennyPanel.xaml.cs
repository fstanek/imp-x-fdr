using FDRCheck.Constants;
using FDRCheck.Utils;
using Microsoft.Win32;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

namespace FDRCheck.Controls
{
    /// <summary>
    /// Interaction logic for VennyPanel.xaml
    /// </summary>
    public partial class VennyPanel : DockPanel
    {
        private readonly PythonEngine pythonEngine = new PythonEngine();
        private readonly SaveFileDialog saveFileDialog = new SaveFileDialog { Filter = FileFilters.Excel };

        public VennyPanel()
        {
            InitializeComponent();

            pythonEngine.MessageReceived += logPanel.AddMessage;
        }

        private void BrowseOutput_Click(object sender, RoutedEventArgs e)
        {
            if (saveFileDialog.ShowDialog(Window.GetWindow(this)) == true)
                vennConfiguration.OutputFileName = saveFileDialog.FileName;
        }

        private void Run_Click(object sender, RoutedEventArgs e)
        {
            var validSegments = vennConfiguration.VennSegments.Where(s => s.IsValid).ToArray();

            if (validSegments.Length < 2)
            {
                ShowError("You need to specify at least two files.");
                return;
            }

            var distinctFileNames = validSegments.Select(s => s.FileName).Distinct().ToArray();
            if (distinctFileNames.Length < validSegments.Length)
            {
                ShowError("There are duplicate file names specified.");
                return;
            }

            if (!FileHelper.IsValidPath(vennConfiguration.OutputFileName))
            {
                ShowError("Output file path is invalid.");
                return;
            }

            var arguments = validSegments.SelectMany(s => new[] { s.FileName, s.Title, s.Color.Value.ToString() })
                .Prepend(vennConfiguration.OutputFileName).ToArray();

            Task.Run(() =>
            {
                vennConfiguration.IsIdle = false;
                pythonEngine.Run("Resources/venny.py", arguments);
                vennConfiguration.IsIdle = true;
            });
        }

        private void Open_Click(object sender, RoutedEventArgs e)
        {
            FileHelper.TryOpenDirectory(vennConfiguration.OutputFileName);
        }

        private void Clear_Click(object sender, RoutedEventArgs e)
        {
            vennConfiguration.Clear();
        }

        private void ShowError(string text)
        {
            MessageBox.Show(Window.GetWindow(this), text, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }
    }
}