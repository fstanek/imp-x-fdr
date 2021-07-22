using IMP_X_FDR.Models;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace IMP_X_FDR.Utils
{
    public static class ScriptHelper
    {
        private const char CommentPrefix = '#';

        public static IEnumerable<SearchEngine> GetSearchEngines(string path)
        {
            foreach (var fileName in Directory.EnumerateFiles(path))
            {
                var displayName = Path.GetFileNameWithoutExtension(fileName);
                var header = File.ReadLines(fileName).FirstOrDefault();

                if (header.StartsWith(CommentPrefix))
                    displayName = header.Trim(CommentPrefix);

                yield return new SearchEngine
                {
                    ScriptName = fileName,
                    DisplayName = displayName
                };
            }
        }

        public static string GetDefaultLibraryFileName()
        {
            return Path.GetFullPath("Resources/libraries/support_peplib1.xlsx");
        }
    }
}