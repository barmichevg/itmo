using System;
using Homm.Core;

[Game]
public class VampireMechanics
{
    [CombatSkill("Vampirism", TriggerType.OnAttack, 10)]
    public void ExecuteLifeDrain(BattleContext ctx)
    {
        int healAmount = (int)(ctx.DamageDealt * 0.5);
        ctx.Attacker.Hp += healAmount;
        Console.WriteLine($"[System] Vampirism activation: healed {healAmount} HP.");
    }

    [CombatSkill("CriticalStrike", TriggerType.OnAttack, 100)]
    public void ExecuteCrit(BattleContext ctx)
    {
        ctx.DamageDealt *= 2;
        Console.WriteLine("[System] CRITICAL HIT! Damage doubled.");
    }
}
