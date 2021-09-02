using IMP_X_FDR.Models;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

namespace IMP_X_FDR.Utils
{
    public static class MaxQuantHelper
    {
        private const char Separator = '\t';
        private const string DecoyPattern = "forward";
        private const string IgnorePattern = "-";

        public static IEnumerable<CrosslinkSpectrumMatch> ReadCsms(string fileName)
        {
            using var reader = new StreamReader(fileName);

            var header = GetValues(reader);
            var indices = new
            {
                Decoy = Array.IndexOf(header, "Decoy"),
                Score = Array.IndexOf(header, "Score"),

                Protein1 = Array.IndexOf(header, "Proteins1"),
                Protein2 = Array.IndexOf(header, "Proteins2"),

                ProInterLink1 = Array.IndexOf(header, "Pro_InterLink1"),
                ProInterLink2 = Array.IndexOf(header, "Pro_InterLink2"),

                Sequence1 = Array.IndexOf(header, "Sequence1"),
                Sequence2 = Array.IndexOf(header, "Sequence2")
            };

            while (!reader.EndOfStream)
            {
                var values = GetValues(reader);

                if (values[indices.Decoy] == DecoyPattern && values[indices.Sequence2] != IgnorePattern)
                {
                    yield return new CrosslinkSpectrumMatch
                    {
                        Score = ParseScore(values[indices.Score]),

                        Protein1 = ParseAccession(values[indices.Protein1]),
                        Protein2 = ParseAccession(values[indices.Protein2]),

                        ProInterLink1 = ParsePosition(values[indices.ProInterLink1]),
                        ProInterLink2 = ParsePosition(values[indices.ProInterLink2]),

                        Sequence1 = values[indices.Sequence1],
                        Sequence2 = values[indices.Sequence2],
                    };
                }
            }
        }

        private static string[] GetValues(StreamReader reader)
        {
            return reader.ReadLine().Split(Separator);
        }

        private static float ParseScore(string text)
        {
            return float.Parse(text, CultureInfo.InvariantCulture);
        }

        private static string ParseAccession(string text)
        {
            var match = Regex.Match(text, @"\|([^\|]+)\|");
            return match.Groups[1].Value;
        }

        private static int ParsePosition(string text)
        {
            return int.Parse(text.Trim(';'));
        }

        public static IEnumerable<CrosslinkSpectrumMatch> GroupCrosslinks(IEnumerable<CrosslinkSpectrumMatch> csms)
        {
            return from csm in csms
                   group csm by new
                   {
                       csm.Protein1,
                       csm.ProInterLink1,
                       csm.Protein2,
                       csm.ProInterLink2
                   } into csmGroup
                   select new CrosslinkSpectrumMatch
                   {
                       Protein1 = csmGroup.Key.Protein1,
                       Protein2 = csmGroup.Key.Protein2,
                       ProInterLink1 = csmGroup.Key.ProInterLink1,
                       ProInterLink2 = csmGroup.Key.ProInterLink2,
                       Sequence1 = csmGroup.First().Sequence1,
                       Sequence2 = csmGroup.First().Sequence2,
                       Score = csmGroup.Max(c => c.Score)
                   };
        }
    }
}