using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public abstract class FormatHandlerBase<TReader> : IFormatHandler
        where TReader : CrosslinkReader
    {
        private readonly Type readerType;
        private readonly List<string> names;
        private readonly List<Action<CrosslinkReader>> actions;
        private readonly List<Action<CrosslinkReader>> filters;

        public abstract string DisplayName { get; }
        public abstract bool IsGrouped { get; }

        public FormatHandlerBase()
        {
            readerType = typeof(TReader);
            names = new List<string>();
            actions = new List<Action<CrosslinkReader>>();
            filters = new List<Action<CrosslinkReader>>();

            Initialize();
        }

        protected abstract void Initialize();

        protected void Register<TValue>(int index, Action<Crosslink, TValue> handler)
        {
            actions.Add(reader => reader.Register(index, handler));
        }

        protected void Register<TValue>(string name, Action<Crosslink, TValue> handler)
        {
            names.Add(name);
            actions.Add(reader => reader.Register(name, handler));
        }

        protected void Filter<TValue>(int index, Func<TValue, bool> handler)
        {
            filters.Add(reader => reader.Filter(index, handler));
        }

        protected void Filter<TValue>(string name, Func<TValue, bool> handler)
        {
            filters.Add(reader => reader.Filter(name, handler));
        }

        public bool CanRead(CrosslinkReader reader)
        {
            return reader.GetType().IsAssignableFrom(readerType)
                && names.All(reader.HasColumn);
        }

        public void Apply(CrosslinkReader reader)
        {
            foreach (var action in actions)
                action(reader);

            foreach (var filter in filters)
                filter(reader);
        }
    }
}