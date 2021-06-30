namespace FDRCheck.Constants
{
    public static class FileFilters
    {
        public static readonly string All = GetFilter("All files", "*");
        public static readonly string Csv = GetFilter("Comma-separated files", "csv");
        public static readonly string Excel = GetFilter("Excel files", "xlsx");

        private static string GetFilter(string name, string extension)
        {
            return $"{name}|*.{extension}";
        }
    }
}