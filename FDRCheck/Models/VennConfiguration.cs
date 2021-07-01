using System.Collections.Generic;
using System.Windows.Media;

namespace FDRCheck.Models
{
    public class VennConfiguration : ConfigurationBase
    {
        private VennSegment[] vennSegments;
        private string outputFileName;
        private bool isIdle = true;

        public VennSegment[] VennSegments
        {
            get => vennSegments;
            set { vennSegments = value; OnPropertyChanged(nameof(VennSegments)); }
        }

        public string OutputFileName
        {
            get => outputFileName;
            set { outputFileName = value; OnPropertyChanged(nameof(OutputFileName)); }
        }

        public bool IsIdle
        {
            get => isIdle;
            set { isIdle = value; OnPropertyChanged(nameof(IsIdle)); }
        }

        public override string ScriptName => throw new System.NotImplementedException();

        public VennConfiguration()
        {
            Clear();
        }

        public override IEnumerable<string> GetArguments()
        {
            throw new System.NotImplementedException();
        }

        public override void Clear()
        {
            VennSegments = new[]
             {
                new VennSegment { Color = Color.FromRgb(181, 248, 254) },
                new VennSegment { Color = Color.FromRgb(253, 184, 127) },
                new VennSegment { Color = Color.FromRgb(16, 255, 203) },
                new VennSegment { Color = Color.FromRgb(247, 85, 144) }
            };

            OutputFileName = null;
        }
    }
}