namespace Ws5Lab;

public interface IExternalDataService
{
    Task<string> GetUserDataAsync(int userId, CancellationToken ct = default);
    Task<string> GetUserOrdersAsync(int userId, CancellationToken ct = default);
    Task<string> GetAdsAsync(CancellationToken ct = default);
    Task<string> GetAdsFromBackupAsync(CancellationToken ct = default);
}
