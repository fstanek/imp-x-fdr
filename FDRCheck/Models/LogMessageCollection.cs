using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace FDRCheck.Models
{
    public class LogMessageCollection : ObservableCollection<LogMessage>
    {
        public LogMessageCollection()
        {
        }

        public LogMessageCollection(IEnumerable<LogMessage> collection) : base(collection)
        {
        }

        public LogMessageCollection(List<LogMessage> list) : base(list)
        {
        }
    }
}