using System;

namespace IMP_X_FDR.Models
{
    public class LogMessage
    {
        public DateTime DateTime { get; set; }
        public string Text { get; set; }
        public bool IsError { get; set; }
    }
}