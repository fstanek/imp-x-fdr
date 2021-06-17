using FDRCheck.Models;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;

namespace FDRCheck
{
    public class PythonEngine
    {
        private const string PythonPath = "Resources/python/python.exe";

        public event Func<string, bool, Task> MessageReceived;

        public void Run(string scriptFileName, IEnumerable<string> arguments)
        {
            using var process = new Process();
            process.StartInfo.FileName = PythonPath;
            process.StartInfo.ArgumentList.Add(scriptFileName);

            foreach (var argument in arguments)
                process.StartInfo.ArgumentList.Add(argument.ToString());

            process.StartInfo.RedirectStandardOutput = true;
            process.OutputDataReceived += (s, e) => OnMessageReceived(e, false);

            process.StartInfo.RedirectStandardError = true;
            process.ErrorDataReceived += (s, e) => OnMessageReceived(e, true);

            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();
            process.WaitForExit();
        }

        private void OnMessageReceived(DataReceivedEventArgs dataReceivedEventArgs, bool isError)
        {
            if (dataReceivedEventArgs.Data != null)
                MessageReceived?.Invoke(dataReceivedEventArgs.Data, isError);
        }

        public void Run(VennConfiguration vennConfiguration, IEnumerable<VennSegment> vennSegments)
        {
            var arguments = vennSegments.SelectMany(s => new[] { s.FileName, s.Title, s.Color.Value.ToString() }).ToArray();

            Run("Resources/scripts/venny.py", arguments);
        }
    }
}