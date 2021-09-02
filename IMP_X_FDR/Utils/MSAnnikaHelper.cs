using IMP_X_FDR.Models;
using OfficeOpenXml;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace IMP_X_FDR.Utils
{
    public static class MSAnnikaHelper
    {
        static MSAnnikaHelper()
        {
            ExcelPackage.LicenseContext = LicenseContext.NonCommercial;
        }

        public static void WriteAnnikaResult(string fileName, IEnumerable<CrosslinkSpectrumMatch> csms)
        {
            using ExcelPackage package = new ExcelPackage();
            var worksheet = package.Workbook.Worksheets.Add("Crosslinks");

            var columns = new (string title, Func<CrosslinkSpectrumMatch, object> selector)[]
            {
                ("Sequence A", csm => csm.Sequence1 ),
                ("Accession A", csm => csm.Protein1 ),
                ("In protein A", csm => csm.ProInterLink1 ),

                ("Sequence B", csm => csm.Sequence2 ),
                ("Accession B", csm => csm.Protein2 ),
                ("In protein B", csm => csm.ProInterLink2 ),

                ("Best CSM Score", csm => csm.Score )
            };

            var rowIndex = 1;
            var header = columns.Select(c => c.title).ToArray();
            WriteLine(worksheet, rowIndex++, header);

            foreach (var csm in csms)
            {
                var values = columns.Select(c => c.selector(csm)).ToArray();
                WriteLine(worksheet, rowIndex++, values);
            }

            var fileInfo = new FileInfo(fileName);
            package.SaveAs(fileInfo);
        }

        private static void WriteLine(ExcelWorksheet worksheet, int rowIndex, object[] values)
        {
            var columnIndex = 1;

            foreach (var value in values)
            {
                worksheet.SetValue(rowIndex, columnIndex, value);
                columnIndex++;
            }
        }
    }
}