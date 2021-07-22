using System.Windows.Media;

namespace IMP_X_FDR.Models
{
    public class VennSegment : BaseModel
    {
        private string fileName;
        private string title;
        private Color? color;

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

        public Color? Color
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
    }
}