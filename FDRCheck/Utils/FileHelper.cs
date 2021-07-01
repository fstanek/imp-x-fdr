using System.Diagnostics;
using System.IO;

namespace FDRCheck.Utils
{
    public static class FileHelper
    {
        public static bool IsValidFileName(string fileName)
        {
            try
            {
                new FileInfo(fileName);
                return true;
            }
            catch
            {
                return false;
            }
        }

        public static bool IsValidDirectory(string directoryName)
        {
            try
            {
                new DirectoryInfo(directoryName);
                return true;
            }
            catch
            {
                return false;
            }
        }

        public static void TryOpenDirectory(string fileName)
        {
            if (string.IsNullOrWhiteSpace(fileName))
                return;

            var fileInfo = new FileInfo(fileName);
            if (fileInfo.Directory.Exists)
                Process.Start("explorer.exe", fileInfo.Directory.FullName);
        }
    }
}