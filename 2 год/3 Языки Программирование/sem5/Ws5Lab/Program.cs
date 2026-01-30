using System;
using System.Diagnostics;
using Ws5Lab;

int userId = 42;

var seds = new SlowExternalDataService(throwOrdersError: false);
var pas = new PageAggregatorService(seds);

// Последовательный вызов
Console.WriteLine("=== Последовательный вызов ===");
var sw = Stopwatch.StartNew();
var seq = await pas.LoadPageDataSequentialAsync(userId);
sw.Stop();
Console.WriteLine(seq);
Console.WriteLine($"Sequential elapsed: {sw.ElapsedMilliseconds} ms\n");


// Параллельный вызов
Console.WriteLine("=== Параллельный вызов ===");
sw.Restart();
var par = await pas.LoadPageDataParallelAsync(userId);
sw.Stop();
Console.WriteLine(par);
Console.WriteLine($"Parallel elapsed: {sw.ElapsedMilliseconds} ms\n");


// Отказоустойчивость
Console.WriteLine("=== Отказоустойчивость ===");
var slowFail = new SlowExternalDataService(throwOrdersError: true);
var aggFail = new PageAggregatorService(slowFail);
sw.Restart();
var parTolerant = await aggFail.LoadPageDataParallelAsync(userId, tolerateFailures: true);
sw.Stop();
Console.WriteLine(parTolerant);
Console.WriteLine($"Parallel (tolerant) elapsed: {sw.ElapsedMilliseconds} ms\n");


// Отмена операции (Cancellation)
Console.WriteLine("=== Отмена операции (Cancellation) ===");
using (var cts = new CancellationTokenSource(TimeSpan.FromMilliseconds(1500)))
{
    try
    {
        sw.Restart();
        var _ = await pas.LoadPageDataParallelAsync(userId, ct: cts.Token);
        sw.Stop();
        Console.WriteLine("Ожидалась отмена, но всё успело завершиться.");
    }
    catch (OperationCanceledException)
    {
        sw.Stop();
        Console.WriteLine($"Операция корректно отменена. elapsed: {sw.ElapsedMilliseconds} ms\n");
    }
}


// Конкуренция (Race Condition)
Console.WriteLine("=== Конкуренция (Race Condition) ===");
sw.Restart();
var parRace = await pas.LoadPageDataParallelAsync(userId, useAdBackupRace: true);
sw.Stop();
Console.WriteLine(parRace);
Console.WriteLine($"Parallel (ads race) elapsed: {sw.ElapsedMilliseconds} ms\n");
