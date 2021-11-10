using IMP_X_FDR.Converters;
using IMP_X_FDR.Models;
using System;
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
                var searchEngine = new SearchEngine
                {
                    ScriptName = fileName,
                    DisplayName = Path.GetFileNameWithoutExtension(fileName)
                };

                var header = File.ReadLines(fileName).FirstOrDefault();
                if (header.StartsWith(CommentPrefix))
                {
                    var headerInfos = header.Trim(CommentPrefix).Split('|');
                    searchEngine.DisplayName = headerInfos.First();

                    if (headerInfos.ElementAtOrDefault(1) is string referenceFileName && !string.IsNullOrWhiteSpace(referenceFileName))
                    {
                        searchEngine.ReferenceScript = Path.Combine(Path.GetDirectoryName(fileName), referenceFileName);
                    }

                    if (headerInfos.ElementAtOrDefault(2) is string fileConverterType && !string.IsNullOrWhiteSpace(fileConverterType))
                    {
                        var type = Type.GetType(fileConverterType);
                        searchEngine.FileConverter = Activator.CreateInstance(type) as IFileConverter;
                    }
                }

                yield return searchEngine;
            }
        }

        public static string GetDefaultLibraryFileName()
        {
            return Path.GetFullPath("Resources/libraries/main_library.xlsx");
        }
    }
}