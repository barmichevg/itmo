using System;
using Homm.Core;

public static class Program
{
    public static void Main()
    {
        var engine = new SkillEngine();

        engine.RegisterAllCurrentlyLoadedAssemblies();

        var ctx = new BattleContext
        {
            DamageDealt = 100,
            Attacker = new UnitStats { Hp = 50 },
            Defender = new UnitStats { Hp = 100 }
        };

        Console.WriteLine("--- Starting Attack Phase ---");
        engine.ExecutePipeline(TriggerType.OnAttack, ctx);

        Console.WriteLine($"DamageDealt Final: {ctx.DamageDealt}");
        Console.WriteLine($"Attacker Final HP: {ctx.Attacker.Hp}");
    }
}
