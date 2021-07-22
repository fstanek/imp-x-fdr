using FDRCheck.Utils;
using System.Collections.ObjectModel;
using System.Linq;

namespace FDRCheck.Models
{
    public class RecalculationConfiguration : JobConfiguration
    {
        private SearchEngine searchEngine;

        public SearchEngine SearchEngine 
        {
            get => searchEngine; set { searchEngine = value; OnPropertyChanged(nameof(SearchEngine)); }
        }

        public ObservableCollection<SearchEngine> SearchEngines { get; } = new ObservableCollection<SearchEngine>();

        public override string ScriptName => SearchEngine.ScriptName;

        public override void Reset()
        {
            base.Reset();

            SearchEngines.Clear();

            foreach (var searchEngine in ScriptHelper.GetSearchEngines("Resources/search-engines/"))
                SearchEngines.Add(searchEngine);

            SearchEngine = SearchEngines.First();
        }
    }
}