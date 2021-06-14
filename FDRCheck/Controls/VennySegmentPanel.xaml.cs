using FDRCheck.Constants;
using FDRCheck.Models;
using Microsoft.Win32;
using System.IO;
using System.Windows;
using System.Windows.Controls;

namespace FDRCheck.Controls
{
    /// <summary>
    /// Interaction logic for VennyInputPanel.xaml
    /// </summary>
    public partial class VennyInputPanel : UserControl
    {
        private readonly OpenFileDialog openFileDialog = new OpenFileDialog { Filter = FileFilters.Excel };

        public VennyInputPanel()
        {
            InitializeComponent();
        }

        private void ButtonBrowse_Click(object sender, RoutedEventArgs e)
        {
            if (openFileDialog.ShowDialog(Window.GetWindow(this)) == true)
            {
                var vennSegment = DataContext as VennSegment;
                vennSegment.FileName = openFileDialog.FileName;

                if (string.IsNullOrWhiteSpace(vennSegment.Title))
                    vennSegment.Title = Path.GetFileNameWithoutExtension(vennSegment.FileName);
            }
        }
    }
}