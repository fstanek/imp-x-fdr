using System.Globalization;

namespace XUnifier.Writers
{
    public class CommaSeparatedWriter<TItem> : IDisposable
    {
        private readonly StreamWriter writer;
        private readonly List<string> headers;
        private readonly List<Func<TItem, object>> handlers;
        private readonly char separator;

        public CommaSeparatedWriter(Stream stream, char? separator = null)
        {
            writer = new StreamWriter(stream);
            this.separator = separator ?? CultureInfo.CurrentCulture.TextInfo.ListSeparator.First();

            headers = new List<string>();
            handlers = new List<Func<TItem, object>>();
        }

        public void Register(string header, Func<TItem, object> handler)
        {
            headers.Add(header);
            handlers.Add(handler);
        }

        public void Write(IEnumerable<TItem> items)
        {
            writer.WriteLine(string.Join(separator, headers));

            foreach (var item in items)
            {
                var columns = handlers.Select(h => h(item));
                var line = string.Join(separator, columns);
                writer.WriteLine(line);
            }

            writer.Flush();
        }

        public void Dispose()
        {
            writer.Dispose();
        }
    }
}