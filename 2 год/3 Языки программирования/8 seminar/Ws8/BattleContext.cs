using System;

namespace Homm.Core;

public class BattleContext
{
    public int DamageDealt { get; set; }
    public UnitStats Attacker { get; set; } = new();
    public UnitStats Defender { get; set; } = new();
}

public class UnitStats { public int Hp { get; set; } }

public enum TriggerType { OnAttack, OnDefense, PostBattle }

[AttributeUsage(AttributeTargets.Method, Inherited = false, AllowMultiple = false)]
public sealed class CombatSkillAttribute : Attribute
{
    public string Name { get; }
    public TriggerType Trigger { get; }
    public int Priority { get; }

    public CombatSkillAttribute(string name, TriggerType trigger, int priority = 1)
    {
        Name = name;
        Trigger = trigger;
        Priority = priority;
    }
}

[AttributeUsage(AttributeTargets.Class, Inherited = false, AllowMultiple = false)]
public sealed class GameAttribute : Attribute { }
