namespace Ws5Lab;

public class PagePayload
{
    public string? UserData { get; set; }
    public string? OrderData { get; set; }
    public string? AdData { get; set; }

    public override string ToString() =>
        $"--- Агрегированный результат ---\n" +
        $"Пользователь: {UserData ?? "<null>"}\n" +
        $"Заказы: {OrderData ?? "<null>"}\n" +
        $"Реклама: {AdData ?? "<null>"}\n" +
        $"-----------------";
}
