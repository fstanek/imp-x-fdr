using System.Globalization;
using System.IO;
using System.Windows.Controls;

namespace FDRCheck.Validation
{
    public class FileExistsRule : ValidationRule
    {
        public override ValidationResult Validate(object value, CultureInfo cultureInfo)
        {
            if (value is string fileName && File.Exists(fileName))
                return ValidationResult.ValidResult;

            return new ValidationResult(false, "File does not exist");
        }
    }
}