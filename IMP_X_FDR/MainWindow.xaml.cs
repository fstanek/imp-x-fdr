using IMP_X_FDR.Utils;
using System.Windows;

namespace IMP_X_FDR
{
    /// <summary>
    /// Interaction logic for JobDialog.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            PythonHelper.Initialize();

            if (!PythonHelper.IsPythonInstalled)
            {
                MessageBox.Show(this, "No python installation found.\nDownload newest version from www.python.org/downloads/", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                Application.Current.Shutdown();
            }
        }
    }
}