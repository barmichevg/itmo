namespace Ws5Lab;

public interface IPageAggregator
{
    Task<PagePayload> LoadPageDataSequentialAsync(int userId, CancellationToken ct = default);

    Task<PagePayload> LoadPageDataParallelAsync(
        int userId,
        CancellationToken ct = default,
        bool tolerateFailures = false,
        bool useAdBackupRace = false);
}
