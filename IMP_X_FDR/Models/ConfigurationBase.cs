using System.Collections.Generic;

namespace IMP_X_FDR.Models
{
    public abstract class ConfigurationBase : BaseModel
    {
        public abstract string ScriptName { get; }
        public abstract IEnumerable<string> Arguments { get; }

        public ConfigurationBase()
        {
            Reset();
        }

        public abstract void Reset();
    }
}
