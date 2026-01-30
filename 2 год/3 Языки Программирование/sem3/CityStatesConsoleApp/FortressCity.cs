using System;
using System.Linq;

namespace CityStatesConsoleApp
{
    public class FortressCity : CityState
    {
        public FortressCity() : base("Крепость-город", 180, 28, 18) { }

        /// <summary>
        /// Спецумение: «Наёмники» — двойной удар.
        /// </summary>
        public override void ApplySpecialAbility(params CityState[] cities)
        {
            var target = cities?.FirstOrDefault();
            if (target == null) return;

            Console.WriteLine($"{Name} нанимает наёмников! Двойной удар по {target.Name}.");
            Attack(target);
            Attack(target);
        }
    }
}
