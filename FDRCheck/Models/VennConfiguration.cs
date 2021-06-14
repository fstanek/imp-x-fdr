using System.Windows.Media;

namespace FDRCheck.Models
{
    public class VennConfiguration
    {
        public string OutputFileName { get; set; }
        public VennSegment[] VennSegments { get; }

        public VennConfiguration()
        {
            /*
             * <controls:VennyInputPanel DataContext="{Binding VennSegments[0]}" VennColor="#B5F8FE"></controls:VennyInputPanel>
             * <controls:VennyInputPanel DataContext="{Binding VennSegments[1]}" VennColor="#FDB87F"></controls:VennyInputPanel>
             * <controls:VennyInputPanel DataContext="{Binding VennSegments[2]}" VennColor="#10FFCB"></controls:VennyInputPanel>
             * <controls:VennyInputPanel DataContext="{Binding VennSegments[3]}" VennColor="#F75590"></controls:VennyInputPanel>
             */

            VennSegments = new[]
            {
                new VennSegment { Color = Color.FromRgb(181, 248, 254) },
                new VennSegment { Color = Color.FromRgb(253, 184, 127) },
                new VennSegment { Color = Color.FromRgb(16, 255, 203) },
                new VennSegment { Color = Color.FromRgb(247, 85, 144) }
            };
        }
    }
}