using System.Collections.Generic;

namespace FDRCheck.Models
{
    public abstract class ConfigurationBase : BaseModel
    {
        public abstract string ScriptName { get; }

        public abstract IEnumerable<string> GetArguments();
        public abstract void Clear();
    }
}
