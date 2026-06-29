using System;

namespace CityStatesConsoleApp
{
    public abstract class CityState
    {
        private static readonly Random Rng = new();

        protected CityState(string baseName, int stability, int influence, int fortification)
        {
            if (string.IsNullOrWhiteSpace(baseName))
                throw new ArgumentException("Name cannot be null or empty.", nameof(baseName));

            Name = $"{baseName} #{Rng.Next(0, 1000)}";
            Stability = stability;
            Influence = influence;
            Fortification = fortification;
        }

        /// <summary> Название города-государства </summary>
        public string Name { get; set; }

        /// <summary> Стабильность (HP) </summary>
        public int Stability { get; protected set; }

        public int Influence { get; set; }

        public int Fortification { get; set; }

        public void Attack(CityState target)
        {
            int damage = Influence - target.Fortification;
            if (damage < 0) damage = 0;

            target.TakeDamage(damage);
            Console.WriteLine($"{Name} атакует на {target.Name}: урон влиянием {damage}.");
        }

        public void TakeDamage(int damage)
        {
            Stability -= damage;

            if (Stability < 0) Stability = 0;
            Console.WriteLine($"{Name} теряет {damage} стабильности. Остаток: {Stability}");
        }

        public void Heal(int amount)
        {
            if (amount < 0)
                throw new ArgumentException("Heal amount cannot be negative.", nameof(amount));

            Stability += amount;
            Console.WriteLine($"{Name} укрепляется на {amount}. Текущая стабильность: {Stability}");
        }

        public abstract void ApplySpecialAbility(params CityState[] cities);
    }
}
