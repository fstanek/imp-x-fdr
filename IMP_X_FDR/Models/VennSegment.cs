using MediaColor = System.Windows.Media.Color;
using SystemColor = System.Drawing.Color;

namespace IMP_X_FDR.Models
{
    public class VennSegment : BaseModel
    {
        private string fileName;
        private string title;
        private MediaColor? color;

        public string FileName
        {
            get => fileName;
            set { fileName = value; OnPropertyChanged(nameof(FileName)); }
        }

        public string Title
        {
            get => title;
            set { title = value; OnPropertyChanged(nameof(Title)); }
        }

        public MediaColor? Color
        {
            get => color;
            set { color = value; OnPropertyChanged(nameof(Color)); }
        }

        public bool IsValid
        {
            get => Color.HasValue && !string.IsNullOrWhiteSpace(FileName);
        }

        public void Reset()
        {
            FileName = null;
            Title = null;
            Color = null;
        }

        public SystemColor GetSystemColor()
        {
            return SystemColor.FromArgb(Color.Value.R, Color.Value.G, Color.Value.B);
        }

        public void SetSystemColor(SystemColor color)
        {
            Color = MediaColor.FromRgb(color.R, color.G, color.B);
        }
    }
}