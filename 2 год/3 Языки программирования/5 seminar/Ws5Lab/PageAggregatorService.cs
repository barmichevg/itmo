namespace Ws5Lab;

public sealed class PageAggregatorService : IPageAggregator
{
    private readonly IExternalDataService _ext;
    public PageAggregatorService(IExternalDataService ext) => _ext = ext;

    public async Task<PagePayload> LoadPageDataSequentialAsync(int userId, CancellationToken ct = default)
    {
        // Последовательно
        var user = await _ext.GetUserDataAsync(userId, ct);
        var orders = await _ext.GetUserOrdersAsync(userId, ct);
        var ads = await _ext.GetAdsAsync(ct);
        
        return new PagePayload {
            UserData = user,
            OrderData = orders,
            AdData = ads
        };
    }

    public async Task<PagePayload> LoadPageDataParallelAsync(
        int userId,
        CancellationToken ct = default,
        bool tolerateFailures = false,
        bool useAdBackupRace = false)
    {
        // Параллельно
        var userTask   = _ext.GetUserDataAsync(userId, ct);
        var ordersTask = _ext.GetUserOrdersAsync(userId, ct);
        Task<string> adsTask = useAdBackupRace ? AdsRaceAsync(ct) : _ext.GetAdsAsync(ct);

        if (!tolerateFailures)
        {
            await Task.WhenAll(userTask, ordersTask, adsTask);
            return new PagePayload
            {
                UserData  = await userTask,
                OrderData = await ordersTask,
                AdData    = await adsTask
            };
        }

        // Отказоустойчиво
        try { await Task.WhenAll(userTask, ordersTask, adsTask); }
        catch { /* ignore */ }

        string? Take(Task<string> t) => t.IsCompletedSuccessfully ? t.Result : null;

        return new PagePayload
        {
            UserData  = Take(userTask),
            OrderData = Take(ordersTask),
            AdData    = Take(adsTask)
        };
    }

    // Гонка
    private async Task<string> AdsRaceAsync(CancellationToken ct)
    {
        var primary = _ext.GetAdsAsync(ct);
        var backup = _ext.GetAdsFromBackupAsync(ct);
        var first = await Task.WhenAny(primary, backup);
        return await first;
    }
}
