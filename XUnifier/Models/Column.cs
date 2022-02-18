namespace XUnifier.Models
{
    //[DebuggerDisplay("{Title}")]
    public class Column
    {
        public string Title { get; set; }
        public int Index { get; set; }

        public Column()
        {

        }

        public Column(string title, int index)
        {
            Title = title;
            Index = index;
        }

        public override string ToString()
        {
            return Title;
        }
    }
}