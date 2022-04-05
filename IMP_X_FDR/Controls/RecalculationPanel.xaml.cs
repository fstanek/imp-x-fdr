using IMP_X_FDR.Constants;
using IMP_X_FDR.Utils;
using Microsoft.Win32;
using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using XUnifier;
using XUnifier.Models;
using XUnifier.Utils;

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

#if !DEBUG
            Task.Run(async () =>
            {
                try
                {
#endif
            configuration.IsIdle = false;
                //var inputFileName = default(string);

                logPanel.AddMessage("Reading crosslinks from file...");
                var items = CrosslinkReaderFactory.GetCrosslinks(configuration.InputFileName, out var isGrouped).ToArray();
                logPanel.AddMessage($"{items.Length} crosslinks found.");

                if (!isGrouped && configuration.GroupCSMs)
                {
                    items = CrosslinkReaderFactory.Group(items).ToArray();
                    logPanel.AddMessage($"Grouped to {items.Length} unique crosslinks.");
                }

                items = CrosslinkReaderFactory.Order(items).ToArray();

                using var pythonHandler = PythonHelper.CreateHandler();
                pythonHandler.AddArgument(configuration.ScriptName);
                pythonHandler.AddArgument(configuration.LibraryFileName);
                pythonHandler.AddArgument(configuration.OutputFileName);

                pythonHandler.AddArgument((isGrouped || configuration.GroupCSMs).ToString());

                pythonHandler.OutputReceived += text => logPanel.AddMessage(text, false);
                pythonHandler.ErrorReceived += text => logPanel.AddMessage(text, true);
#if DEBUG
                pythonHandler.OutputReceived += text => Debug.WriteLine(text);
                pythonHandler.ErrorReceived += text => Debug.WriteLine($"ERROR: {text}");
#endif
            var exitCode = pythonHandler.Run(items.Select(CrosslinkHelper.GetLine));

                //var arguments = configuration.GetArguments(inputFileName).ToArray();
                //PythonHelper.Run(configuration.ScriptName, arguments, logPanel.AddMessage);

                //if (File.Exists(inputFileName))
                //    File.Delete(inputFileName);

                logPanel.AddMessage("Script finished.", false);
#if !DEBUG
            }
                catch (Exception e)
                {
                    logPanel.AddMessage(e.ToString(), true);
                }

                configuration.IsIdle = true;
            });
#else
            configuration.IsIdle = true;
#endif
        }

        private void Open_Click(object sender, RoutedEventArgs e)
        {
            FileHelper.TryOpenDirectory(configuration.OutputFileName);
        }

        private void Clear_Click(object sender, RoutedEventArgs e)
        {
            configuration.Reset();
        }

        private void DockPanel_Loaded(object sender, RoutedEventArgs e)
        {
#if DEBUG
            //configuration.InputFileName = @"C:\Users\stanek\Documents\test files\imp-x-fdr\Annika\reanal_pl1_DSSO_Annika_standard_pepength7.xlsx";
            //configuration.OutputFileName = FileHelper.GetOutputFileName(configuration.InputFileName, ".csv");

            configuration.InputFileName = @"C:\Users\stanek\Documents\test files\imp-x-fdr\MeroX\rep3_DSSO-pl1_KSTY.zhrm";
            configuration.OutputFileName = FileHelper.GetOutputFileName(configuration.InputFileName, ".csv");
#endif
        }
    }
}