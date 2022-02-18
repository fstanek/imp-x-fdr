using XUnifier.Models;
using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public interface IFormatHandler
    {
        // TODO bool HasInvertedScore

        string DisplayName { get;}
        Type ReaderType { get; }
        IEnumerable<Func<TableReader<CrosslinkSpectrumMatch>, bool>> ColumnHandlers { get; }
    }
}