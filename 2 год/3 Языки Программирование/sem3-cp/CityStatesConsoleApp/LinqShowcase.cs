using System;
using System.Collections.Generic;
using System.Linq;

namespace CityStatesConsoleApp
{
    internal static class LinqShowcase
    {
        public static void Run(IEnumerable<CityState> cities)
        {
            var strongholds = cities
                .Where(c => c.Fortification >= 15)
                .Select(c => c.Name);

            Console.WriteLine("Сильные города:");
            foreach (var name in strongholds)
            {
                Console.WriteLine(name);
            }
        }
    }
}
