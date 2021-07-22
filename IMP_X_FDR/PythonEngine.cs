using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;

namespace IMP_X_FDR
{
    public class PythonEngine
    {
        private const string PythonPath = "Resources/python/python.exe";

        public event Func<string, bool, Task> MessageReceived;

        public void Run(string scriptFileName, IEnumerable<string> arguments)
        {
            using var process = new Process();
            process.StartInfo.FileName = PythonPath;
            process.StartInfo.WorkingDirectory = Path.GetDirectoryName(PythonPath);
            process.StartInfo.CreateNoWindow = true;

            process.StartInfo.ArgumentList.Add("-u");

            scriptFileName = Path.GetFullPath(scriptFileName);
            process.StartInfo.ArgumentList.Add(scriptFileName);

            foreach (var argument in arguments)
                process.StartInfo.ArgumentList.Add(argument.ToString());

            process.StartInfo.RedirectStandardOutput = true;
            process.OutputDataReceived += (s, e) => OnMessageReceived(e, false);

            process.StartInfo.RedirectStandardError = true;
            process.ErrorDataReceived += (s, e) => OnMessageReceived(e, true);

            MessageReceived?.Invoke($"Script started: {scriptFileName}", false);

            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();
            process.WaitForExit();

            var result = process.ExitCode == 0 ? "successfully" : "with errors";
            MessageReceived?.Invoke($"Script finished {result}.", false);
        }

        private void OnMessageReceived(DataReceivedEventArgs dataReceivedEventArgs, bool isError)
        {
            if (dataReceivedEventArgs.Data != null)
                MessageReceived?.Invoke(dataReceivedEventArgs.Data, isError);
        }
    }
}