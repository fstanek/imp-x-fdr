using FDRCheck.Models;
using System;
using System.Threading.Tasks;
using System.Windows.Controls;

namespace FDRCheck.Controls
{
    /// <summary>
    /// Interaction logic for LogPanel.xaml
    /// </summary>
    public partial class LogPanel : GroupBox
    {
        public LogPanel()
        {
            InitializeComponent();
        }

        public async Task AddMessage(string text, bool isError)
        {
            await Dispatcher.InvokeAsync(() =>
            {
                var logMessage = new LogMessage
                {
                    DateTime = DateTime.Now,
                    Text = text,
                    IsError = isError
                };

                logMessages.Add(logMessage);
                logViewer.ScrollToEnd();
            });
        }
    }
}