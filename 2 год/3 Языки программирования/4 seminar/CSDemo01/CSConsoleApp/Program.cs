using System.Runtime.InteropServices;

namespace CSConsoleApp
{
    public static class Program
    {
        public static void Main()
        {
            var currentDirectory = System.IO.Directory.GetCurrentDirectory();
            var filePath = System.IO.Directory.GetFiles(currentDirectory, "*.csv").First();

            IReadOnlyList<MovieCredit> movieCredits = null;
            try
            {
                movieCredits = CreditsCsvLoader.Load(filePath);
            }
            catch (Exception exc)
            {
                Console.WriteLine("Не удалось распарсить csv");
                Environment.Exit(1);
            }
            Queries.ExecuteAll(movieCredits);
        }
    }
}
