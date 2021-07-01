﻿using FDRCheck.Models;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace FDRCheck.Utils
{
    public static class ScriptHelper
    {
        private const string ScriptPath = "Resources/scripts/";
        private const char CommentPrefix = '#';

        public static IEnumerable<SearchEngine> GetSearchEngines()
        {
            foreach (var fileName in Directory.EnumerateFiles(ScriptPath))
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
    }
}