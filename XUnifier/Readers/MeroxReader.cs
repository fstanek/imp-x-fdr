using System.IO.Compression;
using XUnifier.Models;
using System.Globalization;

namespace XUnifier.Readers
{
    public class MeroxReader : CommaSeparatedReader
    {
        private ZipArchive zipArchive;
        private Stream stream;

        public MeroxReader(Stream stream) : base(stream)
        {
            CultureInfo = CultureInfo.GetCultureInfo("de-AT");
        }

        protected override void Initialize(Stream stream)
        {
            zipArchive = new ZipArchive(stream);
            var resultFile = zipArchive.GetEntry("Result.csv");

            this.stream = resultFile.Open();
            base.Initialize(this.stream);
        }

        protected override IEnumerable<Column> GetColumns()
        {
            yield break;
        }

        public override void Dispose()
        {
            stream.Dispose();
            zipArchive.Dispose();
            base.Dispose();
        }
    }
}