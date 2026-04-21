namespace TofuyaGame;

public class GameEngine
{
    private readonly Random _rng = new Random();

    public void UpdateWeather(GameState state)
    {
        string[] types = { "Clear", "Cloudy", "Rainy" };
        state.currentWeather = types[_rng.Next(types.Length)];
    }

    public int CalculateDemand(string Weather)
    {
        return Weather switch
        {
            "Clear" => _rng.Next(60, 141),
            "Cloudy" => _rng.Next(30, 71),
            "Rainy" => _rng.Next(5, 31),
            _ => 50
        };
    }

    public void ProcessSale(GameState state, int productionQuantity)
    {
        int totalCost = productionQuantity * GameState.costPerBlock;
        state.currentMoney -= totalCost;

        int demand = CalculateDemand(state.currentWeather);
        int sold = Math.Min(productionQuantity, demand);
        int revenue = sold * GameState.pricePerBlock;

        state.currentMoney += revenue;

        Console.WriteLine($"\n--- End of Day {state.day} ---");
        Console.WriteLine($"Customers: {demand} | Sold: {sold}");
        Console.WriteLine($"Profit: {revenue - totalCost} yen");
    }
}