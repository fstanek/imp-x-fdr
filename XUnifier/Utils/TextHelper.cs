using System.Globalization;
using System.Text;

namespace XUnifier.Utils
{
    public static class TextHelper
    {
        public static IEnumerable<string> Split(string line, char separator = ',', char quote = '"')
        {
            var queue = new Queue<char>(line);
            var builder = new StringBuilder();
            var isQuoting = false;

            while (queue.Any())
            {
                var letter = queue.Dequeue();

                if (letter == separator && !isQuoting)
                {
                    yield return builder.ToString();
                    builder.Clear();
                }
                else if (letter == quote)
                {
                    if (queue.Peek() == quote)
                    {
                        builder.Append(queue.Dequeue());
                    }
                    else
                    {
                        isQuoting = builder.Length == 0;
                    }
                }
                else
                {
                    builder.Append(letter);
                }
            }

            yield return builder.ToString();
        }
    }
}