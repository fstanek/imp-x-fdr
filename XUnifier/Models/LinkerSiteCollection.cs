namespace XUnifier.Models
{
    public class LinkerSiteCollection : List<LinkerSite>
    {
        // TODO use ReadOnlyCollection?

        public LinkerSiteCollection()
        {
            Add(new LinkerSite());
            Add(new LinkerSite());
        }

        public LinkerSiteCollection(IEnumerable<LinkerSite> collection) : base(collection)
        {

        }
    }
}