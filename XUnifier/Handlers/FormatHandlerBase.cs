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

        public abstract string DisplayName { get; }

        public FormatHandlerBase()
        {
            readerType = typeof(TReader);
            names = new List<string>();
            actions = new List<Action<CrosslinkReader>>();

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

        public bool CanRead(CrosslinkReader reader)
        {
            return reader.GetType().IsAssignableFrom(readerType)
                && names.All(reader.HasColumn);
        }

        public void Apply(CrosslinkReader reader)
        {
            foreach (var action in actions)
                action(reader);
        }
    }
}