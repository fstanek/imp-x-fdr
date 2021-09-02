using IMP_X_FDR.Utils;
using System.Linq;

namespace IMP_X_FDR.Converters
{
    public class MaxQuantToAnnikaConverter : IFileConverter
    {
        public void Convert(string sourceFileName, string targetFileName)
        {
            var csms = MaxQuantHelper.ReadCsms(sourceFileName).ToArray();
            var groupedCsms = MaxQuantHelper.GroupCrosslinks(csms).ToArray();
            MSAnnikaHelper.WriteAnnikaResult(targetFileName, groupedCsms);
        }
    }
}