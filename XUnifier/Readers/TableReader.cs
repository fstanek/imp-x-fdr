using System.Globalization;
using XUnifier.Models;

namespace XUnifier.Readers
{
    public abstract class TableReader<TItem> : IDisposable
        where TItem : new()
    {
        // TODO add CultureInfo property

        private Column[] columns;
        private List<Action<TItem>> actions;

        public CultureInfo CultureInfo { get; set; } = CultureInfo.InvariantCulture;

        public TableReader(Stream stream)
        {
            Initialize(stream);

            columns = GetColumns().ToArray();
            actions = new List<Action<TItem>>();
        }

        // TODO filtering
        public bool Register<TValue>(string title, Action<TItem, TValue> handler)
        {
            var column = columns.FirstOrDefault(h => h.Title == title);

            if (column is null)
                return false;

            return Register(column.Index, handler);
        }

        public bool Register<TValue>(int index, Action<TItem, TValue> handler)
        {
            actions.Add(item =>
            {
                var value = GetValue<TValue>(index);
                handler(item, value);
            });

            return true;
        }

        public void Clear()
        {
            actions.Clear();
        }

        public IEnumerable<TItem> Read()
        {
            while (NextRow())
            {
                var item = new TItem();

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