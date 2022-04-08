using IMP_X_FDR.Constants;
using IMP_X_FDR.Utils;
using Microsoft.Win32;
using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using XUnifier;
using XUnifier.Extensions;
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
                var rawItems = CrosslinkReaderFactory.GetCrosslinks(configuration.InputFileName, out var isGrouped).ToArray();
                logPanel.AddMessage($"{rawItems.Length} crosslinks found.");

            void PostprocessAccession(LinkerSite site)
            {
                var match = Regex.Match(site.Accession, @">[a-z]{2}\|(?<acc>[^ |]+)");
                if (match.Success)
                    site.Accession = match.GetString("acc");
            }

            foreach(var item in rawItems)
            {
                PostprocessAccession(item.Site1);
                PostprocessAccession(item.Site2);
            }

            rawItems = CrosslinkReaderFactory.Order(rawItems).ToArray();
            Crosslink[] items = rawItems.ToArray();

                if (!isGrouped && configuration.GroupCSMs)
                {
                    items = CrosslinkReaderFactory.Group(items).ToArray();
                    logPanel.AddMessage($"Grouped to {items.Length} unique crosslinks.");
                }

                using var pythonHandler = PythonHelper.CreateHandler();
            //pythonHandler.AddArgument(configuration.ScriptName);
                pythonHandler.AddArgument(@"Resources/search-engines/merox_new.py");
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
            configuration.InputFileName = @"C:\Users\stanek\Documents\test files\imp-x-fdr\MeroX\rep3_DSSO-pl1_KSTY.zhrm";
            //configuration.InputFileName = @"C:\Users\stanek\Documents\test files\imp-x-fdr\MeroX\pl1_DSSO_rep1_corrected_settings.zhrm";
            configuration.OutputFileName = FileHelper.GetOutputFileName(configuration.InputFileName, ".csv");
#endif
        }
    }
}