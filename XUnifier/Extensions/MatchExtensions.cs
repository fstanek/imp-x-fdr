using System.Text.RegularExpressions;

namespace XUnifier.Extensions
{
    public static class MatchExtensions
    {
        public static string GetString(this Match match, string groupName)
        {
            return match.Groups[groupName].Value;
        }

        public static int GetInt32(this Match match, string groupName)
        {
            var text = match.GetString(groupName);
            return int.Parse(text);
        }
    }
}