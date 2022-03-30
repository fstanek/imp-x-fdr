namespace XUnifier.Models
{
    public class LibraryGroup : IEquatable<LibraryGroup>
    {
        public string Name { get; set; }
        public HashSet<string> Sequences { get; set; }

        public bool Equals(LibraryGroup? other)
        {
            if (other is null)
                return false;

            return Name == other.Name;
        }

        public override int GetHashCode()
        {
            return Name.GetHashCode();
        }
    }
}