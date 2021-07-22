using System;
using System.Windows;
using System.Windows.Interop;
using IWin32Window = System.Windows.Forms.IWin32Window;

namespace IMP_X_FDR.Utils
{
    public static class WindowHelper
    {
        public static void ShowError(DependencyObject dependencyObject, string text)
        {
            var window = Window.GetWindow(dependencyObject);
            MessageBox.Show(window, text, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        public static IWin32Window GetWin32Window(Window window)
        {
            var handle = new WindowInteropHelper(window).Handle;
            return new WindowWrapper(handle);
        }

        public static IWin32Window GetWin32Window(DependencyObject dependencyObject)
        {
            var window = Window.GetWindow(dependencyObject);
            return GetWin32Window(window);
        }

        private class WindowWrapper : IWin32Window
        {
            public IntPtr Handle { get; }

            public WindowWrapper(IntPtr handle)
            {
                Handle = handle;
            }
        }
    }
}