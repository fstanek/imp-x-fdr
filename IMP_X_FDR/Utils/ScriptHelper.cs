using System.IO;

namespace IMP_X_FDR.Utils
{
    public static class ScriptHelper
    {
        public static string GetDefaultLibraryFileName()
        {
            return Path.GetFullPath("Resources/libraries/main_library.xlsx");
        }
    }
}