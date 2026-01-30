using System;
using System.Collections.Generic;
using System.Linq;


namespace CityStatesConsoleApp

{
    public class WarManager
    {
        private readonly List<CityState> _cities = new();
        private readonly Random _random = new();

        private const double SpecialChance = 0.20;

        public WarManager(int pairCount)
        {
            if (pairCount <= 0)
                throw new ArgumentException("Pair count must be greater than zero.", nameof(pairCount));

            for (int i = 0; i < pairCount; i++)
            {
                _cities.Add(new FortressCity());
                _cities.Add(new MerchantRepublic());
            }
        }

        public void StartWar()
        {
            Console.WriteLine("Война началась");
            while (_cities.Count(c => c.Stability > 0) > 1)
            {
                var alive = _cities.Where(c => c.Stability > 0).ToList();
                var attacker = alive[_random.Next(alive.Count)];
                CityState target;
                do
                {
                    target = alive[_random.Next(alive.Count)];
                } while (ReferenceEquals(attacker, target) && alive.Count > 1);

                var used = TryUseSpecial(attacker, alive, target);
                if (!used && !ReferenceEquals(attacker, target))
                {
                    attacker.Attack(target);
                }
            }

            var winner = _cities.FirstOrDefault(c => c.Stability > 0);
            if (winner != null)
            {
                Console.WriteLine($"\n{winner.Name} — последний выстоявшое город-государство с {winner.Stability} стабильности!");
            }
            else
            {
                Console.WriteLine("\nВсе города пали!");
            }
        }

                private bool TryUseSpecial(CityState attacker, List<CityState> alive, CityState target)
        {
            if (_random.NextDouble() > SpecialChance)
                return false;
                
            switch (attacker)
            {
                case FortressCity fc:
                    if (target != null && !ReferenceEquals(attacker, target))
                                    {
                        Console.WriteLine($"{attacker.Name} использует особую способность!");
                        fc.ApplySpecialAbility(target);
                        return true;
                    }
                    break;

                case MerchantRepublic mr:
                    var toHeal = alive
                        .Where(c => c is MerchantRepublic && c.Stability > 0)
                        .OrderBy(c => c.Stability)
                        .Take(2)
                        .ToArray();

                    if (toHeal.Length == 0)
                        toHeal = new[] { attacker };

                    Console.WriteLine($"{attacker.Name} использует особую способность!");
                    mr.ApplySpecialAbility(toHeal);
                    return true;
            }

            return false;
        }

        public IEnumerable<CityState> Cities => _cities.AsReadOnly();
    }
}
