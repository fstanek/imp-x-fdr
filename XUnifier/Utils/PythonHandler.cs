﻿using System.Diagnostics;

namespace XUnifier.Utils
{
    public class PythonHandler : IDisposable
    {
        private readonly Process process;

        public event Action<string> OutputReceived;
        public event Action<string> ErrorReceived;

        public PythonHandler()
        {
            process = CreateProcess();

            process.OutputDataReceived += (s, e) =>
            {
                if (!string.IsNullOrWhiteSpace(e.Data))
                    OutputReceived?.Invoke(e.Data);
            };

            process.ErrorDataReceived += (s, e) =>
            {
                if (!string.IsNullOrWhiteSpace(e.Data))
                    ErrorReceived?.Invoke(e.Data);
            };
        }

        public static Process CreateProcess()
        {
            var process = new Process();

            process.StartInfo = new ProcessStartInfo
            {
                FileName = "python",
                UseShellExecute = false,
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            };

            // use unbuffered streams (https://stackoverflow.com/questions/53379866/running-python-script-on-c-sharp-and-getting-output-continuously#answer-53380763)
            process.StartInfo.ArgumentList.Add("-u");

            return process;
        }

        public void AddArgument(string argument)
        {
            process.StartInfo.ArgumentList.Add(argument);
        }

        public int Run(Stream inputStream)
        {
            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            inputStream.CopyTo(process.StandardInput.BaseStream);
            process.StandardInput.Close();

            process.WaitForExit();
            return process.ExitCode;
        }

        public int Run(IEnumerable<string> lines = null)
        {
            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            foreach (var line in lines ?? Enumerable.Empty<string>())
                process.StandardInput.WriteLine(line);

            process.StandardInput.Close();
            process.WaitForExit();

            return process.ExitCode;
        }

        public int Run(out string outputText, out string errorText)
        {
            process.Start();
            process.WaitForExit();

            outputText = process.StandardOutput.ReadToEnd();
            errorText = process.StandardError.ReadToEnd();

            return process.ExitCode;
        }

        public void Dispose()
        {
            process.Dispose();
        }
    }
}