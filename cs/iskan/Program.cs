using TofuyaGame;

//Initialize components
GameState state = new GameState();
GameEngine engine = new GameEngine();

Console.WriteLine("--- PROFESSIONAL ISKANDAR TOFU SHOP ---");

while (!state.isGameOver)
{
    engine.UpdateWeather(state);

    Console.WriteLine($"\n[DAY {state.day}] Funds: {state.currentMoney} | Weather: {state.currentWeather}");
    Console.Write("Production amount: ");

    if(int.TryParse(Console.ReadLine(), out int qty) && qty >= 0)
    {
        if (qty * GameState.costPerBlock <= state.currentMoney)
        {
            engine.ProcessSale(state, qty);
            state.day++;
        }
        else
        {
            Console.WriteLine("(!) Not enough money!");
        }
    }
}

Console.WriteLine(state.isVictory ? "You Win!" : "Game Over!");