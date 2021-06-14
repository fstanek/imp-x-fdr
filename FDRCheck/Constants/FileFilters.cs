namespace FDRCheck.Constants
{
    public static class FileFilters
    {
        public static readonly string All = GetFilter("All files", ".*");
        public static readonly string Excel = GetFilter("Excel files", FileExtensions.Excel);

        private static string GetFilter(string name, string extension)
        {
            return $"{name} ({extension})|*{extension}";
        }
    }
}