using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;

namespace Homm.Core;

public sealed class SkillEngine
{
    private sealed record SkillEntry(
        string Name,
        int Priority,
        Action<BattleContext> Handler,
        MethodInfo SourceMethod
    );

    private readonly Dictionary<TriggerType, List<SkillEntry>> _pipeline = new();
    private readonly HashSet<string> _registeredNames = new(StringComparer.OrdinalIgnoreCase);

    public SkillEngine()
    {
        foreach (TriggerType t in Enum.GetValues(typeof(TriggerType)))
            _pipeline[t] = new List<SkillEntry>();


        AppDomain.CurrentDomain.AssemblyLoad += (_, e) => RegisterAssembly(e.LoadedAssembly);
    }

    public void RegisterAllCurrentlyLoadedAssemblies()
    {
        foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
            RegisterAssembly(asm);
    }


    public void RegisterAssembly(Assembly assembly)
{
    Type[] types;
    try { types = assembly.GetTypes(); }
    catch (ReflectionTypeLoadException ex)
    {
        types = ex.Types.Where(t => t != null).Cast<Type>().ToArray();
    }

    var gameTypes = types.Where(t =>
        t is { IsAbstract: false, IsInterface: false } &&
        t.GetCustomAttribute<GameAttribute>() != null);

    foreach (var type in gameTypes)
    {
        object? instance = null;

        var methods = type.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.Static);
        foreach (var method in methods)
        {
            var skillAttr = method.GetCustomAttribute<CombatSkillAttribute>();
            if (skillAttr is null) continue;

            if (!IsValidSignature(method))
                continue;

            if (!_registeredNames.Add(skillAttr.Name))
                continue;

            var handler = BuildHandler(type, ref instance, method);

            _pipeline[skillAttr.Trigger].Add(new SkillEntry(
                Name: skillAttr.Name,
                Priority: skillAttr.Priority,
                Handler: handler,
                SourceMethod: method
            ));

            Console.WriteLine(
                $"Registered logic: {skillAttr.Name} " +
                $"(Trigger={skillAttr.Trigger}, Priority={skillAttr.Priority}, " +
                $"Method={type.FullName}.{method.Name}, Assembly={assembly.GetName().Name})"
            );
        }
    }

    foreach (var key in _pipeline.Keys.ToList())
    {
        _pipeline[key] = _pipeline[key]
            .OrderByDescending(s => s.Priority)
            .ThenBy(s => s.Name, StringComparer.OrdinalIgnoreCase)
            .ToList();
    }
}


    public void ExecutePipeline(TriggerType trigger, BattleContext context)
    {
        if (!_pipeline.TryGetValue(trigger, out var list) || list.Count == 0)
            return;

        foreach (var skill in list)
        {
            try
            {
                skill.Handler(context);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[SkillEngine] Skill '{skill.Name}' failed: {ex.Message}");
            }
        }
    }

    private static bool IsValidSignature(MethodInfo method)
    {
        if (method.IsGenericMethodDefinition) return false;
        if (method.ReturnType != typeof(void)) return false;

        var p = method.GetParameters();
        return p.Length == 1 && p[0].ParameterType == typeof(BattleContext);
    }

    private static Action<BattleContext> BuildHandler(Type declaringType, ref object? instance, MethodInfo method)
    {
        if (method.IsStatic)
        {
            return (Action<BattleContext>)method.CreateDelegate(typeof(Action<BattleContext>));
        }

        instance ??= CreateInstanceOrThrow(declaringType);
        return (Action<BattleContext>)method.CreateDelegate(typeof(Action<BattleContext>), instance);
    }

    private static object CreateInstanceOrThrow(Type type)
    {
        var ctor = type.GetConstructor(Type.EmptyTypes);
        if (ctor is null)
            throw new InvalidOperationException(
                $"Type '{type.FullName}' must have public parameterless constructor for skill discovery.");

        return Activator.CreateInstance(type)!;
    }
}
