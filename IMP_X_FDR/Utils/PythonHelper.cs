﻿using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace IMP_X_FDR.Utils
{
    public static class PythonHelper
    {
        private const string RequirementsPath = "Resources/requirements.txt";

        private static string pythonPath;
        public static bool IsPythonInstalled => pythonPath != null;

        public static void Initialize()
        {
            pythonPath = new[]
            {
                "python.exe",
                FromRegistryKey(Registry.CurrentUser),
                FromRegistryKey(Registry.LocalMachine)
            }.FirstOrDefault(ValidatePythonPath);

            if(IsPythonInstalled)
                TryInstallPackages();
        }

        private static string FromRegistryKey(RegistryKey registryKey)
        {
            const string Key64 = @"Software\Wow6432Node\Python\PythonCore";
            const string Key32 = @"Software\Python\PythonCore";

            var pythonCore = registryKey.OpenSubKey(Key64) ?? registryKey.OpenSubKey(Key32);
            if (pythonCore != null)
            {
                var version = pythonCore.GetSubKeyNames().LastOrDefault();

                if (version != null)
                {
                    var installPath = pythonCore?.OpenSubKey($@"{version}\InstallPath");
                    return installPath?.GetValue("ExecutablePath") as string;
                }
            }

            return null;
        }

        private static bool ValidatePythonPath(string path)
        {
            if (string.IsNullOrWhiteSpace(path))
                return false;

            try
            {
                return Run(path, "--version", 1000);
            }
            catch
            {
                return false;
            }
        }

        private static bool Run(string fileName, string arguments, int? milliseconds = default)
        {
            using var process = new Process();
            process.StartInfo.FileName = fileName;
            process.StartInfo.Arguments = "--version";
            process.StartInfo.UseShellExecute = true;
#if !DEBUG
            process.StartInfo.CreateNoWindow = true;
#endif
            process.Start();

            if (milliseconds.HasValue)
                process.WaitForExit(milliseconds.Value);
            else
                process.WaitForExit();

            return process.ExitCode == 0;
        }

        private static void TryInstallPackages()
        {
            Run(pythonPath, $"-m pip install -r {RequirementsPath}");
        }

        public static void Run(string scriptFileName, IEnumerable<string> arguments, Func<string, bool, Task> messageHandler)
        {
            scriptFileName = Path.GetFullPath(scriptFileName);

            using var process = new Process();
            process.StartInfo.FileName = pythonPath;
            process.StartInfo.WorkingDirectory = Path.GetDirectoryName(scriptFileName);
            process.StartInfo.CreateNoWindow = true;

            //process.StartInfo.ArgumentList.Add("-u");
            process.StartInfo.ArgumentList.Add(scriptFileName);

            foreach (var argument in arguments)
                process.StartInfo.ArgumentList.Add(argument.ToString());

            process.StartInfo.RedirectStandardOutput = true;
            process.OutputDataReceived += (s, e) => OnMessageReceived(e, messageHandler, false);

            process.StartInfo.RedirectStandardError = true;
            process.ErrorDataReceived += (s, e) => OnMessageReceived(e, messageHandler, true);

            messageHandler?.Invoke($"Script started: {scriptFileName}", false);

            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();
            process.WaitForExit();

            var result = process.ExitCode == 0 ? "successfully" : "with errors";
            messageHandler?.Invoke($"Script finished {result}.", false);
        }

        private static void OnMessageReceived(DataReceivedEventArgs dataReceivedEventArgs, Func<string, bool, Task> messageHandler, bool isError)
        {
            if (dataReceivedEventArgs.Data != null)
                messageHandler?.Invoke(dataReceivedEventArgs.Data, isError);
        }
    }
}