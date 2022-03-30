using System.Globalization;
using XUnifier.Models;
using XUnifier.Utils;

namespace XUnifier.Readers
{
    public class CommaSeparatedReader : CrosslinkReader
    {
        // TODO move to TextHelper
        private static readonly char[] Separators = { '\t', ',', ';' };

        private StreamReader reader;
        private char? separator;
        private string[] currentRow;

        public CommaSeparatedReader(Stream stream) : base(stream)
        {

        }

        protected override void Initialize(Stream stream)
        {
            reader = new StreamReader(stream);
        }

        protected override IEnumerable<Column> GetColumns()
        {
            NextRow();

            for (int i = 0; i < currentRow.Length; i++)
            {
                yield return new Column
                {
                    Index = i,
                    Title = currentRow[i]
                };
            }
        }

        protected override bool NextRow()
        {
            if (reader.EndOfStream)
                return false;

            var line = reader.ReadLine();

            if(!separator.HasValue)
            {
                var separators = GetSeparator(line).ToArray();
                separator = separators.First();
            }

            currentRow = TextHelper.Split(line, separator.Value).ToArray();
            return true;
        }

        // TODO move to text helper
        private IEnumerable<char> GetSeparator(string line)
        {
            return from separator in Separators
                   let count = line.Count(c => c == separator)
                   orderby count descending
                   select separator;
        }

        protected override TValue GetValue<TValue>(int index)
        {
            var textValue = currentRow[index];
            var targetType = typeof(TValue);

            if (IsNumber(targetType))
                textValue = textValue.Replace(CultureInfo.NumberFormat.NumberGroupSeparator, null);

            return (TValue)Convert.ChangeType(textValue, targetType, CultureInfo);
        }

        private bool IsNumber(Type type)
        {
            switch (Type.GetTypeCode(type))
            {
                case TypeCode.Byte:
                case TypeCode.SByte:
                case TypeCode.UInt16:
                case TypeCode.UInt32:
                case TypeCode.UInt64:
                case TypeCode.Int16:
                case TypeCode.Int32:
                case TypeCode.Int64:
                case TypeCode.Decimal:
                case TypeCode.Double:
                case TypeCode.Single:
                    return true;
                default:
                    return false;
            }
        }

        public override void Dispose()
        {
            reader.Dispose();
        }
    }
}