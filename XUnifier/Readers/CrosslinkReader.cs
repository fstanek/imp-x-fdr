using System.Globalization;
using XUnifier.Handlers;
using XUnifier.Models;

namespace XUnifier.Readers
{
    public abstract class CrosslinkReader : IDisposable
    {
        // TODO define handlers here, e.g. abstract GetHandlers

        private Column[] columns;
        private List<Action<Crosslink>> actions;
        private List<Func<bool>> filters;

        public IFormatHandler FormatHandler { get; private set; }
        public CultureInfo CultureInfo { get; set; } = CultureInfo.InvariantCulture;

        public CrosslinkReader(Stream stream)
        {
            Initialize(stream);

            columns = GetColumns().ToArray();
            actions = new List<Action<Crosslink>>();
            filters = new List<Func<bool>>();

            FormatHandler = GetHandlers().FirstOrDefault(h => h.CanRead(this));

            if (FormatHandler is null)
                throw new Exception("Unknown file format.");

            FormatHandler.Apply(this);
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

        public void Filter<TValue>(string title, Func<TValue, bool> handler)
        {
            var column = columns.FirstOrDefault(h => h.Title == title);

            if (column is not null)
                Filter(column.Index, handler);
        }

        public void Filter<TValue>(int index, Func<TValue, bool> handler)
        {
            filters.Add(() =>
            {
                var value = GetValue<TValue>(index);
                return handler(value);
            });
        }

        public IEnumerable<Crosslink> Read()
        {
            while (NextRow())
            {
                if (FilterItem())
                {
                    var item = new Crosslink();

                    foreach (var action in actions)
                        action(item);

                    yield return item;
                }
            }
        }

        private bool FilterItem()
        {
            if (!filters.Any())
                return true;

            return filters.Any(f => f());
        }

        protected abstract void Initialize(Stream stream);
        protected abstract IEnumerable<Column> GetColumns();
        protected abstract IEnumerable<IFormatHandler> GetHandlers();
        protected abstract bool NextRow();
        protected abstract TValue GetValue<TValue>(int index);

        public abstract void Dispose();
    }
}