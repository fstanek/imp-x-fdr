using FDRCheck.Models;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;

namespace FDRCheck
{
    public class PythonEngine
    {
        private const string PythonPath = "Resources/python/python.exe";
        private const string ResultPrefix = "RESULT: ";

        public event Action<string> InfoReceived;
        public event Action<string> ErrorReceived;

        public string Run(string scriptFileName, string workingDirectory, IEnumerable<string> arguments)
        {
            var startInfo = new ProcessStartInfo
            {
                FileName = PythonPath,
                WorkingDirectory = workingDirectory,
                CreateNoWindow = true,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            };

            startInfo.ArgumentList.Add(scriptFileName);

            foreach (var argument in arguments)
                startInfo.ArgumentList.Add(argument.ToString());

            using var process = Process.Start(startInfo);
            var resultText = "";

            process.OutputDataReceived += (s, e) =>
            {
                if (string.IsNullOrWhiteSpace(e.Data))
                    return;

                if (e.Data.StartsWith(ResultPrefix))
                {
                    resultText = e.Data.Substring(0, ResultPrefix.Length);
                }
                else
                {
                    InfoReceived?.Invoke(e.Data);
                }
            };

            process.ErrorDataReceived += (s, e) =>
            {
                if (string.IsNullOrWhiteSpace(e.Data))
                    return;

                ErrorReceived?.Invoke(e.Data);
            };

            process.WaitForExit();
            return resultText;
        }

        public void Run(JobConfiguration jobConfiguration)
        {
            Run(jobConfiguration.SearchEngine.ScriptName,
                Path.GetDirectoryName(jobConfiguration.OutputFileName),
                jobConfiguration.GetArguments());
        }
    }
}