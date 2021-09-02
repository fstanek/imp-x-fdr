using IMP_X_FDR.Constants;
using IMP_X_FDR.Models;
using Microsoft.Win32;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using ColorDialog = System.Windows.Forms.ColorDialog;
using DialogResult = System.Windows.Forms.DialogResult;

namespace IMP_X_FDR.Controls
{
    /// <summary>
    /// Interaction logic for VennyInputPanel.xaml
    /// </summary>
    public partial class VennyInputPanel : UserControl
    {
        private readonly ColorDialog colorDialog = new ColorDialog { AllowFullOpen = true };
        private readonly OpenFileDialog openFileDialog = new OpenFileDialog { Filter = FileFilters.Excel };

        public VennyInputPanel()
        {
            InitializeComponent();
        }

        private void ColorButton_Click(object sender, RoutedEventArgs e)
        {
            var vennSegment = DataContext as VennSegment;
            colorDialog.Color = vennSegment.GetSystemColor();

            if (colorDialog.ShowDialog() == DialogResult.OK)
                vennSegment.SetSystemColor(colorDialog.Color);
        }

        private void BrowseButton_Click(object sender, RoutedEventArgs e)
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