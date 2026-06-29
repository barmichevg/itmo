using System;

namespace CityStatesConsoleApp
{
    public sealed class MerchantRepublic : CityState
    {
        private static readonly Random Rng = new();

        public MerchantRepublic() : base("Торговая республика ", 130, 35, 8) { }

        /// <summary>
        /// Спецумение: «Великая ярмарка» — лечит город на 15–25.
        /// </summary>
        public override void ApplySpecialAbility(params CityState[] cities)
        {
            foreach (var city in cities ?? Array.Empty<CityState>())
            {
                int healAmount = Rng.Next(15, 26);
                city.Heal(healAmount);
                Console.WriteLine($"{Name} проводит Великую ярмарку и укрепляет {city.Name} на {healAmount}.");
            }
        }
    }
}
