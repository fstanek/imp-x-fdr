using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace FDRCheck.Models
{
    public class SearchEngineCollection : ObservableCollection<SearchEngine>
    {
        public SearchEngineCollection()
        {
        }

        public SearchEngineCollection(IEnumerable<SearchEngine> collection) : base(collection)
        {
        }

        public SearchEngineCollection(List<SearchEngine> list) : base(list)
        {
        }
    }
}