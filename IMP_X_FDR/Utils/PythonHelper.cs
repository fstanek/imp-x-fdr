using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using XUnifier.Utils;

namespace IMP_X_FDR.Utils
{
    public static class PythonHelper
    {
        // TODO if 'python' not found, try add to PATH
        /*
         * var name = "PATH";
         * var scope = EnvironmentVariableTarget.Machine; // or User
         * var oldValue = Environment.GetEnvironmentVariable(name, scope);
         * var newValue  = oldValue + @";C:\Program Files\MySQL\MySQL Server 5.1\bin\\";
         * Environment.SetEnvironmentVariable(name, newValue, scope);
         */

        private const string RequirementsPath = "Resources/requirements.txt";

        private static string pythonPath;
        public static bool IsPythonInstalled => pythonPath != null;

        public static void Initialize()
        {
            pythonPath = new[]
            {
                //"python",
                FromRegistryKey(Registry.CurrentUser),
                FromRegistryKey(Registry.LocalMachine)
            }.FirstOrDefault(ValidatePythonPath);

            if (IsPythonInstalled)
                TryInstallPackages();
        }

        private static string FromRegistryKey(RegistryKey registryKey)
        {
            const string Key64 = @"Software\Wow6432Node\Python\PythonCore";
            const string Key32 = @"Software\Python\PythonCore";

            var pythonCore = registryKey.OpenSubKey(Key64) ?? registryKey.OpenSubKey(Key32);
            if (pythonCore is null)
                return null;

            var version = pythonCore.GetSubKeyNames().OrderBy(Version.Parse).LastOrDefault();
            if (version is null)
                return null;

            var installPath = pythonCore?.OpenSubKey($@"{version}\InstallPath");
            var fileName = installPath?.GetValue("ExecutablePath") as string;

            return File.Exists(fileName)
                ? fileName
                : null;
        }

        private static bool ValidatePythonPath(string path)
        {
            if (string.IsNullOrWhiteSpace(path))
                return false;

            try
            {
                return Run(path, "--version");
            }
            catch
            {
                return false;
            }
        }

        private static bool Run(string fileName, string arguments)
        {
            using var process = new Process();
            process.StartInfo.FileName = fileName;
            process.StartInfo.Arguments = arguments;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.RedirectStandardError = true;
            process.StartInfo.UseShellExecute = false;
            //#if !DEBUG
            process.StartInfo.CreateNoWindow = true;
            //#endif
            process.Start();
            process.WaitForExit();

            var output = process.StandardOutput.ReadToEnd();
            var error = process.StandardError.ReadToEnd();

            return process.ExitCode == 0;
        }

        private static void TryInstallPackages()
        {
            Run(pythonPath, $"-m pip install -r \"{RequirementsPath}\"");
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

        public static PythonHandler CreateHandler()
        {
            return new PythonHandler(pythonPath);
        }
    }
}