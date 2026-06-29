namespace Ws5Lab;

public sealed class SlowExternalDataService : IExternalDataService
{
    private readonly bool _throwOrdersError;
    public SlowExternalDataService(bool throwOrdersError) => _throwOrdersError = throwOrdersError;

    public async Task<string> GetUserDataAsync(int userId, CancellationToken ct = default)
    {
        Log("GetUserDataAsync START");
        try
        {
            await Task.Delay(2000, ct);
            return $"User#{userId}: Alice";
        }
        finally { Log("GetUserDataAsync END"); }
    }

    public async Task<string> GetUserOrdersAsync(int userId, CancellationToken ct = default)
    {
        Log("GetUserOrdersAsync START");
        try
        {
            await Task.Delay(3000, ct);
            if (_throwOrdersError)
                throw new Exception("Orders API failed (simulated).");
            return $"Orders for #{userId}: [A123, B456, C789]";
        }
        finally { Log("GetUserOrdersAsync END"); }
    }

    public async Task<string> GetAdsAsync(CancellationToken ct = default)
    {
        Log("GetAdsAsync START");
        try
        {
            await Task.Delay(1000, ct);
            return "Ads: Super Sale -50%";
        }
        finally { Log("GetAdsAsync END"); }
    }

    public async Task<string> GetAdsFromBackupAsync(CancellationToken ct = default)
    {
        Log("GetAdsFromBackupAsync START");
        try
        {
            await Task.Delay(1500, ct);
            return "Ads (backup): Clearance -40%";
        }
        finally { Log("GetAdsFromBackupAsync END"); }
    }

    private static void Log(string msg)
    {
        var ts = DateTime.Now.ToString("HH:mm:ss.fff");
        Console.WriteLine($"[{ts}] [T{Environment.CurrentManagedThreadId}] {msg}");
    }
}
