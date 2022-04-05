using OfficeOpenXml;
using XUnifier.Handlers;
using XUnifier.Models;

namespace XUnifier.Readers
{
    public class ExcelReader : CrosslinkReader
    {
        private ExcelPackage package;
        private ExcelWorksheet sheet;
        private int currentRow;

        static ExcelReader()
        {
            // TODO move to appsettings
            ExcelPackage.LicenseContext = LicenseContext.NonCommercial;
        }

        public ExcelReader(Stream stream) : base(stream)
        {

        }

        protected override void Initialize(Stream stream)
        {
            package = new ExcelPackage(stream);
            sheet = package.Workbook.Worksheets.First();
            currentRow = 1;
        }

        protected override IEnumerable<Column> GetColumns()
        {
            return Enumerable.Range(1, sheet.Dimension.Columns).Select(i =>
            {
                return new Column
                {
                    Index = i,
                    Title = sheet.GetValue<string>(1, i)
                };
            });
        }

        protected override IEnumerable<IFormatHandler> GetHandlers()
        {
            yield return new AnnikaFormatHandler();
            yield return new AnnikaXLFormatHandler();
            yield return new XLinkXFormatHandler();
        }

        protected override bool NextRow()
        {
            currentRow++;
            return currentRow <= sheet.Dimension.Rows;
        }

        protected override TValue GetValue<TValue>(int index)
        {
            return sheet.GetValue<TValue>(currentRow, index);
        }

        public override void Dispose()
        {
            package.Dispose();
        }
    }
}