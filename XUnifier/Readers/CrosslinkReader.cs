using System.Globalization;
using XUnifier.Models;

namespace XUnifier.Readers
{
    public abstract class CrosslinkReader : IDisposable
    {
        // TODO consider filtering (e.g. Decoys)

        private Column[] columns;
        private List<Action<Crosslink>> actions;

        public CultureInfo CultureInfo { get; set; } = CultureInfo.InvariantCulture;

        public CrosslinkReader(Stream stream)
        {
            Initialize(stream);

            columns = GetColumns().ToArray();
            actions = new List<Action<Crosslink>>();
        }

        public bool HasColumn(string title)
        {
            return columns.Any(c => c.Title == title);
        }

        // TODO filtering
        public void Register<TValue>(string title, Action<Crosslink, TValue> handler)
        {
            var column = columns.FirstOrDefault(h => h.Title == title);

            if (column != null)
                Register(column.Index, handler);
        }

        public void Register<TValue>(int index, Action<Crosslink, TValue> handler)
        {
            actions.Add(item =>
            {
                var value = GetValue<TValue>(index);
                handler(item, value);
            });
        }

        public IEnumerable<Crosslink> Read()
        {
            while (NextRow())
            {
                var item = new Crosslink();

                foreach (var action in actions)
                    action(item);

                yield return item;
            }
        }

        protected abstract void Initialize(Stream stream);
        protected abstract IEnumerable<Column> GetColumns();
        protected abstract bool NextRow();
        protected abstract TValue GetValue<TValue>(int index);

        public abstract void Dispose();
    }
}