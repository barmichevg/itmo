using System;
using System.Collections.Generic;

namespace CityStatesConsoleApp
{
    static class Program
    {
        public static void Main(string[] args)
        {
            var cities = GetCities();
            foreach (var city in cities)
            {
                Console.WriteLine($"{city.Name} — Stability: {city.Stability}, Influence: {city.Influence}, Fortification: {city.Fortification}");
            }

            LinqShowcase.Run(cities);

            var warManager = new WarManager(5);
            warManager.StartWar();

            Console.ReadKey();
        }

        public static IEnumerable<CityState> GetCities()
        {
            var list = new List<CityState>();
            for (int i = 0; i < 3; i++)
            {
                list.Add(new FortressCity());
                list.Add(new MerchantRepublic());
            }
            return list;
        }
    }
}
