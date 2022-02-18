using OfficeOpenXml;
using XUnifier.Models;

namespace XUnifier.Readers
{
    public class ExcelReader<TItem> : TableReader<TItem>
        where TItem : new()
    {
        private ExcelPackage package;
        private ExcelWorksheet sheet;
        private int currentRow;

        static ExcelReader()
        {
            ExcelPackage.LicenseContext = LicenseContext.NonCommercial;
        }

        public ExcelReader(Stream stream) : base(stream)
        {

        }

        protected override void Initialize(Stream stream)
        {
            package = new ExcelPackage(stream);
            sheet = package.Workbook.Worksheets.First();
            currentRow = 0;
        }

        protected override IEnumerable<Column> GetColumns()
        {
            NextRow();

            return Enumerable.Range(1, sheet.Dimension.Columns).Select(i =>
            {
                return new Column
                {
                    Index = i,
                    Title = sheet.GetValue<string>(1, i)
                };
            });
        }

        protected override bool NextRow()
        {
            if (currentRow > sheet.Dimension.Rows)
                return false;

            currentRow++;
            return true;
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