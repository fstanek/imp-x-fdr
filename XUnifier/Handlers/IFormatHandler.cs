using XUnifier.Readers;

namespace XUnifier.Handlers
{
    public interface IFormatHandler
    {
        // TODO bool HasInvertedScore

        string DisplayName { get; }
        bool IsGrouped { get; }

        bool CanRead(CrosslinkReader reader);
        void Apply(CrosslinkReader reader);
    }
}