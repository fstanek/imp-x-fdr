﻿using System.Collections.Generic;

namespace IMP_X_FDR.Models
{
    public abstract class ConfigurationBase : BaseModel
    {
        public abstract string ScriptName { get; }
        

        public ConfigurationBase()
        {
            Reset();
        }

        public abstract IEnumerable<string> GetArguments(string inputFileName);
        public abstract void Reset();
    }
}
