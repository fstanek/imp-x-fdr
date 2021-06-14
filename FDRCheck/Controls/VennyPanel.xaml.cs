using FDRCheck.Constants;
using Microsoft.Win32;
using System.Linq;
using System.Windows;
using System.Windows.Controls;

namespace FDRCheck.Controls
{
    /// <summary>
    /// Interaction logic for VennyPanel.xaml
    /// </summary>
    public partial class VennyPanel : UserControl
    {
        private readonly SaveFileDialog saveFileDialog = new SaveFileDialog { Filter = FileFilters.Excel };

        public VennyPanel()
        {
            InitializeComponent();
        }

        private void BrowseOutput_Click(object sender, RoutedEventArgs e)
        {
            if(saveFileDialog.ShowDialog(Window.GetWindow(this)) == true)
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
            if(distinctFileNames.Length < validSegments.Length)
            {
                ShowError("There are duplicate file names specified.");
                return;
            }
        }

        private void Open_Click(object sender, RoutedEventArgs e)
        {

        }

        private void Clear_Click(object sender, RoutedEventArgs e)
        {

        }

        private void ShowError(string text)
        {
            MessageBox.Show(Window.GetWindow(this), text, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }
    }
}