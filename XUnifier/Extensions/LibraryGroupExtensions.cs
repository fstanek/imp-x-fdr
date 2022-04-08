using XUnifier.Models;

namespace XUnifier.Extensions
{
    public static class LibraryGroupExtensions
    {
        public static bool Contains(this LibraryGroup group, LinkerSite site)
        {
            return group.Sequences.Contains(site.Sequence)
                || group.Sequences.Any(s => s.Contains(site.Sequence));
        }
    }
}