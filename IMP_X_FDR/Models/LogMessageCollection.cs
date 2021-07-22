using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace IMP_X_FDR.Models
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